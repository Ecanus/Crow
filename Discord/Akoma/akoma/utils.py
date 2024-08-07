import datetime
import requests

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from typing import Text, Optional, Any, Dict, List

import akoma.constants as c
from akoma.errors import WhatIsError

def get_definitions_from_website(word: Text) -> Text:
    """Returns definitions associated with the given word from the
    DICTIONARY_URL.
    If no definitions can be found, returns an appropriate message.
    """
    url = c.DICTIONARY_URL.format(word=word)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if response.status_code == c.RESPONSE_200:
        try:
            entry_word_section = soup.find_all(class_=c.ENTRY_WORD_CLASS)

            return get_definitions_from_entry_word_section(
                entry_word_section).format(word=word)
        except WhatIsError as e:
            return e.format(word=word)
        except Exception as e:
            return c.EXCEPTION_TEXT.format(e)

    elif response.status_code == c.RESPONSE_404:
        # Check if misspelled
        if soup.find(class_=c.MISSPELLED_WORD_CLASS):
            spelling_suggestions_str =\
                get_formatted_spelling_suggestions_from_div(
                soup.find(c.DIV_ELEMENT, class_=c.SPELLING_SUGGESTION_CLASS))

            return spelling_suggestions_str.format(word=word)
        else:
            return c.MISSPELLED_WORD_MSG.format(word=word)
    else:
        return c.REQUEST_ERROR_MESSAGE.format(
            url=url,
            code=response.status_code
        )

def get_definitions_from_entry_word_section(
        entry_word_section: ResultSet[Any]) -> Text:
    """Returns all definitions associated with the given entry_word_section.
    """
    # key: part of speech
    # value: concatenated string of  vg_divs for corresponding part of speech
    definitions_dict = {}

    # If entry_word_section is None or empty
    if not entry_word_section:
        return c.NO_DEFINITIONS_FOUND_MSG

    for entry in entry_word_section:
        pos_soup = entry.find(class_=c.PARTS_OF_SPEECH_CLASS)
        pos_value = pos_soup.get_text() if pos_soup else None

        # If no part of speech, check if respelling link provided
        if pos_value is None:
            return try_get_respelling_definitions(entry_word_section)

        vg_divs = entry.find_all(class_=c.VG_CLASS)
        definitions_dict[pos_value] = get_definitions_str_from_vg_divs(vg_divs)

    return get_formatted_definitions_str(definitions_dict)

def try_get_respelling_definitions(
        entry_word_section: ResultSet[Any]) -> Text:
    """Attempts to find a link in the webpage which redirects to an
    alternative spelling of the word being searched for.

    If an alternative spelling is found, returns the definitions
    for this word.

    Else, raises a WhatIsError.
    """
    respelling_soup = entry_word_section[0].find(
        "a", class_=c.RESPELLING_CLASS)

    try:
        respelled_word = respelling_soup.get_text()
        return get_definitions_from_website(respelled_word)
    except AttributeError:
        raise WhatIsError(c.RESPELLING_ERROR_TEXT)


def get_definitions_str_from_vg_divs(vg_divs: ResultSet[Any]) -> Text:
    """Returns a concatenated string of all definitions found within the
    given vg_divs iterable.
    """
    entry_str = ""

    for vg_div in vg_divs:
        vg_entry_divs = vg_div.find_all(class_=c.VG_ENTRY_ITEM_CLASS)

        # vd label
        vd_heading = vg_div.find(class_=c.VD_CLASS)
        if vd_heading:
            entry_str += "*{vd_heading}*\n".format(
                vd_heading=vd_heading.get_text())

        # vg entry divs
        for vg_entry_div in vg_entry_divs:
            # Num Label
            num_label = vg_entry_div.find(class_=c.VG_ENTRY_ITEM_LABEL_CLASS)
            num_label = num_label.get_text()

            if int(num_label) > c.DEFINITION_DISPLAY_NUM:
                break

            entry_str += "> **{}**.\n".format(num_label)

            # Sub-Entries
            sub_entry_divs = vg_entry_div.find_all(
                class_=c.SUB_ENTRY_CLASS)

            for sub_entry_div in sub_entry_divs:
                letter_label = sub_entry_div.find(class_=c.LETTER_CLASS)

                definition = sub_entry_div.find(
                    c.SPAN_ELEMENT, class_=c.DEFINITION_CLASS)
                definition = definition.get_text().replace(": ", "", 1)

                if letter_label and definition:
                    entry_str += "> {letter_label}) {definition}\n".format(
                        letter_label=letter_label.get_text(),
                        definition=definition)
                elif definition and not letter_label:
                    entry_str += "> {definition}\n".format(
                        definition=definition)
                else:
                    continue

            entry_str += "\n"

    return entry_str.strip()

def get_formatted_definitions_str(
        definitions_dict: Dict[Text, Text]) -> Text:
    """Parses through the given definitions_dict and returns a
    well-formatted string containing definitions sorted by part of speech.
    """
    definitions_str = c.WHATIS_RESPONSE_HEADER

    for pos in definitions_dict:
        definitions_str += "__***{pos}***__\n\n".format(pos=pos)
        definitions_str += "{}".format(definitions_dict[pos])

        definitions_str += "\n\n"

    return definitions_str.strip()

def get_formatted_spelling_suggestions_from_div(
        spelling_suggestion_soup: ResultSet[Any]) -> Text:
    """Parses through the given spelling_suggestion_soup and returns a
    well-formatted string of possible spelling suggestions.
    """
    suggestions_str = c.WHATIS_RESPONSE_HEADER
    suggestions_str += c.MISSPELLED_WORD_TEXT
    suggestions_str += " " + c.SPELLING_SUGGESTION_TEXT

    all_spelling_suggestions = spelling_suggestion_soup.find_all(
        class_=c.SPELLING_SUGGESTIONS_CLASS)[
            :c.SPELLING_SUGGESTION_DISPLAY_NUM]

    for suggestion in all_spelling_suggestions:
        suggestions_str += ("- {}\n").format(suggestion.get_text())

    return suggestions_str.strip()

def append_signature(input_str: Text) -> Text:
    """Appends the signature of the bot to the given input_str.
    Returns the new joined string."""
    return input_str.strip() + "\n\n" + c.SIGNATURE

def format_date(
        date: datetime.datetime,
        format: Optional[Text]=c.DATETIME_FORMAT_LONG) -> Text:
    """Returns a well-formated date string for readability using the
    given format value."""
    return date.strftime(format)
import datetime
import requests

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from typing import Text, Optional, Any, Dict, List

import akoma.constants as constants
from akoma.errors import WhatIsError

def get_definitions_from_website(word: Text) -> Text:
    """Returns definitions associated with the given word from the
    DICTIONARY_URL.
    If no definitions can be found, returns an appropriate message.
    """
    url = constants.DICTIONARY_URL.format(word=word)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if response.status_code == constants.RESPONSE_200:
        try:
            entry_word_section = soup.find_all(class_=constants.ENTRY_WORD_CLASS)

            return get_definitions_from_entry_word_section(
                entry_word_section).format(word=word)
        except WhatIsError as e:
            return e.format(word=word)
        except Exception as e:
            return constants.EXCEPTION_TEXT.format(e)

    elif response.status_code == constants.RESPONSE_404:
        # Check if misspelled
        if soup.find(class_=constants.MISSPELLED_WORD_CLASS):
            spelling_suggestions_str =\
                get_formatted_spelling_suggestions_from_div(
                soup.find("div", class_=constants.SPELLING_SUGGESTION_CLASS))

            return spelling_suggestions_str.format(word=word)
        else:
            return constants.MISSPELLED_WORD_MSG.format(word=word)
    else:
        return constants.REQUEST_ERROR_MESSAGE.format(
            url=url,
            code=response.status_code
        )

    # Check if regional spelling variant. Return definition anyways.

def get_definitions_from_entry_word_section(
        entry_word_section: ResultSet[Any]) -> Dict[Text, Text]:
    """Returns all definitions associated with the given entry_word_section.
    """
    definition_dict = {}

    # If entry_word_section is None or empty
    if not entry_word_section:
        return constants.NO_DEFINITIONS_FOUND_MSG

    for entry in entry_word_section:
        pos_soup = entry.find(class_=constants.PARTS_OF_SPEECH_CLASS)
        pos_value = pos_soup.get_text() if pos_soup else None

        if pos_value is None:
            return try_get_respelling_definitions(entry_word_section)

        definition_dict[pos_value] = []

        # Definitions are found within <span class="dtText">
        entries = entry.find_all("span", class_=constants.DEFINITION_CLASS)
        for definition in entries:
            definition_dict[pos_value].append(definition.get_text())

    definitions_str = get_formatted_definitions_str(definition_dict)

    return definitions_str

def try_get_respelling_definitions(
        entry_word_section: ResultSet[Any]) -> Text:
    respelling_soup = entry_word_section[0].find(
        "a", class_=constants.RESPELLING_CLASS)

    try:
        respelled_word = respelling_soup.get_text()
        return get_definitions_from_website(respelled_word)
    except AttributeError:
        raise WhatIsError(constants.RESPELLING_ERROR_TEXT)



def get_formatted_definitions_str(
        definitions_dict: Dict[Text, List[Text]]) -> Text:
    """Parses through the given definitions_dict and returns a
    well-formatted string containing definitions sorted by part of speech.
    """
    definitions_str = constants.WHATIS_RESPONSE_HEADER

    for pos in definitions_dict:
        definitions_str += "*{pos}*\n".format(pos=pos.capitalize())
        definitions_to_display =\
            definitions_dict[pos][:constants.DEFINITION_DISPLAY_NUM]

        for i, definition in enumerate(definitions_to_display, 1):
            definition = definition.replace(": ", "", 1).strip().capitalize()
            definitions_str += (
                "{i}. {definition}\n").format(
                    i=i,
                    definition=definition
                )

        definitions_str += "\n"

    return definitions_str.strip()

def get_formatted_spelling_suggestions_from_div(
        spelling_suggestion_soup: ResultSet[Any]) -> Text:
    """Parses through the given spelling_suggestion_soup and returns a
    well-formatted string of possible spelling suggestions.
    """
    suggestions_str = constants.WHATIS_RESPONSE_HEADER
    suggestions_str += constants.MISSPELLED_WORD_TEXT
    suggestions_str += " " + constants.SPELLING_SUGGESTION_TEXT

    all_spelling_suggestions = spelling_suggestion_soup.find_all(
        class_=constants.SPELLING_SUGGESTIONS_CLASS)[
            :constants.SPELLING_SUGGESTION_DISPLAY_NUM]

    for suggestion in all_spelling_suggestions:
        suggestions_str += ("- {}\n").format(suggestion.get_text())

    return suggestions_str.strip()

def append_signature(input_str: Text) -> Text:
    """Appends the signature of the bot to the given input_str.
    Returns the new joined string."""
    return input_str.strip() + "\n\n" + constants.SIGNATURE

def format_date(
        date: datetime.datetime,
        format: Optional[Text]=constants.DATETIME_FORMAT_LONG) -> Text:
    """Returns a well-formated date string for readability using the
    given format value."""
    return date.strftime(format)
from typing import Text, Optional
import datetime
from PyDictionary import PyDictionary

from constants import SIGNATURE, DATETIME_FORMAT_LONG

def sign(input_str: Text) -> Text:
    """Appends the signature of the bot to the given input_str.
    Returns the new joined string."""
    return input_str.strip() + "\n\n" + SIGNATURE

def get_definition_str(word: Text) -> Text:
    """Returns a string containing the definition of the given word.
    If no definition can be found, returns a fail message."""
    dictionary = PyDictionary()
    meaning_dict = dictionary.meaning(word)

    # No definition found
    if meaning_dict is None:
        return "No definition can be found for: {word}".format(word=word)
        pass

    definition_str = ":books: **{}**\n\n".format(word)

    for key in meaning_dict:
        definition_str += "*{key}*\n".format(key=key)

        for i, meaning in enumerate(meaning_dict[key], 1):
            # Capitalise first letter
            # meaning = meaning[0].upper() + meaning[1:]

            definition_str += (
                "{i}. {meaning}\n").format(
                    i=i,
                    meaning=meaning
                )

        definition_str += "\n"

    return definition_str.strip()

def format_date(
        date: datetime.datetime,
        format: Optional[Text]=DATETIME_FORMAT_LONG) -> Text:
    """Returns a well-formated date string for readability using the
    given format value."""
    return date.strftime(format)


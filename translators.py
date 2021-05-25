import csv
import time

from textblob import TextBlob
from textblob.exceptions import NotTranslated


class TranslatorInterface:
    def translate_text(self, text: str, target_language_code: str, source_language_code: str) -> str:
        pass


class Dummy (TranslatorInterface):
    def translate_text(self, text: str, target_language_code: str, source_language_code: str) -> str:
        return ""


class Dictionary (TranslatorInterface):
    def __init__(self):
        self.dictionary = {}
        with open('en_lt.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.dictionary[row[0]] = row[1]

    def translate_text(self, text: str, target_language_code: str, source_language_code: str = None) -> str:
        return self.dictionary.get(text, "")


class Blob (TranslatorInterface):
    def translate_text(self, text: str, target_language_code: str, source_language_code: str = "auto") -> str:
        time.sleep(1)
        try:
            translation: TextBlob = TextBlob(text).translate(from_lang=source_language_code, to=target_language_code)
            return translation.string
        except NotTranslated:
            return text

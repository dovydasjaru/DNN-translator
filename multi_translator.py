from typing import List

import translators as t
import wikipedia


class MultiTranslator:
    __dict_conf = "#Confidence 1#"
    __wiki_conf = "#Confidence 0.9#"
    __wiki_tran_conf = "#Confidence 0.5#"
    __tran_conf = "#Confidence 0.3#"

    def __init__(self, is_en_to_lt: bool = True):
        if is_en_to_lt:
            self.dictionary_translator = t.Dictionary()
        else:
            self.dictionary_translator = t.Dummy()
        self.blob_translator = t.Blob()

    def translate(self, text: List[str], target_language: str, source_language: str, add_confidence: bool = False) -> \
            List[str]:
        dict_conf = ""
        wiki_conf = ""
        wiki_tran_conf = ""
        tran_conf = ""
        if add_confidence:
            dict_conf = MultiTranslator.__dict_conf
            wiki_conf = MultiTranslator.__wiki_conf
            wiki_tran_conf = MultiTranslator.__wiki_tran_conf
            tran_conf = MultiTranslator.__tran_conf
        results = []
        for word in text:
            translation = self.dictionary_translator.translate_text(word, target_language, source_language)
            if translation != "":
                results.append(translation + dict_conf)
                continue
            wikipedia_result = wikipedia.make_request(word, target_language, source_language)
            if 'translated' in wikipedia_result:
                results.append(wikipedia_result['result'] + wiki_conf)
                continue

            if wikipedia_result["result"] != "":
                translation = self.dictionary_translator.translate_text(wikipedia_result["result"].split(":", 1)[0],
                                                                        target_language, source_language)
                if translation != "":
                    results.append(translation + dict_conf)
                    continue
                translation = self.blob_translator.translate_text(wikipedia_result["result"], target_language,
                                                                  source_language)
                results.append(translation.split(":", 1)[0] + wiki_tran_conf)
            else:
                results.append(self.blob_translator.translate_text(word, target_language, source_language) + tran_conf)

        return results

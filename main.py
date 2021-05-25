import multi_translator
import label_reader_writer as rw
import label_finder as finder
import argparse


def translate_dnn(location: str, target_language: str, source_language: str, append_confidence: bool):
    label_files = finder.find_labels_file(location)
    code_files = finder.find_labels_code(location)
    if len(label_files) + len(code_files) == 1:
        if len(label_files) == 1:
            label_reader = rw.read_labels_file
            label_writer = rw.write_labels_file
            label_location = label_files[0]
        else:
            label_reader = rw.read_labels_code
            label_writer = rw.write_labels_code
            label_location = code_files[0]

        print("found: " + label_location + " file")

        data = label_reader(label_location)
        print("read label file")
        untranslated = data["name_list"]
        translated = []
        t = multi_translator.MultiTranslator()
        translation_points = len(untranslated)
        counter = 0
        for line in untranslated:
            translated.append(t.translate(line, target_language, source_language, append_confidence))
            counter += 1
            print("translated ", counter, " of ", translation_points)
        print("writing translated labels")
        label_writer(label_location, translated, data)
        print("done")
    elif len(label_files) + len(code_files) > 1:
        print("Found more than one possible labels file:")
        print("Possible labels in files: ", label_files)
        print("Possible labels in code: ", code_files)
        print("Please specify which file to use")
    else:
        print("Did not find any label files")


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--inputLanguage", required=False,
                help="Language that models labels are written. Should be in form of two ascii letters")
ap.add_argument("-o", "--outputLanguage", required=False,
                help="Language that models labels will be translated. Should be in form of two ascii letters")
ap.add_argument("-c", "--appendConfidence", required=False, action='store_true',
                help="A flag that means translation confidence will be appended to each translation")
args, file = ap.parse_known_args()

if args.inputLanguage is None:
    args.inputLanguage = "en"
if args.outputLanguage is None:
    args.outputLanguage = "lt"
if len(file) == 1:
    translate_dnn(file[0], args.inputLanguage, args.outputLanguage, args.appendConfidence)
else:
    print("Expected one file location")

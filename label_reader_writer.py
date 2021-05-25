from typing import List
import re


__separators = [",", ";", "."]
__pattern = r'= \[[\n]?[ ]*["\']([_A-Za-z ]+)["\'],([\n ][ ]*["\'][A-Za-z ]+["\'],)+([\n ][ ]*["\'][A-Za-z ]+["\'])?[\n]?[ ]*\]'


def read_labels_file(file_location: str) -> dict:
    with open(file_location, 'r') as f:
        labels = [label.rstrip() for label in f]
    has_id = any(character.isdigit() for character in labels[0])

    names = labels[0]
    id_separator = ""
    if has_id:
        id_separator = get_id_separator(labels[0])
        names = labels[0].split(id_separator, 1)[1]

    names_separator = get_names_separator(names)

    id_list = []
    name_list = []
    for label in labels:
        if has_id:
            id_and_names = label.split(id_separator, 1)
            name_list.append(id_and_names[1].split(names_separator))
            id_list.append(id_and_names[0])
        else:
            name_list.append(label.split(names_separator))
            id_list.append("")
    return {"id_list": id_list, "name_list": name_list, "id_separator": id_separator, "name_separator": names_separator}


def write_labels_file(file_location: str, translations: List[List[str]], reader_output: dict):
    id_separator = reader_output["id_separator"].encode('utf8')
    writer = open(file_location, 'wb')
    for i in range(len(reader_output["id_list"])):
        writer.write(reader_output["id_list"][i].encode('utf8'))
        writer.write(id_separator)
        writer.write(reader_output["name_separator"].join(translations[i]).encode('utf8'))
        writer.write("\n".encode('utf8'))

    writer.close()


def get_id_separator(id_and_names: str) -> str:
    id_length = id_and_names.find(" ")
    id_separator = " "
    for sep in __separators:
        separated_length = id_and_names.find(sep)
        if id_length > separated_length != -1 or id_length == -1:
            id_length = separated_length
            id_separator = sep

    index = id_and_names.find(id_separator)
    if index != -1:
        if id_and_names[index + 1] == " ":
            id_separator += " "
    else:
        return ""
    return id_separator


def get_names_separator(names: str) -> str:
    for sep in __separators:
        if sep in names:
            index = names.index(sep)
            if names[index + 1] == " ":
                sep += " "
            return sep
    return ""


def read_labels_code(file_location: str) -> dict:
    with open(file_location, 'r') as f:
        text = f.read()

    result = re.search(__pattern, text).group(0)
    if "\"" in result:
        separator = "\""
    else:
        separator = "'"
    result_list = result.split(separator)

    name_list = list()
    for i in range(1, len(result_list), 2):
        name_list.append([result_list[i]])

    return {"name_list": name_list, "original": result_list, "separator": separator}


def write_labels_code(file_location: str, translations: List[List[str]], reader_output: dict):
    result_list = reader_output["original"].copy()
    i = 1
    for translated in translations:
        result_list[i] = translated[0]
        i += 2
    result = reader_output["separator"].join(result_list)
    with open(file_location, 'r') as f:
        text = f.read()
    text = text.replace(reader_output["separator"].join(reader_output["original"]), result)
    with open(file_location, 'w', encoding="utf8") as f:
        f.write(text)

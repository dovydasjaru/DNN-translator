import os
from typing import List
import re


allowed_file_extensions = ["csv", "txt"]
allowed_code_extensions = ["py"]
__pattern = r'= \[[\n]?[ ]*["\']([_A-Za-z ]+)["\'],([\n]?[ ]*["\'][A-Za-z ]+["\'],)+([\n]?[ ]*["\'][A-Za-z ]+["\'])?[\n]?[ ]*\]'


def find_labels_file(directory_location: str) -> List[str]:
    if os.path.isfile(directory_location):
        if is_label_file(directory_location):
            return [directory_location]
        else:
            return []

    list_of_files = list()
    for (dir_path, dir_names, filenames) in os.walk(directory_location):
        if "." in dir_path:
            continue
        for file in filenames:
            if file.split(".")[-1] in allowed_file_extensions:
                file_path = os.path.join(dir_path, file)
                if os.stat(file_path).st_size == 0:
                    continue
                if is_label_file(file_path):
                    list_of_files.append(file_path)

    return list_of_files


def is_label_file(file_location: str) -> bool:
    f = open(file_location, 'r', encoding="utf8")
    text = f.readline()
    has_id = any(character.isdigit() for character in text)
    for text_line in f:
        if has_id != any(character.isdigit() for character in text_line):
            f.close()
            return False
    f.close()
    return True


def find_labels_code(directory_location: str) -> List[str]:
    if os.path.isfile(directory_location):
        if is_code_label_file(directory_location):
            return [directory_location]
        else:
            return []

    list_of_files = list()
    for (dir_path, dir_names, filenames) in os.walk(directory_location):
        if "." in dir_path:
            continue
        for file in filenames:
            if file.split(".")[-1] in allowed_code_extensions:
                file_path = os.path.join(dir_path, file)
                if os.stat(file_path).st_size == 0:
                    continue
                if is_code_label_file(file_path):
                    list_of_files.append(file_path)

    return list_of_files


def is_code_label_file(file_location: str) -> bool:
    f = open(file_location, 'r', encoding="utf8")
    text = f.read()
    f.close()
    if re.search(__pattern, text):
        return True
    return False

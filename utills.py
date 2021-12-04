import re
from bs4 import Tag
from typing import List, Iterator


def extract_first_digit(string: str, default_value: int = 0) -> int:
    if string != "":
        return int(re.findall(f"\\d+", string)[0])
    else:
        return default_value


def extract_text_from_tags(iterator: Iterator[Tag]) -> List[str]:
    return [tag.text for tag in iterator]


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def take_key_by_value(dictionary: dict, value):
    return list(dictionary.keys())[list(dictionary.values()).index(value)]


def first_minus_all(int_list: List[int]):
    last = int_list[0]
    for num in int_list[1:]:
        last -= num
    return last


def make_percentage(mother: int, child: int):
    try:
        return int((child / mother) * 1000) / 10
    except ZeroDivisionError:
        return 0


def put_key_and_value_to_dictionary(dictionary, key, value):
    dictionary[key] = value
    return dictionary


def remove_key(d, key):
    r = dict(d)
    del r[key]
    return r


def list_in_dictionary_key(object_list: list, dictionary: dict):
    for key in dictionary.keys():
        if object_list == key:
            return True
    return False


last_index = (lambda one_list: len(one_list) - 1)

zero_to_one_one_to_zero = (lambda x: 0 if x == 1 else 1)

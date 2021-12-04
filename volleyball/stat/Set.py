# 세트 번호, 포지션
from typing import List
from bs4 import BeautifulSoup, Tag
from utills import extract_text_from_tags
import requests


class Set:

    def __init__(self, position: List[List[str]], liberos: List[List[str]], index: int):
        self.position = position
        self.liberos = liberos
        self.index = index


def make_set(link: str, soup: BeautifulSoup) -> List[Set]:
    set_list: List[Set] = []

    sets_tag: Tag = soup.select("#tab1 > div.wrp_liverecord > div.wrp_tab_set > ul")[0]
    for index, set_tag in enumerate(sets_tag.find_all("li")):
        set_tag: Tag
        if index + 1 != set_tag.find_all("li"):
            new_link: str = link + f"&r_set={index+1}"
            set_html = requests.get(new_link)
            set_soup = BeautifulSoup(set_html.content, "lxml")
        else:
            set_soup = soup
        left_liberos = [text[4:] for text in extract_text_from_tags([tag for tag in set_soup.select("#tab1 > div.position > ul.p_li.li01")[0].find_all("li") if tag.text != "LI: "])]
        right_liberos = [text[4:] for text in extract_text_from_tags([tag for tag in set_soup.select("#tab1 > div.position > ul.p_li.li02")[0].find_all("li") if tag.text != "LI: "])]

        left_position_first = extract_text_from_tags(set_soup.select("#tab1 > div.position > ul.p_left.left01")[0].find_all("li"))
        left_position_second = extract_text_from_tags(set_soup.select("#tab1 > div.position > ul.p_left.left02")[0].find_all("li"))

        right_position_first = extract_text_from_tags(set_soup.select("#tab1 > div.position > ul.p_right.right01")[0].find_all("li"))
        right_position_second = extract_text_from_tags(set_soup.select("#tab1 > div.position > ul.p_right.right02")[0].find_all("li"))

        left_position = [left_position_first[2]] + list(reversed(left_position_second)) + [left_position_first[0], left_position_first[1]]
        right_position = [right_position_second[0]] + right_position_first + [right_position_second[2], right_position_second[1]]

        set_list.append(Set([left_position, right_position], [left_liberos, right_liberos], index))

    return set_list

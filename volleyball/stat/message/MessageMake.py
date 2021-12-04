import requests
from bs4 import BeautifulSoup, Tag
from utills import has_numbers
from variable import *
from volleyball.stat.message import *
from volleyball.stat.message.Messages import Messages


def extract_action_from_text(text: str):
    if len(text.split()) >= 2 and text.split()[1] in action_with_name and has_numbers(text.split()[0]):
        return text.split()[1]
    elif len(text.split()) >= 3 and text.split()[2] in action_with_name and has_numbers(text.split()[0]):
        return text.split()[2]
    elif len(text.split()) >= 2 and text.split()[1] in action_with_name:
        return text
    elif len(text.split()) == 1:
        return text.replace(" ", "")
    else:
        return ""


def make_message_multiple_set(link: str, soup: BeautifulSoup) -> List[List[Messages]]:
    messages_multiple_set: List[List[Messages]] = []
    sets_tag: Tag = soup.select("#tab1 > div.wrp_liverecord > div.wrp_tab_set > ul")[0]
    for index, _ in enumerate(sets_tag.find_all("li")):
        if index + 1 != len(sets_tag.find_all("li")):
            new_link: str = link + f"&r_set={index+1}"
            set_html = requests.get(new_link)
            set_soup = BeautifulSoup(set_html.content, "lxml")
        else:
            set_soup = soup
        teams_messages = make_message(set_soup)
        messages_multiple_set.append([Messages(teams_messages[0]), Messages(teams_messages[1])])
    return messages_multiple_set


def add_error_type(message: Message, text: str):
    try:
        if type(message) != FaultMessage:
            message.error_type = error_to_num[list(filter(lambda error: error in text, error_to_num.keys()))[0]]
            message.success_failure = Message.FAILURE
        return message
    except IndexError:
        return message


def make_message(soup: BeautifulSoup) -> List[List[Message]]:
    messages: List[List[Message]] = [[], []]
    tags = soup.select("#onair_lst > ul")[0].find_all("li")
    for index, tag in enumerate(tags[1:-1]):
        left_text = tag.find_all("span")[0].text
        right_next_text = tags[index + 2].find_all("span")[3].text
        if left_text == "":
            messages[0].append(NoneMessage(index))
        elif left_text == "경고":
            messages[0].append(WarningMessage(index))
        else:
            left_action = extract_action_from_text(left_text)
            if left_action == "팀득점":
                messages[0].append(TeamMessage(index, Message.SUCCESS))
            elif left_action == "팀실패":
                messages[0].append(TeamMessage(index, Message.FAILURE))
            elif left_action not in action_with_name:
                messages[0].append(action_to_class.get(left_action)(index))
            else:
                num_and_name = left_text.split(left_action)[0]
                num = int(num_and_name.split(".")[0])
                name = num_and_name.split(".")[1]
                if name[len(name) - 1] == " ":
                    name = name[:-1]
                if "경고" in left_action:
                    messages[0].append(PersonalWarningMessage(index, num, name))
                elif left_action not in action_with_result:
                    messages[0].append(add_error_type(action_to_class[left_action](index, num, name), left_text))
                else:
                    result: str = left_text.split(left_action)[1]
                    if "정확" in result or "성공" in result:
                        messages[0].append(
                            add_error_type(action_to_class[left_action](index, num, name, Message.SUCCESS), left_text))
                    elif "실패" in result or "블로킹 성공" in right_next_text:
                        messages[0].append(
                            add_error_type(action_to_class[left_action](index, num, name, Message.FAILURE), left_text))
                    else:
                        messages[0].append(
                            add_error_type(action_to_class[left_action](index, num, name, Message.ORDINARY), left_text))

        right_text = tag.find_all("span")[3].text
        left_next_text = tags[index + 2].find_all("span")[0].text
        if right_text == "":
            messages[1].append(NoneMessage(index))
        elif right_text == "경고":
            messages[1].append(WarningMessage(index))
        else:
            right_action = extract_action_from_text(right_text)
            if right_action == "팀득점":
                messages[1].append(TeamMessage(index, Message.SUCCESS))
            elif right_action == "팀실패":
                messages[1].append(TeamMessage(index, Message.FAILURE))
            elif right_action not in action_with_name:
                messages[1].append(action_to_class.get(right_action)(index))
            else:
                num_and_name = right_text.split(right_action)[0]
                num = int(num_and_name.split(".")[0])
                name = num_and_name.split(".")[1]
                if name[len(name) - 1] == " ":
                    name = name[:-1]
                if "경고" in right_text:
                    messages[1].append(PersonalWarningMessage(index, num, name))
                elif right_action not in action_with_result:
                    messages[1].append(add_error_type(action_to_class[right_action](index, num, name), right_text))
                else:
                    result: str = right_text.split(right_action)[1]
                    if "정확" in result or "성공" in result:
                        messages[1].append(
                            add_error_type(action_to_class[right_action](index, num, name, Message.SUCCESS),
                                           right_text))
                    elif "실패" in result or "블로킹 성공" in left_next_text:
                        messages[1].append(
                            add_error_type(action_to_class[right_action](index, num, name, Message.FAILURE),
                                           right_text))
                    else:
                        messages[1].append(
                            add_error_type(action_to_class[right_action](index, num, name, Message.ORDINARY),
                                           right_text))
    return messages

import requests
from bs4 import BeautifulSoup, Tag, ResultSet
from typing import List
import re
from utills import extract_first_digit
from alive_progress import alive_bar


class LinkProcessor:
    MEN = 0
    WOMEN = 1

    REGULAR_SEASON = 0
    PLAY_OFF = 1
    CHAMP = 2
    SEMI_PLAY_OFF = 3

    links: List[str] = []

    def __init__(self, gender: List[int], mod: List[int], years: List[int], nums: List[int]):
        self.gender = gender
        self.mod = mod
        self.years = years
        self.nums = nums

    def make_round_number(self):
        links: List[str] = []
        for year in self.years:
            if year < 2013:
                for month in range(10, 13):
                    links.append(f"https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=00{year-2003}&yymm={year}-{month}&s_part=0&r_round=")
                for month in range(1, 5):
                    links.append(f"https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=00{year-2003}&yymm={year+1}-{'0'+str(month)}&s_part=0&r_round=")
            else:
                for month in range(10, 13):
                    links.append(f"https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=0{year-2003}&yymm={year}-{month}&s_part=0&r_round=")
                for month in range(1, 5):
                    links.append(f"https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=0{year-2003}&yymm={year+1}-{'0'+str(month)}&s_part=0&r_round=")

        print("make link for set")
        with alive_bar(len(links)) as bar:
            for link in links:
                html = requests.get(link)
                soup = BeautifulSoup(html.content, "lxml")
                game_spaces: ResultSet = soup.select("#type1 > div > table > tbody > tr")
                for game_space in game_spaces:
                    try:
                        game_space: Tag
                        if game_space.find_all("td")[2].text == "남자":
                            if self.MEN in self.gender:
                                str_game_num = game_space.find_all("td")[1].text
                                game_num = extract_first_digit(str_game_num)

                                try:
                                    str_game_round = re.findall(f"\d+", game_space.find_all("td")[8].text)[0]
                                    game_round = extract_first_digit(str_game_round)

                                    if self.REGULAR_SEASON in self.mod and game_num in self.nums:
                                        self.links.append(f"https://www.kovo.co.kr/media/popup_result.asp?season={link[68:71]}&g_part=201&r_round={game_round}&g_num={game_num}")
                                except IndexError:
                                    game_round = 1
                                    game_mod: int

                                    if game_space.find_all("td")[8].text == "V리그 준플레이오프":
                                        game_mod = self.SEMI_PLAY_OFF
                                    elif game_space.find_all("td")[8].text == "V리그 플레이오프":
                                        game_mod = self.PLAY_OFF
                                    else:
                                        game_mod = self.CHAMP

                                    if game_mod in self.mod and game_num in self.nums:
                                        self.links.append(f"https://www.kovo.co.kr/media/popup_result.asp?season={link[68:71]}&g_part=20{game_mod+1}&r_round={game_round}&g_num={game_num}")
                        else:
                            if self.WOMEN in self.gender:
                                str_game_num = game_space.find_all("td")[1].text
                                game_num = extract_first_digit(str_game_num)

                                try:
                                    str_game_round = re.findall(f"\d+", game_space.find_all("td")[8].text)[0]
                                    game_round = extract_first_digit(str_game_round)

                                    if self.REGULAR_SEASON in self.mod and game_num in self.nums:
                                        self.links.append(f"https://www.kovo.co.kr/media/popup_result.asp?season={link[68:71]}&g_part=201&r_round={game_round}&g_num={game_num}")
                                except IndexError:
                                    game_round = 1
                                    game_mod: int
                                    if game_space.find_all("td")[8].text == "V리그 플레이오프":
                                        game_mod = self.PLAY_OFF
                                    else:
                                        game_mod = self.CHAMP

                                    if game_mod in self.mod and game_num in self.nums:
                                        self.links.append(f"https://www.kovo.co.kr/media/popup_result.asp?season={link[68:71]}&g_part=20{game_mod+1}&r_round={game_round}&g_num={game_num}")

                    except AttributeError:
                        pass
                    except IndexError:
                        pass
                bar()


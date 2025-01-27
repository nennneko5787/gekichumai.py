import re
from datetime import datetime

import bs4

from .exceptions import *
from .objects import GameData, Cource


class Parser:
    def __init__(self):
        pass

    def login(self, response: str) -> tuple[list[GameData], str]:
        gamedatas: list[GameData] = []
        soup = bs4.BeautifulSoup(response, "html.parser")
        errorBlock = soup.find("div", class_="block text_l")
        if not "Aime選択・利用権設定" in response:
            if errorBlock:
                elements: bs4.element.ResultSet = errorBlock.find_all("p")
                raise LoginFailedException(elements[1].get_text(strip=True))
            else:
                raise LoginFailedException()
        gamedata_list = soup.find("div", class_="mt_10")
        if not gamedata_list:
            raise LoginFailedException()

        for count, gamedata in enumerate(
            gamedata_list.find_all("div", class_="box_playerprofile .clearfix")
        ):
            # icon
            div = gamedata.find("div", "player_chara")
            img = div.find("img")
            if img and "src" in img.attrs:
                player_icon = img["src"]
            else:
                player_icon = None

            # level and name
            div = gamedata.find("div", "player_name")
            player_level: int = int(
                gamedata.find("div", class_="player_lv").get_text(strip=True)
            )
            player_name: str = gamedata.find("div", class_="player_name_in").get_text(
                strip=True
            )

            # rating
            div: bs4.element.NavigableString = gamedata.find(
                "div", "player_rating_num_block"
            )
            rating = []

            for rate in div.contents:
                if rate.name == "img" and "src" in rate.attrs:
                    # rating_ の後の数字を抽出
                    match = re.search(r"rating_\w+_(\d{2})\.png", rate.attrs["src"])
                    if match:
                        rating.append(str(int(match.group(1))))
                elif rate.name == "div" and "player_rating_comma" in rate.get(
                    "class", []
                ):
                    rating.append(".")

            player_rating = float("".join(rating))

            # max rating
            player_max_rating = float(
                gamedata.find("div", class_="player_rating_max").get_text(strip=True)
            )

            # over power
            player_over_power_text: str = gamedata.find(
                "div", class_="player_overpower_text"
            ).get_text(strip=True)
            player_over_power, player_over_power_percentage = (
                player_over_power_text.split("(")
            )
            player_over_power = float(player_over_power)
            player_over_power_percentage: float = float(
                player_over_power_percentage.lstrip("(").rstrip(")").rstrip("%")
            )
            player_lastplaydate: datetime = datetime.strptime(
                gamedata.find("div", class_="player_lastplaydate_text").get_text(
                    strip=True
                ),
                "%Y/%m/%d %H:%M",
            )

            player_honor = (
                gamedata.find("div", class_="player_honor_text")
                .find("span")
                .get_text(strip=True)
            )

            match (
                soup.find("div", class_="aime_charge_block")
                .find("div", class_="aime_charge_course_block")
                .find_all("span", class_="mr_10")[1]
            ):
                case "スタンダードコース":
                    player_cource = Cource.STANDARD
                case "プレミアムコース":
                    player_cource = Cource.PREMIUM
                case _:
                    player_cource = Cource.FREE

            gamedatas.append(
                GameData(
                    index=count,
                    icon=player_icon,
                    honor=player_honor,
                    level=player_level,
                    name=player_name,
                    rating=player_rating,
                    max_rating=player_max_rating,
                    over_power=player_over_power,
                    over_power_percentage=player_over_power_percentage,
                    lastplaydate=player_lastplaydate,
                )
            )

        return gamedatas, player_cource

    def switch_gamedata(self, response: str) -> str:
        soup = bs4.BeautifulSoup(response, "html.parser")
        soup.find("div", class_="avatar_base")

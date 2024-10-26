import re
from datetime import datetime

import bs4

from .exceptions import *
from .http import ChunithmHTTPClient
from .gamedata import GameData
from ..utils import Utils


class Chunithm:
    """チュウニズムを操作できるクラス。"""

    def __init__(self, *, proxy: str = None, proxies: dict = None):
        """ライブラリを初期化します。

        Args:
            proxy (str, optional): 使用するプロキシ(一つ)
            proxies (dict, optional): 使用するプロキシ。スキームごとにプロキシを変更することができます。
        """
        self.csrf = Utils.random_string(32)
        self.http = ChunithmHTTPClient(False, self.csrf, proxy=proxy, proxies=proxies)
        self.gamedata: list[GameData] = []

    def login(self, segaid: str, password: str):
        """チュウニズムネットにログインします。

        Args:
            segaid (str): ログインするユーザーのsegaID。
            password (str): ログインするユーザーのパスワード。
        """
        response = self.http.login(segaid, password)
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

            honor_element = gamedata.find("div", class_="player_honor_text")

            player_honor = honor_element.find("span").get_text(strip=True)

            self.gamedata.append(
                GameData(
                    idx=count,
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

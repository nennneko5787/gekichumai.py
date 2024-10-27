from .exceptions import *
from .http import ChunithmHTTPClient
from .objects import GameData, Cource
from ..utils import Utils
from .parser import Parser


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
        self.parser = Parser()
        self.gamedata: list[GameData] = []
        self.curent_gamedata: GameData = []
        self.cource: Cource = Cource.FREE

    def login(self, segaid: str, password: str):
        """チュウニズムネットにログインします。

        Args:
            segaid (str): ログインするユーザーのsegaID。
            password (str): ログインするユーザーのパスワード。
        """
        response = self.http.login(segaid, password)
        self.gamedata, self.cource = self.parser.login(response)
        return

    def switch_gamedata(self, index: int):
        """ゲームデータを切り替えます。

        Args:
            index (int): ゲームデータのインデックス。self.gamedataから確認することができます。
        """
        self.curent_gamedata = self.gamedata[index]
        response = self.http.switch_gamedata(index)
        self.parser.switch_gamedata(response)

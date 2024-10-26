import asyncio
from typing import Callable, Union

import httpx

from .exceptions import *


class ChunithmHTTPClient:
    def __init__(
        self, is_async: bool, csrf: str, *, proxy: str = None, proxies: dict = None
    ):
        """チュウニズムNET用のHTTPライブラリを初期化します。

        Args:
            is_async (bool): リクエストにasyncioを使用するかどうか。
            csrf (str): チュウニズムNETで使用するCSRFトークン。
            proxy (str, optional): 使用するプロキシ(一つ)
            proxies (dict, optional): 使用するプロキシ。スキームごとにプロキシを変更することができます。
        """
        self.csrf: str = csrf
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        }

        self.is_async = is_async
        if self.is_async:
            self.http = httpx.AsyncClient(
                headers=self.headers,
                cookies={"_t": self.csrf},
                proxy=proxy,
                proxies=proxies,
            )
        else:
            self.http = httpx.Client(
                headers=self.headers,
                cookies={"_t": self.csrf},
                proxy=proxy,
                proxies=proxies,
            )

    async def _async_login(self, segaid: str, password: str) -> str:
        response = await self.http.post(
            "https://new.chunithm-net.com/chuni-mobile/html/mobile/submit/",
            data={
                "segaId": segaid,
                "password": password,
                "save_cookie": "save_cookie",
                "token": self.csrf,
            },
            follow_redirects=True,
        )
        return response.text

    def _sync_login(self, segaid: str, password: str) -> str:
        response = self.http.post(
            "https://new.chunithm-net.com/chuni-mobile/html/mobile/submit/",
            data={
                "segaId": segaid,
                "password": password,
                "save_cookie": "save_cookie",
                "token": self.csrf,
            },
            follow_redirects=True,
        )
        return response.text

    def login(
        self, segaid: str, password: str
    ) -> Callable[..., Union[str, asyncio.Future[str]]]:
        if self.is_async:
            return self._async_login(segaid, password)
        else:
            return self._sync_login(segaid, password)

import asyncio
from typing import (
    Literal,
    Optional
)
from aiohttp import ClientSession

from .modules.stocks import Stocks
from .modules.product import Product
from .modules.posting import Posting
from .exceptions.api import ApiError

class OzonClient:
    """
    Основной клиент для управления OZON API.

    :param api_key: str - API ключ от OZON Seller
    :param client_id: str - Client Id от OZON Seller
    :param base_url: str - Основная ссылка для API запросов
    :param locale: "RU" | "EN" - Язык ответов
    """
    def __init__(
            self,
            api_key: str,
            client_id: str,
            base_url: str = "https://api-seller.ozon.ru/",
            locale: Literal["RU", "EN"] = "RU"
    ):
        self.api_key = api_key
        self.client_id = client_id
        self.headers = {
            "Client-Id": self.client_id,
            "Api-Key": self.api_key
        }
        self.base_url = base_url
        self.locale = locale
        self.stocks = Stocks(self)
        self.product = Product(self)
        self.warehouse = None
        self.posting = Posting(self)

    async def fetch(
            self,
            method: Literal["get", "post", "put"],
            endpoint: str,
            wait: bool = False,
            time: Optional[int] = None,
            **kwargs
    ):
        async with ClientSession(headers=self.headers, base_url=self.base_url) as session:
            session_method = getattr(session, method.lower(), None)

            if session_method is None:
                raise ValueError(f"HTTP метод {method.lower()} не поддерживается."
                                 if self.locale == "RU" else
                                 f"HTTP method {method.lower()} is not supported.")

            async with session_method(url=endpoint, **kwargs) as response:
                data = await response.json()

            if response.status != 200:

                if wait and (time is not None) and (response.status == 999):
                    await asyncio.sleep(time)
                    return await self.fetch(method, endpoint, wait, time, **kwargs)

                raise ApiError(response.status, data, self.locale)

            return data

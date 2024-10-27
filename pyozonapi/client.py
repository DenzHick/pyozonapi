import asyncio
from typing import (
    Literal,
    Optional,
    Dict,
    Callable
)
from aiohttp import ClientSession
from aiohttp import web

from .modules.stocks import Stocks
from .modules.product import Product
from .modules.posting import Posting
from .exceptions.api import ApiError
from .models.push import OzonPushEvent


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
        self.api_key: str = api_key
        self.client_id: str = client_id
        self.headers: Dict[str, str] = {
            "Client-Id": self.client_id,
            "Api-Key": self.api_key
        }
        self.base_url: str = base_url
        self.locale: Literal["RU", "EN"] = locale
        self.stocks: Stocks = Stocks(self)
        self.product: Product = Product(self)
        self.warehouse = None
        self.posting: Posting = Posting(self)
        self.push = None # Включение, выключение, изменение push-уведомлений. Спросить как это сделать у ChatGPT

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


class OzonPushClient:

    def __init__(
            self,
            host: str = '0.0.0.0',
            port: int  = 8080,
            webhook_path: str = "/ozon/push"
    ):
        """
        :param host: Хост, на котором будет запущен сервер.
        :param port: Порт, на котором будет запущен сервер.
        :param webhook_path: Путь, на который будут приходить уведомления.
        """
        self.host: str = host
        self.port: int = port
        self.webhook_path: str = webhook_path
        self.app = web.Application()
        self.app.router.add_post(self.webhook_path, self._handle_push)
        self._on_event: Optional[Callable[[OzonPushEvent], None]] = None

    def on_event(self, callback: Callable[[OzonPushEvent], None]):
        """
        Устанавливает функцию обратного вызова для обработки событий.
        """
        self._on_event = callback

    async def _handle_push(self, request: web.Request):
        """
        Обрабатывает входящие push-уведомления от Ozon Seller API.
        """
        try:
            data = await request.json()
            event = OzonPushEvent(**data)

            if self._on_event:
                await self._on_event(event)

            return web.Response(body={"result": True}, status=200)
        except Exception:
            return web.Response(body={
                "error": {
                    "code": "ERROR_UNKNOWN",
                    "message": "ошибка",
                    "details": None
                }
            }, status=400)

    async def start(self):
        """
        Запускает сервер для приема уведомлений.
        """
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        print(f"Server started at http://{self.host}:{self.port}{self.webhook_path}")

    async def stop(self):
        """
        Останавливает сервер.
        """
        await self.app.shutdown()
        await self.app.cleanup()

from typing import (
    Optional,
    List
)

from .tools import list_division

from ..client import (
    OzonClient
)
from ..models.stocks import (
    StocksResponse,
    StocksResponseFBS,
    StocksUpdateParams,
    StocksUpdateResponse
)

from ..models.product import (
    ProductInfoResponse
)

from ..modules.tools import ttl_cache

from ..exceptions.params import (
    ParamLimitError
)


class Stocks:
    """
    Модули для работы с остатками товаров
    """
    def __init__(self, client: OzonClient):
        self._client = client

    @ttl_cache
    async def get(self, limit: Optional[int] = None, wait: bool = True) -> StocksResponse:
        """
        Возвращает информацию о количестве товаров на складах FBS и FBO.

        :param limit: Int > 0 - Количество товаров для получения. Если значение больше количества всех товаров или не указано, то выведет их максимальное количество.
        :param wait: Bool - Ждать при достижении лимита на запросы.

        :return: StocksResponse
        """

        if limit <= 0:
            raise ParamLimitError(self._client.locale)

        MAX_LIMIT = 1000
        last_id = ''
        stocks = []

        while True:

            body = {
                "filter": {},
                "last_id": last_id,
                "limit": min(MAX_LIMIT, limit - len(stocks)) if limit is not None else MAX_LIMIT
            }

            data = await self._client.fetch('post', 'v3/product/info/stocks', wait=wait, time=60, json=body)

            stocks.extend(data["result"]["items"])

            if (body["limit"] < MAX_LIMIT) or (data["result"]["total"] < body["limit"]) or (len(stocks) >= limit):
                break

            last_id = data["result"]["last_id"]

        return StocksResponse.from_response(stocks)

    @ttl_cache
    async def get_fbs(self, product_info: ProductInfoResponse, wait: bool = True) -> StocksResponseFBS:
        """
        Возвращает информацию о количестве товаров на каждом складе FBS.

        :param product_info: ProductInfoResponse - Вывод OzonClient.product.get_info с запроса на v2/product/info/list.
        :param wait: Bool - Ждать при достижении лимита на запросы.

        :return: StocksResponseFBS
        """

        skus: List[List[int | str]] = [[offer.sku, offer.id] for offer in product_info.offers if offer.sku]

        MAX_LIMIT = 500
        stocks = []

        for param_skus in list_division(skus, MAX_LIMIT):
            body = {
                "sku": [item[0] for item in param_skus]
            }

            data = await self._client.fetch('post', 'v1/product/info/stocks-by-warehouse/fbs', wait=wait, time=60, json=body)

            changed_data = []
            for data_item in data["result"]:
                for sku_item in param_skus:
                    if sku_item[0] == data_item["sku"]:
                        data_item["id"] = sku_item[1]
                        changed_data.append(data_item)
                        break

            stocks.extend(changed_data)

        return StocksResponseFBS.from_response(stocks)

    async def update(self, update_params: List[StocksUpdateParams], wait: bool = True) -> StocksUpdateResponse:
        """
        Обновляет остатки товаров.

        :param update_params: List[StocksUpdateParams] - Информация о товарах на складах.
        :param wait: Bool - Ждать при достижении лимита на запросы.

        :return: StocksUpdateResponse
        """

        MAX_LIMIT = 100
        updates = []

        for params in list_division(update_params, MAX_LIMIT):
            body = {
                "stocks": params
            }

            data = await self._client.fetch('post', 'v2/products/stocks', wait=wait, time=60, json=body)

            updates.extend(data["result"])

        return StocksUpdateResponse.from_response(updates)

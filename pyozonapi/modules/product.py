from typing import (
    Optional,
    List
)

from ..client import (
    OzonClient
)

from ..exceptions.params import (
    ParamLimitError
)

from ..models.product import (
    ProductListResponse,
    ProductInfoResponse
)

from ..types import Info_Statuses
from ..modules.tools import list_division

class Product:
    """
    Модули для работы с товарами
    """
    def __init__(self, client: OzonClient):
        self._client = client

    async def get_list(
            self,
            status: Info_Statuses = "ALL",
            limit: Optional[int] = None,
            wait: bool = True
    ) -> ProductListResponse:
        """
        Возвращает список товаров.

        :param status: Str - Статус видимости товара.
        :param limit: Int > 0 - Количество товаров для получения. Если значение больше количества всех товаров или не указано, то выведет их максимальное количество.
        :param wait: Bool - Ждать при достижении лимита на запросы.

        :return: ProductListResponse
        """

        if limit <= 0:
            raise ParamLimitError(self._client.locale)

        MAX_LIMIT = 1000
        last_id = ''
        products = []

        while True:

            body = {
                "filter": {
                    "visibility": status,
                },
                "last_id": last_id,
                "limit": min(MAX_LIMIT, limit - len(products)) if limit is not None else MAX_LIMIT
            }

            data = await self._client.fetch('post', 'v2/product/list', wait=wait, time=60, json=body)

            products.extend(data["result"]["items"])

            if (body["limit"] < MAX_LIMIT) or (data["result"]["total"] < body["limit"]) or (len(products) >= limit):
                break

            last_id = data["result"]["last_id"]

        return ProductListResponse(products, self._client.locale)

    async def get_info(self, product_list: ProductListResponse, wait: bool = True) -> ProductInfoResponse:
        """
        Возвращает список товаров.

        :param product_list: ProductListResponse - Вывод OzonClient.product.get_list с запроса на v2/product/list.
        :param wait: Bool - Ждать при достижении лимита на запросы.

        :return: ProductListResponse
        """
        offer_ids: List[str] = [offer.id for offer in product_list.offers]

        MAX_LIMIT = 1000
        products = []

        for param_offer_ids in list_division(offer_ids, MAX_LIMIT):

            body = {
                "offer_id": param_offer_ids,
                "product_id": [],
                "sku": []
            }

            data = await self._client.fetch('post', 'v2/product/info/list', wait=wait, time=60, json=body)

            products.extend(data["result"]["items"])

        return ProductInfoResponse(products, self._client.locale)

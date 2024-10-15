from typing import Optional

from ..client import (
    OzonClient
)

from ..types import (
    Posting_Statuses
)

from ..exceptions.params import (
    ParamLimitError
)

from ..models.posting import PostingUnfulfilledResponse

from datetime import datetime

class Posting:
    """
    Модули для работы с поставками и заказами
    """
    def __init__(self, client: OzonClient):
        self._client = client

    async def get_unfulfilled_list(
            self,
            status: Posting_Statuses,
            cutoff_from: datetime,
            cutoff_to: datetime,
            limit: Optional[int] = None,
            reverse: bool = False,
            wait: bool = True
    ) -> PostingUnfulfilledResponse:
        """
        Возвращает список необработанных отправлений.

        :param status: Posting_Statuses - статус отправления.
        :param cutoff_from: Datetime - Фильтр по времени, до которого продавцу нужно собрать заказ. Начало периода.
        :param cutoff_to: Datetime - Фильтр по времени, до которого продавцу нужно собрать заказ. Конец периода.
        :param reverse: Bool - Получить ответ с обратной сортировкой.
        :param limit: Int > 0 - Количество товаров для получения. Если значение больше количества всех товаров или не указано, то выведет их максимальное количество.
        :param wait: Bool - Ждать при достижении лимита на запросы.

        :return: PostingUnfulfilledResponse
        """
        if limit <= 0:
            raise ParamLimitError(self._client.locale)

        MAX_LIMIT = 1000
        postings = []

        while True:
            body = {
                "dir": "DESC" if reverse else "ASC",
                "filter": {
                    "cutoff_from": cutoff_from.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "cutoff_to": cutoff_to.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "status": status,
                },
                "limit": min(MAX_LIMIT, limit - len(postings)) if limit is not None else MAX_LIMIT,
                "offset": len(postings),
                "with": {
                    "analytics_data": True,
                    "barcodes": True,
                    "financial_data": True,
                    "translit": True
                }
            }

            data = await self._client.fetch('post', 'v3/posting/fbs/unfulfilled/list', wait=wait, time=60, json=body)

            postings.extend(data["result"]["postings"])

            if (body["limit"] < MAX_LIMIT) or (data["result"]["count"] < body["limit"]) or (len(postings) >= limit):
                break

        return PostingUnfulfilledResponse(postings, self._client.locale)

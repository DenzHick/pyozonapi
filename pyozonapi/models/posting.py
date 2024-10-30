from pydantic import BaseModel, Field
from typing import (
    List,
    Dict,
    Any
)
from .base import BaseResponse
from ..types import (
    Posting_Statuses,
    Posting_SubStatuses
)


class PostingUnfulfilledResponse(BaseModel):
    """
    Модель ответа OzonClient.posting.get_unfulfilled_list

    :param postings: dict - json ответ от API на v3/posting/fbs/unfulfilled/list.
    :param locale: "RU" | "EN" - Язык ответов.
    """

    class Order(BaseResponse):

        class Offer(BaseResponse):

            id: str = Field(alias='offer_id')
            sku: int
            quantity: int
            name: str

        id: int = Field(alias='order_id')
        number: str = Field(alias='order_number')
        offers: List[Offer] = Field(alias='products')
        posting_number: str
        status: Posting_Statuses
        substatus: Posting_SubStatuses

    orders: List[Order]

    @classmethod
    def from_response(cls, response: List[Dict[str, Any]]) -> "PostingUnfulfilledResponse":
        orders = [cls.Order(**order) for order in response]
        return cls(orders=orders)

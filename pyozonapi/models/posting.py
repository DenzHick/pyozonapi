from pydantic import BaseModel, Field
from typing import (
    List,
    Dict,
    Any
)

from ..types import (
    Posting_Statuses,
    Posting_SubStatuses
)


class PostingUnfulfilledOffer(BaseModel):

    id: str = Field(alias='offer_id')
    sku: int
    quantity: int
    name: str

    class Config:
        extra = 'allow'


class PostingUnfulfilledOrder(BaseModel):

    id: int = Field(alias='order_id')
    number: str = Field(alias='order_number')
    offers: List[PostingUnfulfilledOffer] = Field(alias='products')
    posting_number: str
    status: Posting_Statuses
    substatus: Posting_SubStatuses

    class Config:
        extra = 'allow'


class PostingUnfulfilledResponse(BaseModel):
    """
    Модель ответа OzonClient.posting.get_unfulfilled_list

    :param postings: dict - json ответ от API на v3/posting/fbs/unfulfilled/list.
    :param locale: "RU" | "EN" - Язык ответов.
    """

    orders: List[PostingUnfulfilledOrder]

    @classmethod
    def from_response(cls, response: List[Dict[str, Any]]) -> "PostingUnfulfilledResponse":
        orders = [PostingUnfulfilledOrder(**order) for order in response]
        return cls(orders=orders)

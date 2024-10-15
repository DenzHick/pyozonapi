from typing import (
    List,
    Dict,
    Any,
    Literal
)

from ..types import (
    Posting_Statuses,
    Posting_SubStatuses
)

from ..modules.tools import add_values

class PostingUnfulfilledResponse:
    """
    Модель ответа OzonClient.posting.get_unfulfilled_list

    :param postings: dict - json ответ от API на v3/posting/fbs/unfulfilled/list.
    :param locale: "RU" | "EN" - Язык ответов.
    """
    def __init__(
            self,
            postings: List[Dict[str, Any]],
            locale: Literal["RU", "EN"] = "RU"
    ):
        try:
            self.orders: List[PostingUnfulfilledOrder] = [PostingUnfulfilledOrder(order) for order in postings]
        except KeyError:
            raise ValueError("Передан неверный массив данных."
                             if locale == "RU" else
                             "Incorrect data was transmitted.")

class PostingUnfulfilledOrder:

    def __init__(
            self,
            order: Dict[str, Any]
    ):
        self.id: int = order["order_id"]
        self.number: str = order["order_number"]
        self.posting_number: str = order["posting_number"]
        self.status: Posting_Statuses = order["status"]
        self.substatus: Posting_SubStatuses = order["substatus"]
        self.offers: List[PostingUnfulfilledOffer] = [PostingUnfulfilledOffer(offer) for offer in order["products"]]
        add_values(self, order, ["order_id", "order_number", "products"])

class PostingUnfulfilledOffer:

    def __init__(
            self,
            offer: Dict[str, Any]
    ):
        self.id: str = offer["offer_id"]
        self.sku: int = offer["sku"]
        self.quantity: int = offer["quantity"]
        self.name: str = offer["name"]
        add_values(self, offer, ["offer_id"])

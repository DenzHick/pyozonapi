from typing import (
    Literal,
    List,
    Dict,
    Union,
    Any
)

from ..types import Currency_Codes

from ..modules.tools import add_values

class ProductListResponse:
    """
    Модель ответа OzonClient.product.get_list

    :param products: dict - json ответ от API на v2/product/list.
    :param locale: "RU" | "EN" - Язык ответов.
    """
    def __init__(
            self,
            products: List[Dict[str, Union[int, str]]],
            locale: Literal["RU", "EN"] = "RU"
    ):
        try:
            self.offers: List[ProductListOffer] = [ProductListOffer(offer) for offer in products]
        except KeyError:
            raise ValueError("Передан неверный массив данных."
                             if locale == "RU" else
                             "Incorrect data was transmitted.")


class ProductListOffer:

    def __init__(
            self,
            offer: Dict[str, Union[int, str]]
    ):
        self.id: str = offer["offer_id"]
        self.product_id: int = offer["product_id"]


class ProductInfoResponse:
    """
    Модель ответа OzonClient.product.get_info

    :param products: dict - json ответ от API на v2/product/info/list.
    :param locale: "RU" | "EN" - Язык ответов.
    """
    def __init__(
            self,
            products: List[Dict[str, Any]],
            locale: Literal["RU", "EN"] = "RU"
    ):
        try:
            self.offers: List[ProductInfoOffer] = [ProductInfoOffer(offer) for offer in products]
        except KeyError:
            raise ValueError("Передан неверный массив данных."
                             if locale == "RU" else
                             "Incorrect data was transmitted.")


class ProductInfoOffer:

    def __init__(
            self,
            offer: Dict[str, Any]
    ):
        self.id: str = offer["offer_id"]
        self.product_id: int = offer["id"]
        self.sku: int = offer["sku"]
        self.name: str = offer["name"]
        self.is_archived: bool = offer["is_archived"]
        self.stocks: ProductStocks = ProductStocks(offer["stocks"])
        self.discounted_stocks: ProductStocks = ProductStocks(offer["discounted_stocks"])
        self.visibility_details: ProductVisibilityDetails = ProductVisibilityDetails(offer["visibility_details"])
        self.visible: bool = offer["visible"]
        add_values(self, offer, ["offer_id", "id"])

class ProductStocks:

    def __init__(
            self,
            stocks: Dict[str, Any]
    ):
        self.coming: int = stocks["coming"]
        self.present: int = stocks["present"]
        self.reserved: int = stocks["reserved"]
        add_values(self, stocks)

class ProductVisibilityDetails:

    def __init__(
            self,
            visibility_details: Dict[str, Any]
    ):
        self.active_product = visibility_details["active_product"]
        self.has_price = visibility_details["has_price"]
        self.has_stock = visibility_details["has_stock"]
        self.reasons = visibility_details["reasons"]
        add_values(self, visibility_details)

from typing import (
    Literal,
    List,
    Dict,
    Union,
    Any,
    TypedDict
)


class StocksResponse:
    """
    Модель ответа OzonClient.stocks.get

    :param stocks: dict - json ответ от API на v3/product/info/stocks.
    :param locale: "RU" | "EN" - Язык ответов.
    """
    def __init__(
            self,
            stocks: List[Dict[str, Union[int, str, List[Dict[str, Union[str, int]]]]]],
            locale: Literal["RU", "EN"] = "RU"
    ):
        try:
            self.offers: List[StocksOffer] = [StocksOffer(offer) for offer in stocks]
        except KeyError:
            raise ValueError("Передан неверный массив данных."
                             if locale == "RU" else
                             "Incorrect data was transmitted.")


class StocksOffer:

    def __init__(
            self,
            offer: Dict[str, Union[int, str, List[Dict[str, Union[str, int]]]]]
    ):
        self.id: str = offer["offer_id"]
        self.product_id: int = offer["product_id"]
        self.fbs: StocksType = StocksType([item for item in offer["stocks"] if item["type"] == "fbs"][0])
        self.fbo: StocksType = StocksType([item for item in offer["stocks"] if item["type"] == "fbo"][0])


class StocksType:

    def __init__(
            self,
            stocks_type: Dict[str, Any]
    ):
        self.quantity: int = stocks_type["present"]
        self.reserve: int = stocks_type["reserved"]


class StocksResponseFBS:
    """
    Модель ответа OzonClient.stocks.get_fbs

    :param stocks: dict - json ответ от API на v1/product/info/stocks-by-warehouse/fbs.
    :param locale: "RU" | "EN" - Язык ответов.
    """
    def __init__(
            self,
            stocks: List[Dict[str, Any]],
            locale: Literal["RU", "EN"] = "RU"
    ):
        try:
            self.offers: List[StocksOfferFBS] = [StocksOfferFBS(offer) for offer in stocks]
        except KeyError:
            raise ValueError("Передан неверный массив данных."
                             if locale == "RU" else
                             "Incorrect data was transmitted.")


class StocksOfferFBS:

    def __init__(self, offer: Dict[str, Any]):
        self.id: str = offer["id"]
        self.sku: int = offer["sku"]
        self.product_id: int = offer["product_id"]
        self.quantity: int = offer["present"]
        self.reserve: int = offer["reserved"]
        self.warehouse_id: int = offer["warehouse_id"]
        self.warehouse_name: str = offer["warehouse_name"]

class StocksUpdateParams(TypedDict):
    """
    offer_id - Артикул товара \n
    product_id - ID товара \n
    stock - Новый остаток товара с учетом резервов \n
    warehouse_id - ID склада FBS
    """

    offer_id: str
    product_id: int
    stock: int
    warehouse_id: int

class StocksUpdateResponse:
    """
    Модель ответа OzonClient.stocks.update

    :param updates: dict - json запрос.
    :param locale: "RU" | "EN" - Язык ответов.
    """
    def __init__(
            self,
            updates: List[Dict[str, Any]],
            locale: Literal["RU", "EN"] = "RU"
    ):
        try:
            self.offers: List[StocksUpdateOffer] = [StocksUpdateOffer(offer) for offer in updates]
        except KeyError:
            raise ValueError("Передан неверный массив данных."
                             if locale == "RU" else
                             "Incorrect data was transmitted.")

class StocksUpdateOffer:

    def __init__(
            self,
            offer: Dict[str, Any]
    ):
        self.id: str = offer["offer_id"]
        self.product_id: int = offer["product_id"]
        self.warehouse_id: int = offer["warehouse_id"]
        self.updated: bool = offer["updated"]
        self.errors: list = offer["errors"]

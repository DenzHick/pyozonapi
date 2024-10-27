from pydantic import BaseModel, Field
from typing import (
    List,
    Dict,
    Any
)


class StocksType(BaseModel):

    quantity: int = Field(alias='present')
    reserve: int = Field(alias='reserved')

    class Config:
        extra = 'allow'

class StocksOffer(BaseModel):

    id: str = Field(alias='offer_id')
    product_id: int
    fbs: StocksType
    fbo: StocksType

    class Config:
        extra = 'allow'

    @classmethod
    def from_response(cls, response: Dict[str, Any]) -> "StocksOffer":
        fbs = next((item for item in response['stocks'] if item['type'] == 'fbs'), None)
        fbo = next((item for item in response['stocks'] if item['type'] == 'fbo'), None)
        return cls(fbs=fbs, fbo=fbo, **(response.pop('stocks', response)))

class StocksResponse(BaseModel):
    """
    Модель ответа OzonClient.stocks.get

    :param stocks: dict - json ответ от API на v3/product/info/stocks.
    :param locale: "RU" | "EN" - Язык ответов.
    """

    offers: List[StocksOffer]

    @classmethod
    def from_response(cls, response: List[Dict[str, Any]]) -> "StocksResponse":
        offers = [StocksOffer.from_response(offer) for offer in response]
        return cls(offers=offers)


class StocksOfferFBS(BaseModel):

    id: str = Field(alias='offer_id')
    sku: int
    product_id: int
    quantity: int = Field(alias='present')
    reserve: int = Field(alias='reserved')
    warehouse_id: int
    warehouse_name: str

    class Config:
        extra = 'allow'


class StocksResponseFBS(BaseModel):
    """
    Модель ответа OzonClient.stocks.get_fbs

    :param stocks: dict - json ответ от API на v1/product/info/stocks-by-warehouse/fbs.
    :param locale: "RU" | "EN" - Язык ответов.
    """

    offers: List[StocksOfferFBS]

    @classmethod
    def from_response(cls, response: List[Dict[str, Any]]) -> "StocksResponseFBS":
        offers = [StocksOfferFBS(**offer) for offer in response]
        return cls(offers=offers)


class StocksUpdateParams(BaseModel):
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


class StocksUpdateOffer(BaseModel):

    id: str = Field(alias='offer_id')
    product_id: int
    warehouse_id: int
    updated: bool
    errors: list

    class Config:
        extra = 'allow'


class StocksUpdateResponse(BaseModel):
    """
        Модель ответа OzonClient.stocks.update

        :param updates: dict - json запрос.
        :param locale: "RU" | "EN" - Язык ответов.
    """

    offers: List[StocksUpdateOffer]

    @classmethod
    def from_response(cls, response: List[Dict[str, Any]]) -> "StocksUpdateResponse":
        offers = [StocksUpdateOffer(**offer) for offer in response]
        return cls(offers=offers)

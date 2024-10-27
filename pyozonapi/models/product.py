from pydantic import BaseModel, Field
from typing import (
    List,
    Dict,
    Any
)


class ProductListOffer(BaseModel):

    id: str = Field(alias='offer_id')
    product_id: int

    class Config:
        extra = 'allow'


class ProductListResponse(BaseModel):
    """
    Модель ответа OzonClient.product.get_list

    :param products: dict - json ответ от API на v2/product/list.
    :param locale: "RU" | "EN" - Язык ответов.
    """

    offers: List[ProductListOffer]

    @classmethod
    def from_response(cls, response: List[Dict[str, Any]]) -> "ProductListResponse":
        offers = [ProductListOffer(**offer) for offer in response]
        return cls(offers=offers)


class ProductStocks(BaseModel):

    quantity: int = Field(alias='present')
    reserve: int = Field(alias='reserved')
    coming: int

    class Config:
        extra = 'allow'


class ProductVisibilityDetails(BaseModel):

    active_product: bool
    has_price: bool
    has_stock: bool
    reasons: dict

    class Config:
        extra = 'allow'


class ProductInfoOffer(BaseModel):

    id: str = Field(alias='offer_id')
    product_id: int
    sku: int
    name: str
    is_archived: bool
    visible: bool
    stocks: ProductStocks
    discounted_stocks: ProductStocks
    visibility_details: ProductVisibilityDetails

    class Config:
        extra = 'allow'


class ProductInfoResponse(BaseModel):
    """
    Модель ответа OzonClient.product.get_info

    :param products: dict - json ответ от API на v2/product/info/list.
    :param locale: "RU" | "EN" - Язык ответов.
    """

    offers: List[ProductInfoOffer]

    @classmethod
    def from_response(cls, response: List[Dict[str, Any]]) -> "ProductInfoResponse":
        offers = [ProductInfoOffer(**offer) for offer in response]
        return cls(offers=offers)

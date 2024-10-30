from pydantic import BaseModel, Field
from typing import (
    List,
    Dict,
    Any
)
from .base import BaseResponse


class ProductListResponse(BaseModel):
    """
    Модель ответа OzonClient.product.get_list

    :param products: dict - json ответ от API на v2/product/list.
    :param locale: "RU" | "EN" - Язык ответов.
    """

    class Offer(BaseResponse):

        id: str = Field(alias='offer_id')
        product_id: int

    offers: List[Offer]

    @classmethod
    def from_response(cls, response: List[Dict[str, Any]]) -> "ProductListResponse":
        offers = [cls.Offer(**offer) for offer in response]
        return cls(offers=offers)


class ProductInfoResponse(BaseModel):
    """
    Модель ответа OzonClient.product.get_info

    :param products: dict - json ответ от API на v2/product/info/list.
    :param locale: "RU" | "EN" - Язык ответов.
    """

    class Offer(BaseResponse):

        class Stocks(BaseResponse):

            quantity: int = Field(alias='present')
            reserve: int = Field(alias='reserved')
            coming: int

        class VisibilityDetails(BaseResponse):

            active_product: bool
            has_price: bool
            has_stock: bool
            reasons: dict

        id: str = Field(alias='offer_id')
        product_id: int
        sku: int
        name: str
        is_archived: bool
        visible: bool
        stocks: Stocks
        discounted_stocks: Stocks
        visibility_details: VisibilityDetails

    offers: List[Offer]

    @classmethod
    def from_response(cls, response: List[Dict[str, Any]]) -> "ProductInfoResponse":
        offers = [cls.Offer(**offer) for offer in response]
        return cls(offers=offers)

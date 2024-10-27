from pydantic import BaseModel, Field, field_validator
from typing import (
    Literal,
    List
)
from datetime import datetime

class OzonPushEvent(BaseModel):
    """
    Модель push-уведомления от Ozon Seller API.
    """
    message_type: str

    class Config:
        extra = 'allow'


class OzonPushProduct(BaseModel):
    sku: int
    quantity: int

    class Config:
        extra = 'allow'


class OzonPushNewPosting(OzonPushEvent):
    message_type: Literal["TYPE_NEW_POSTING"]
    posting_number: str
    products: List[OzonPushProduct]
    in_process_at: datetime
    warehouse_id: int
    seller_id: int

    @field_validator('in_process_at', mode='before')
    def parse_in_process_at(cls, value):
        if isinstance(value, str):
            value = value.replace('Z', '+00:00')
            return datetime.fromisoformat(value)
        return value

    class Config:
        extra = 'allow'


class OzonPushPostingCancelledReason(BaseModel):
    id: int
    message: str

    class Config:
        extra = 'allow'


class OzonPushPostingCancelled(OzonPushEvent):
    message_type: Literal["TYPE_POSTING_CANCELLED"]
    posting_number: str
    products: List[OzonPushProduct]
    old_state: str
    new_state: str
    changed_state_date: datetime
    reason: OzonPushPostingCancelledReason
    warehouse_id: int
    seller_id: int

    @field_validator('changed_state_date', mode='before')
    def parse_changed_state_date(cls, value):
        if isinstance(value, str):
            value = value.replace('Z', '+00:00')
            return datetime.fromisoformat(value)
        return value

    class Config:
        extra = 'allow'


class OzonPushStateChanged(OzonPushEvent):
    message_type: Literal["TYPE_STATE_CHANGED"]
    posting_number: str
    new_state: str
    changed_state_date: datetime
    warehouse_id: int
    seller_id: int

    @field_validator('changed_state_date', mode='before')
    def parse_changed_state_date(cls, value):
        if isinstance(value, str):
            value = value.replace('Z', '+00:00')
            return datetime.fromisoformat(value)
        return value

    class Config:
        extra = 'allow'

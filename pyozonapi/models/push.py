from pydantic import BaseModel, field_validator
from typing import (
    Literal,
    List
)
from .base import (
    BaseResponse,
    BasePushEvent
)
from datetime import datetime


class PushProduct(BaseResponse):

    sku: int
    quantity: int


class PushNewPosting(BasePushEvent):

    message_type: Literal["TYPE_NEW_POSTING"]
    posting_number: str
    products: List[PushProduct]
    in_process_at: datetime
    warehouse_id: int
    seller_id: int

    @field_validator('in_process_at', mode='before')
    def parse_in_process_at(cls, value):
        if isinstance(value, str):
            value = value.replace('Z', '+00:00')
            return datetime.fromisoformat(value)
        return value


class PushPostingCancelled(BasePushEvent):

    class Reason(BaseResponse):

        id: int
        message: str

    message_type: Literal["TYPE_POSTING_CANCELLED"]
    posting_number: str
    products: List[PushProduct]
    old_state: str
    new_state: str
    changed_state_date: datetime
    reason: Reason
    warehouse_id: int
    seller_id: int

    @field_validator('changed_state_date', mode='before')
    def parse_changed_state_date(cls, value):
        if isinstance(value, str):
            value = value.replace('Z', '+00:00')
            return datetime.fromisoformat(value)
        return value


class PushStateChanged(BasePushEvent):

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

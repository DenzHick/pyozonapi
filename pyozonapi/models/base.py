from pydantic import BaseModel


class BaseResponse(BaseModel):

    class Config:
        extra = 'allow'
        allow_mutation = False


class BasePushEvent(BaseModel):

    message_type: str

    class Config:
        extra = 'allow'
        allow_mutation = False

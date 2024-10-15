from typing import (
    Literal
)

class ApiError(Exception):

    messages = {
        "": ""
    }

    def __init__(self, status: int, data: dict, locale: Literal["RU", "EN"]):
        self.status = status
        self.code = data.get('code')
        self.details = data.get('details')
        self.message = self.messages[locale].get(status) if status in self.messages[locale] else self.messages[locale][0]
        super().__init__(f"{'Статус' if locale == 'RU' else 'Status'}: {self.status}; {self.message}; "
                         f"{'Детали' if locale == 'RU' else 'Details'}: {self.details}")

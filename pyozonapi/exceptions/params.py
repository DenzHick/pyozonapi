from typing import (
    Literal
)

class ParamLimitError(Exception):

    def __init__(self, locale: Literal["RU", "EN"]):
        super().__init__(
            "Параметр limit должен быть больше 0!"
            if locale == "RU" else
            "limit parameter must be greater than 0!"
        )

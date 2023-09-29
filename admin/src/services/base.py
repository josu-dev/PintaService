from typing import Any, Dict, TypedDict


class BaseService:
    ...


class BaseServiceError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def filter_nones(kwargs: TypedDict) -> Dict[str, Any]:
    return {key: value for key, value in kwargs.items() if value is not None}

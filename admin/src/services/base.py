from typing import Any, Dict, TypedDict


class BaseService:
    ...


class BaseServiceError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

import functools
from enum import Enum
from typing import Any, Union


class StaticClass:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"Static class '{cls.__name__}' cannot be instantiated")

def clamp(number: Any, low: Any, high: Any) -> Any:
    return max(low, min(number, high))

def denum(item: Union[Enum, Any]) -> Any:
    if isinstance(item, Enum):
        return item.value
    return item

def universal(method: callable) -> callable:
    """Makes a new instance of self automatically if called as Class.method()"""
    _cached = functools.cache(method)

    @classmethod
    def wrapper(self, *args, **kwargs):
        if isinstance(self, type):
            self = self()
        return method(self, *args, **kwargs)

    return wrapper

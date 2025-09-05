import functools
from enum import Enum
from pathlib import Path
from typing import Any, Self, Union

from attrs import define


class StaticClass:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"Cannot instantiate static class '{cls.__name__}'")

def clamp(number: Any, low: Any, high: Any) -> Any:
    return max(low, min(number, high))

def denum(item: Union[Enum, Any]) -> Any:
    if isinstance(item, Enum):
        return item.value
    return item

def mkdir(path: Path) -> Path:
    if not (path := Path(path)).exists():
        path.mkdir(parents=True)
    return path

@define
class hybridmethod:
    """Auto make a self instance called as classmethod"""
    method: callable

    def __get__(self, this: Self, cls: type) -> callable:
        instance = (this or cls())

        @functools.wraps(self.method)
        def wrapper(*args, **kwargs):
            return self.method(instance, *args, **kwargs)

        return wrapper

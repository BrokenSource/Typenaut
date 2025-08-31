from enum import Enum
from typing import Any, Union


def clamp(number: Any, low: Any, high: Any) -> Any:
    return max(low, min(number, high))

def denum(item: Union[Enum, Any]) -> Any:
    if isinstance(item, Enum):
        return item.value
    return item

class StaticClass:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"Static class '{cls.__name__}' cannot be instantiated")


from typenaut.core import *
from typenaut.document import Document
from typenaut.module import Composite, Module
from typenaut.modules import *

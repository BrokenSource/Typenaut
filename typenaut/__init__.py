from enum import Enum
from typing import Any, Union


def denum(item: Union[Enum, Any]) -> Any:
    if isinstance(item, Enum):
        return item.value
    return item

class StaticClass:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"Static class '{cls.__name__}' cannot be instantiated")


from typenaut.core.angle import Angle, angle
from typenaut.core.color import Color, color
from typenaut.document import Document
from typenaut.module import Composite, Container, Module
from typenaut.modules.rectangle import Rectangle, rectangle
from typenaut.modules.text import Text, text

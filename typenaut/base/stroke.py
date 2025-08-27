from typing import Iterable, Self

from attrs import define
from typenaut.base.color import Color
from typenaut.base.length import Length


@define
class Stroke:
    color: Color
    width: Length

    def code(self) -> Iterable[str]:
        yield f"{self.color.code()} + {self.width.code()}"

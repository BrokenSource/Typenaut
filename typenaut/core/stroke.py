from typing import Iterable

from attrs import define
from typenaut import StaticClass
from typenaut.core.color import Color
from typenaut.core.length import Length

# ---------------------------------------------------------------------------- #

@define
class Stroke:
    color: Color
    width: Length

    def code(self) -> Iterable[str]:
        yield f"{self.color.ucode()} + {self.width.ucode()}"

# ---------------------------------------------------------------------------- #

class stroke(StaticClass):
    ...

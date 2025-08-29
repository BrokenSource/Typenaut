from typing import Iterable

from attrs import define
from typenaut import StaticClass
from typenaut.core.color import Color, color
from typenaut.core.length import Length, length
from typenaut.module import Module

# ---------------------------------------------------------------------------- #

@define
class Stroke(Module):
    color: Color
    width: Length

    def code(self) -> Iterable[str]:
        yield f"{self.color.ucode()} + {self.width.ucode()}"

# ---------------------------------------------------------------------------- #

class stroke(StaticClass):
    default = lambda: Stroke(color=color.black(), width=length.pt(1))

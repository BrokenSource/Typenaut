from typing import Self

from attrs import define


@define
class Color:
    r: int = 0
    g: int = 0
    b: int = 0

    def luma(self, value: int) -> Self:
        self.r, self.g, self.b = (value, value, value)

    def __str__(self) -> str:
        return f'rgb({self.r}, {self.g}, {self.b})'

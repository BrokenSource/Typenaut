from typing import Self

from attrs import define


@define
class Color:
    r: int = 0
    g: int = 0
    b: int = 0

    def luma(self, value: int) -> Self:
        self.r, self.g, self.b = (value, value, value)

    def white(self) -> Self:
        self.r, self.g, self.b = (255, 255, 255)
        return self

    def __str__(self) -> str:
        return f'rgb({self.r}, {self.g}, {self.b})'

from typing import Iterable

from attrs import define
from typenaut.module import ChildrenModule


@define
class Card(ChildrenModule):
    title: str = "Untitled"

    def code(self) -> Iterable[str]:
        yield '#card('
        for child in self.children:
            yield from child.code()
        yield ')'

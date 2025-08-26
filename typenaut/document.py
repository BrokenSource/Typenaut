from collections.abc import Iterable

import typst
from attrs import define

from typenaut.module import ChildrenModule


@define
class Document(ChildrenModule):
    def __attrs_post_init__(self):
        ...

    def code(self) -> Iterable[str]:
        ...

        for child in self.children:
            yield from child.code()

    def pdf(self) -> bytes:
        typst.compile(
            input=''.join(self.code()),
        )

from collections.abc import Iterable
from pathlib import Path

from attrs import define

from typenaut.module import Module
from typenaut.utils import StaticClass


@define
class Include(Module):
    file: Path

    def typst(self) -> Iterable[str]:
        yield from (
            self.file
            .read_text(encoding="utf-8")
            .splitlines()
        )

class include(StaticClass):
    file = Include

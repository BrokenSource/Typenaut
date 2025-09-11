from collections.abc import Iterable
from pathlib import Path

from attrs import define, field

from typenaut.module import Module
from typenaut.utils import StaticClass


@define
class Include(Module):
    file: Path = field(default=None, converter=Path)

    def __attrs_post_init__(self):
        Module.__attrs_post_init__(self)

        if (not self.file.exists()):
            raise ValueError(f"Included file must exist: {self.file}")

    def typst(self) -> Iterable[str]:
        yield from (
            self.file
            .read_text(encoding="utf-8")
            .splitlines()
        )

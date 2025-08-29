from collections.abc import Iterable

from attrs import define
from typenaut.module import Composite


@define
class Custom(Composite):
    """Inline a custom piece of code"""
    value: str = ""

    def code(self) -> Iterable[str]:
        yield str(self.value)

from collections.abc import Iterable

from attrs import define

from typenaut.module import Module


@define
class Custom(Module):
    """Inline a custom piece of code"""
    value: str = ""

    def typst(self) -> Iterable[str]:
        yield str(self.value)

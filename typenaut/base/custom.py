from collections.abc import Iterable

from attrs import define
from typenaut.module import ChildrenModule


@define
class Custom(ChildrenModule):
    """Inline a custom piece of code"""

    value: str = ""
    """May contain {children}"""

    def code(self) -> Iterable[str]:
        yield str(self.value)
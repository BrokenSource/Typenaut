from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Self

from attrs import Factory, define, field

if TYPE_CHECKING:
    from typenaut.document import Document

# ---------------------------------------------------------------------------- #

@define
class Module(ABC):

    parent: Module = field(default=None, repr=False)
    """Root project object"""

    def __attrs_post_init__(self):
        if isinstance(self.parent, ChildrenModule):
            self.parent.add(self)

    @property
    def document(self) -> Document:
        from typenaut.document import Document

        while not isinstance(self, Document):
            self = self.parent

        return self

    @abstractmethod
    def code(self) -> Iterable[str]:
        """Final code written to the typst document"""
        ...

    def ucode(self) -> str:
        return ''.join(self.code())

    # ------------------------------------------ #
    # Context

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):
        # self.parent.add(self)
        pass

# ---------------------------------------------------------------------------- #

@define
class ChildrenModule(Module):
    """A module which may contain other ones within"""

    def __attrs_post_init__(self):
        Module.__attrs_post_init__(self)

    children: list[Self] = Factory(list)
    """List of modules"""

    def add(self, child: Self) -> Self:
        self.children.append(child)
        child.parent = self
        return self

# ---------------------------------------------------------------------------- #

@define
class FinalModule(Module):
    """A module which does not """
    ...

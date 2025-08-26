from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Optional, Self

from attrs import Factory, define, field

if TYPE_CHECKING:
    from typenaut.document import Document

# ---------------------------------------------------------------------------- #

@define
class Module(ABC):

    parent: Optional[Module] = field(default=None, repr=False)
    """Parent module that contains the current one as child"""

    document: Optional[Document] = field(default=None, repr=False)
    """The root document this module belongs to"""

    def __attrs_post_init__(self):
        from typenaut.document import Document

        # Propagate root document reference
        if (not isinstance(self, Document)):
            self.document = (self.document or self)

        # Automatically append us to content module
        if isinstance(self.parent, ChildrenModule):
            self.parent.add(self)

    def nthparent(self, n: int) -> Optional[Module]:
        """Get the Nth .parent chain module"""
        for _ in range(n):
            self = self.parent
        return self

    @abstractmethod
    def code(self) -> Iterable[str]:
        """Final code written to the typst document"""
        ...

    def ucode(self) -> str:
        return ''.join(self.code())

    def copy(self) -> Self:
        return copy.deepcopy(self)

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

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
    """Base module class that outputs some typst code"""

    # # Typst code

    @abstractmethod
    def typst(self) -> Iterable[str]:
        """Final code written to the typst document"""
        ...

    def code(self) -> str:
        return ''.join(filter(None, self.typst()))

    # # Quality of life

    def copy(self, **update: dict) -> Self:
        """Get a copy with updated values from this module"""
        other = copy.deepcopy(self)
        for key, value in update.items():
            setattr(other, key, value)
        return other

# ---------------------------------------------------------------------------- #

@define
class Composite(Module):

    parent: Optional[Self] = field(default=None, repr=False)
    """Parent module that owns the current one as child"""

    document: Optional["Document"] = field(default=None, repr=False)
    """The root document this module belongs to"""

    def __attrs_post_init__(self):
        from typenaut.document import Document

        # Propagate root document reference
        if (not isinstance(self, Document)):
            self.document = (self.document or self)

        # Automatically append to parent container
        if isinstance(self.parent, Container):
            self.parent.add(self)

    def nthparent(self, n: int) -> Optional[Module]:
        """Get the Nth .parent chain module"""
        for _ in range(n):
            self = self.parent
        return self

# ---------------------------------------------------------------------------- #

@define
class Container(Composite):
    """A module which may contain other ones within"""

    def __attrs_post_init__(self):
        Composite.__attrs_post_init__(self)

    children: list[Self] = Factory(list)
    """List of modules"""

    def add(self, child: Self) -> Self:
        self.children.append(child)
        child.parent = self
        return self

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):
        pass

import copy
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Optional, Self
from uuid import UUID, uuid4

from attrs import Factory, define, field

if TYPE_CHECKING:
    from typenaut.document import Document

# ---------------------------------------------------------------------------- #

@define(slots=False)
class CoreModule(ABC):
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
        new = copy.deepcopy(self)
        for key, value in update.items():
            setattr(new, key, value)
        return new

# ---------------------------------------------------------------------------- #

@define(slots=False)
class Module(CoreModule):

    parent: Optional[Self] = field(default=None, repr=False)
    """Parent module that owns the current one as child"""

    def __attrs_post_init__(self):

        # Automatically append to parent
        if (self.parent is not None):
            self.parent.add(self)

    @property
    def document(self) -> 'Document':
        # Note: While this might seem inefficient, propagating a document
        # reference makes deepcopied objects to run __del__ many times!
        from typenaut.document import Document
        while not isinstance(self, Document):
            self = self.parent
        return self

    # # Typst code

    def imports(self) -> Iterable[str]:
        """Optional imports for the typst document"""
        yield ""

    # # Quality of life

    # Override to optionally change parent
    def copy(self, parent: "Module"=None, **update: dict) -> Self:
        new = CoreModule.copy(self, **update)
        if isinstance(parent, Composite):
            parent.add(new)
        return new

    def nthparent(self, n: int) -> Optional[Self]:
        """Get the Nth .parent chain module"""
        for _ in range(n):
            self = self.parent
        return self

# ---------------------------------------------------------------------------- #

@define(slots=False)
class Composite(Module):
    """A module which may contain other ones within"""

    children: list[Self] = Factory(list)
    """List of modules"""

    def traverse(self) -> Iterable[Module]:
        """Recursively yields all modules"""
        for child in self.children:
            if isinstance(child, Composite):
                yield from child.traverse()
            else:
                yield child
        yield self

    def add(self, child: Self) -> Self:
        self.children.append(child)
        child.parent = self
        return self

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):
        pass

# ---------------------------------------------------------------------------- #

@define(slots=False)
class Labeled:

    label: UUID = Factory(uuid4)
    """Unique identifier for the module"""

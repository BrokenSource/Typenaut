from collections.abc import Iterable

from attrs import define

from typenaut.module import Composite, Labeled


@define(slots=False)
class SectionBase(Labeled, Composite):
    name: str = ""
    depth: int = 1

    def typst(self) -> Iterable[str]:
        yield f"{'='*self.depth} {self.name} <{self.label}>"

        for child in self.children:
            yield from child.typst()

@define
class Section(SectionBase):
    depth: int = 1

@define
class Subsection(SectionBase):
    depth: int = 2

@define
class Subsubsection(SectionBase):
    depth: int = 3

from collections.abc import Iterable

from attrs import define

from typenaut.module import Labeled, Module


@define
class Section(Labeled, Module):
    name: str = ""
    depth: int = 1

    def typst(self) -> Iterable[str]:
        yield f"{'='*self.depth} {self.name} <{self.label}>"

@define
class Subsection(Section):
    depth: int = 2

@define
class Subsubsection(Subsection):
    depth: int = 3

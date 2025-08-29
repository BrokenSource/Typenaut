import shutil
import tempfile
from collections.abc import Iterable
from functools import partial
from pathlib import Path

import typst
from attrs import Factory, define

from typenaut.core.length import AbsoluteLength, Length
from typenaut.module import Container


@define
class Margin:
    right:  Length = Factory(lambda: AbsoluteLength(1.0))
    left:   Length = Factory(lambda: AbsoluteLength(1.0))
    top:    Length = Factory(lambda: AbsoluteLength(1.0))
    bottom: Length = Factory(lambda: AbsoluteLength(1.0))

    @property
    def code(self) -> Iterable[str]:
        yield f"#set page(margin: ("
        yield f"    right:  {self.right.ucode()},"
        yield f"    left:   {self.left.ucode()},"
        yield f"    top:    {self.top.ucode()},"
        yield f"    bottom: {self.bottom.ucode()},"
        yield f"))"
        yield f""


@define
class Document(Container):
    margin: Margin = Factory(Margin)

    workspace: Path = Factory(lambda: Path(tempfile.mkdtemp(prefix=f"{__package__}-")))
    """Temporary directory to store document files, cleaned up on garbage collection"""

    def __attrs_post_init__(self):
        ...

    def __del__(self):
        """Cleanup the temporary directory on destruction"""
        path = Path(tempfile.gettempdir())

        # Triple check workspace is a parent of system tempdir (expected, enforced)
        if (path == self.workspace) or (not self.workspace.is_relative_to(path)):
            raise RuntimeError(f"Avoided catastrophe by not deleting {self.workspace}")

        shutil.rmtree(self.workspace, ignore_errors=True)

    def code(self) -> Iterable[str]:
        yield from self.margin.code

        for child in self.children:
            yield from child.code()

    def pdf(self) -> bytes:
        main = (self.workspace/"main.typ")
        main.write_text('\n'.join(self.code()))

        return typst.compile(
            input=main,
            root=self.workspace,
        )

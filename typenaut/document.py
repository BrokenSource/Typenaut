import shutil
import subprocess
import tempfile
from collections.abc import Iterable
from pathlib import Path
from typing import Optional

import typst
from attrs import Factory, define
from PIL.Image import Image as ImageType

from typenaut.core.length import Length, length
from typenaut.module import Container


@define
class Margin:
    right:  Length = Factory(length.auto)
    left:   Length = Factory(length.auto)
    top:    Length = Factory(length.auto)
    bottom: Length = Factory(length.auto)

    @property
    def code(self) -> Iterable[str]:
        yield f"#set page(margin: ("
        yield f"    right:  {self.right.code()},"
        yield f"    left:   {self.left.code()},"
        yield f"    top:    {self.top.code()},"
        yield f"    bottom: {self.bottom.code()},"
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

    def typst(self) -> Iterable[str]:
        yield from self.margin.code

        for child in self.children:
            yield from child.typst()

    def code(self) -> str:
        main = (self.workspace/"main.typ")
        main.write_text('\n'.join(self.typst()), encoding="utf-8")

        # Optional code formatting if available
        if (typstyle := shutil.which("typstyle")):
            subprocess.run((typstyle, "-i", str(main)))

        return main.read_text(encoding="utf-8")

    def pdf(self,
        output: Optional[Path]=None,
    ) -> bytes:
        self.code()
        return typst.compile(
            input=(self.workspace/"main.typ"),
            output=output,
            root=self.workspace,
            format="pdf",
        )

    def png(self,
        ppi: int=144,
    ) -> ImageType:
        raise NotImplementedError

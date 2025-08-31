import atexit
import gc
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
from typenaut.module import Composite

# Ensure workspace is cleaned at exit
atexit.register(gc.collect)


@define
class Margin(Composite):
    right:  Length = Factory(length.auto)
    left:   Length = Factory(length.auto)
    top:    Length = Factory(length.auto)
    bottom: Length = Factory(length.auto)

    def typst(self) -> Iterable[str]:
        yield f"#set page(margin: ("
        yield   f"right:  {self.right.code()},"
        yield   f"left:   {self.left.code()},"
        yield   f"top:    {self.top.code()},"
        yield   f"bottom: {self.bottom.code()},"
        yield f"))"


@define
class Document(Composite):
    margin: Margin = Factory(Margin, takes_self=True)

    workspace: Path = Factory(lambda: Path(tempfile.mkdtemp(prefix=f"{__package__}-")))
    """Temporary directory to store document files, cleaned up on garbage collection"""

    def __attrs_post_init__(self):
        Composite.__attrs_post_init__(self)

    def __del__(self):
        """Cleanup the temporary directory on destruction"""
        path = Path(tempfile.gettempdir())

        # Triple check workspace is a parent of system tempdir (expected, enforced)
        if (path == self.workspace) or (not self.workspace.is_relative_to(path)):
            raise RuntimeError(f"Expected workspace {self.workspace} path changed for deletion")

        shutil.rmtree(self.workspace, ignore_errors=True)

    def typst(self) -> Iterable[str]:

        # Organize imports at the start
        for module in self.traverse():
            yield from module.imports()

        for child in self.children:
            yield from child.typst()

    def code(self) -> str:
        code = '\n'.join(self.typst())
        code = '\n'.join(filter(None, code.splitlines()))
        self._typ.write_text(code)

        # Optional code formatting if available
        if (typstyle := shutil.which("typstyle")):
            subprocess.run((typstyle, "-i", str(self._typ)))

        return self._typ.read_text()

    @property
    def _typ(self) -> Path:
        return (self.workspace / "main.typ")

    def pdf(self,
        output: Optional[Path]=None,
    ) -> bytes:
        self.code()
        return typst.compile(
            root=self.workspace,
            input=self._typ,
            output=output,
            format="pdf",
        )

    def png(self,
        ppi: int=144,
    ) -> ImageType:
        raise NotImplementedError

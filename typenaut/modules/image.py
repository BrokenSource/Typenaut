import shutil
from pathlib import Path
from typing import Iterable, Literal, Optional, Union

from attrs import Factory, define
from PIL.Image import Image as ImageType

from typenaut.core.function import Function
from typenaut.core.length import Length, length
from typenaut.module import Composite, Labeled
from typenaut.utils import StaticClass

# ---------------------------------------------------------------------------- #

@define
class Image(Composite, Labeled):
    """https://typst.app/docs/reference/visualize/image/"""

    source: Union[Path, ImageType, bytes]
    """https://typst.app/docs/reference/visualize/image/#parameters-source"""

    width: Length = Factory(length.auto)
    """https://typst.app/docs/reference/visualize/image/#parameters-width"""

    height: Length = Factory(length.auto)
    """https://typst.app/docs/reference/visualize/image/#parameters-height"""

    scaling: Literal["smooth", "pixelated"] = "smooth"
    """https://typst.app/docs/reference/visualize/image/#parameters-scaling"""

    fit: Literal["cover", "contain", "stretch"] = "cover"
    """https://typst.app/docs/reference/visualize/image/#parameters-fit"""

    def __attrs_post_init__(self):
        if isinstance(self.source, Path):
            shutil.copy(self.source, self.path)

        elif isinstance(self.source, bytes):
            self.path.write_bytes(self.source)

        elif isinstance(self.source, ImageType):
            self.source.save(self.path, format="PNG")

    @property
    def path(self) -> Path:
        return (self.document.images/f"{self.label}")

    def typst(self) -> Iterable[str]:
        yield from Function(
            name="image",
            args=[self.path],
            kwargs=dict(
                width=self.width,
                height=self.height,
                scaling=self.scaling,
                alt=f"Image {self.label}",
                fit=self.fit,
            ),
            body=self.children,
        ).call()
        yield f"<{self.label}>"

# ---------------------------------------------------------------------------- #

class image(StaticClass):
    ...

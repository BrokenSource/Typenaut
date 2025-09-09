from pathlib import Path
from typing import Iterable, Literal, Optional, Union

import imageio.v3 as iio
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

    width: Optional[Length] = Factory(length.auto)
    """https://typst.app/docs/reference/visualize/image/#parameters-width"""

    height: Optional[Length] = Factory(length.auto)
    """https://typst.app/docs/reference/visualize/image/#parameters-height"""

    fit: Literal["cover", "contain", "stretch"] = "cover"
    """https://typst.app/docs/reference/visualize/image/#parameters-fit"""

    def __attrs_post_init__(self):
        self.document.images

    def path(self) -> Path:
        return (self.document.images/f"{self.label}.png")

    def where(self) -> Path:
        if isinstance(self.source, Path):
            return self.source
        # Todo: Save bytes or PIL to workspace path

    def typst(self) -> Iterable[str]:
        yield from Function(
            name="image",
            args=[self.source],
            kwargs=dict(
                width=self.width,
                height=self.height,
                fit=self.fit,
            ),
            body=self.children,
        ).call()
        yield f"<{self.label}>"

# ---------------------------------------------------------------------------- #

class image(StaticClass):
    ...

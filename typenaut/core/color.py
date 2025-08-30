import colorsys
from typing import Iterable, Self

from attrs import define
from typenaut import StaticClass
from typenaut.module import Module

# ---------------------------------------------------------------------------- #

@define
class Color(Module):

    red: float = 0.0
    """Normalized red component value"""

    green: float = 0.0
    """Normalized green component value"""

    blue: float = 0.0
    """Normalized blue component value"""

    alpha: float = 1.0
    """Normalized alpha component value"""

    # ------------------------------------------ #
    # Module implementation

    def typst(self) -> Iterable[str]:
        yield "rgb("
        yield     f"{100.0*self.red:.2f}%,"
        yield     f"{100.0*self.green:.2f}%,"
        yield     f"{100.0*self.blue:.2f}%,"
        yield     f"{100.0*self.alpha:.2f}%"
        yield ")"

    # ------------------------------------------ #
    # Red, Green, Blue (RGB)

    @classmethod
    def from_rgb(cls,
        red:   float=0.0,
        green: float=0.0,
        blue:  float=0.0,
        alpha: float=1.0
    ) -> Self:
        """Get a color from a rgba(0.0-1.0) normalized tuple"""
        return cls(red=red, green=green, blue=blue, alpha=alpha)

    @classmethod
    def from_rgb_u8(cls,
        red:   int=0,
        green: int=0,
        blue:  int=0,
        alpha: int=255
    ) -> Self:
        """Get a color from a rgba(0-255) SDR u8 tuple"""
        return cls(
            red   = (red  /255.0),
            green = (green/255.0),
            blue  = (blue /255.0),
            alpha = (alpha/255.0)
        )

    @property
    def rgb(self) -> tuple[float, float, float]:
        return (self.red, self.green, self.blue)

    @rgb.setter
    def rgb(self, value: tuple[float, float, float]):
        self.red, self.green, self.blue = value

    # ------------------------------------------ #
    # LUMA

    @staticmethod
    def from_luma(value: float) -> Self:
        """Get a grayscale color from a (0.0-1.0) luma value"""
        return Color.from_rgb(red=value, green=value, blue=value)

    @staticmethod
    def from_luma_u8(value: int) -> Self:
        """Get a grayscale color from a (0-255) luma value"""
        return Color.from_rgb_u8(red=value, green=value, blue=value)

    # ------------------------------------------ #
    # Hexadecimal

    @classmethod
    def from_hex(cls, value: str) -> Self:
        """Get a color from a hex string"""
        self = cls()
        self.hex = value
        return self

    @property
    def hex(self) -> str:
        """Get the color as a hex string"""
        return ("#"
            f"{int(255*self.red):02X}"
            f"{int(255*self.green):02X}"
            f"{int(255*self.blue):02X}"
            f"{int(255*self.alpha):02X}"
        )

    @hex.setter
    def hex(self, value: str):
        value: str = value.lstrip("#")

        def parse(value: str, chunk: int) -> Iterable[int]:
            for part in range(0, len(value), chunk):
                item = value[part:part+chunk]
                item = item * (3 - chunk)
                yield int(item, 16) / 255.0
            yield self.alpha

        # From sugar '#ABC' as '#AABBCC'
        if len(value) in (3, 4):
            color = parse(value, 1)

        # Regular hex, optional alpha
        elif len(value) in (6, 8):
            color = parse(value, 2)

        else:
            raise ValueError(f"Invalid hex color: '{value}'")

        # Update self values consuming the generator
        self.red, self.green, self.blue, self.alpha, *_ = color

    # ------------------------------------------ #
    # Hue, Saturation, Brightness (HSV)

    @classmethod
    def from_hsv(cls,
        hue: float=0.0,
        saturation: float=1.0,
        brightness: float=1.0,
        alpha: float=0.0
    ) -> Self:
        """Get a color from a hsva(0.0-1.0) normalized tuple"""
        return cls(*colorsys.hsv_to_rgb(hue, saturation, brightness), alpha=alpha)

    @property
    def hsv(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hsv(self.red, self.green, self.blue)

    @hsv.setter
    def hsv(self, value: tuple[float, float, float]):
        self.red, self.green, self.blue = colorsys.hsv_to_rgb(*value)

    # ------------------------------------------ #
    # Hue, Saturation, Luminance (HSL)

    @classmethod
    def from_hsl(cls,
        hue: float=0.0,
        saturation: float=1.0,
        lightness: float=1.0,
        alpha: float=1.0
    ) -> Self:
        """Get a color from a hsla(0.0-1.0) normalized tuple"""
        return cls(*colorsys.hls_to_rgb(hue, lightness, saturation), alpha=alpha)

    @property
    def hls(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hls(self.red, self.green, self.blue)

    @hls.setter
    def hls(self, value: tuple[float, float, float]):
        self.red, self.green, self.blue = colorsys.hls_to_rgb(*value)

    # ------------------------------------------ #
    # Shared and unique components of HSV, HSL

    # Hue

    @property
    def hue(self) -> float:
        return self.hsv[0]

    @hue.setter
    def hue(self, value: float):
        self.hsv = (value, self.saturation, self.brightness)

    # Saturation

    @property
    def saturation(self) -> float:
        return self.hsv[1]

    @saturation.setter
    def saturation(self, value: float):
        self.hsv = (self.hue, value, self.brightness)

    # Brightness

    @property
    def brightness(self) -> float:
        return self.hsv[2]

    @brightness.setter
    def brightness(self, value: float):
        self.hsv = (self.hue, self.saturation, value)

    # Lightness

    @property
    def lightness(self) -> float:
        return self.hls[1]

    @lightness.setter
    def lightness(self, value: float):
        self.hls = (self.hue, value, self.saturation)

# ---------------------------------------------------------------------------- #

class color(StaticClass):
    rgb     = Color.from_rgb
    rgb_u8  = Color.from_rgb_u8
    luma    = Color.from_luma
    luma_u8 = Color.from_luma_u8
    hex     = Color.from_hex
    hsv     = Color.from_hsv
    hsl     = Color.from_hsl

    # # Predefined Colors

    none    = lambda: Color.from_hex("#00000000")
    black   = lambda: Color.from_hex("#000000")
    gray    = lambda: Color.from_hex("#AAAAAA")
    silver  = lambda: Color.from_hex("#DDDDDD")
    white   = lambda: Color.from_hex("#FFFFFF")
    navy    = lambda: Color.from_hex("#001F3F")
    blue    = lambda: Color.from_hex("#0074D9")
    aqua    = lambda: Color.from_hex("#7fDBFF")
    teal    = lambda: Color.from_hex("#39CCCC")
    eastern = lambda: Color.from_hex("#239DAD")
    purple  = lambda: Color.from_hex("#B10DC9")
    fuchsia = lambda: Color.from_hex("#F012BE")
    maroon  = lambda: Color.from_hex("#85144B")
    red     = lambda: Color.from_hex("#FF4136")
    orange  = lambda: Color.from_hex("#FF851B")
    yellow  = lambda: Color.from_hex("#FFDC00")
    olive   = lambda: Color.from_hex("#3D9970")
    green   = lambda: Color.from_hex("#2ECC40")
    lime    = lambda: Color.from_hex("#01FF70")

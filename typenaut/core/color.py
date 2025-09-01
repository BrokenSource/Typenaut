import colorsys
import functools
from typing import Iterable, Optional, Self

from attrs import define

from typenaut.module import CoreModule
from typenaut.utils import StaticClass, clamp, universal

# ---------------------------------------------------------------------------- #

@define
class Color(CoreModule):

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
        yield f"  {clamp(100.0*self.red,   0, 100):.2f}%,"
        yield f"  {clamp(100.0*self.green, 0, 100):.2f}%,"
        yield f"  {clamp(100.0*self.blue,  0, 100):.2f}%,"
        yield f"  {clamp(100.0*self.alpha, 0, 100):.2f}%,"
        yield ")"

    # ------------------------------------------ #
    # Red, Green, Blue (RGB)

    @universal
    def rgb(self,
        red:   Optional[float]=None,
        green: Optional[float]=None,
        blue:  Optional[float]=None,
        alpha: Optional[float]=None,
    ) -> Self:
        """Set a color from a rgba(0.0-1.0) normalized tuple"""
        self.red   = (red   or self.red  )
        self.green = (green or self.green)
        self.blue  = (blue  or self.blue )
        self.alpha = (alpha or self.alpha)
        return self

    def as_rgb(self) -> tuple[float, float, float, float]:
        return (self.red, self.green, self.blue, self.alpha)

    @universal
    def rgb_u8(self,
        red:   Optional[int]=None,
        green: Optional[int]=None,
        blue:  Optional[int]=None,
        alpha: Optional[int]=None,
    ) -> Self:
        """Set a color from a rgba(0-255) SDR u8 tuple"""
        for key, value in locals().items():
            if (value is not None) and (value != self):
                setattr(self, key, value/255.0)
        return self

    def as_rgb_u8(self) -> tuple[int, int, int, int]:
        return tuple(map(lambda x: 255*x, self.as_rgb()))

    # ------------------------------------------ #
    # LUMA

    # @staticmethod
    # @functools.cache
    # def from_luma(value: float) -> Self:
    #     """Get a grayscale color from a (0.0-1.0) luma value"""
    #     return Color.rgb(red=value, green=value, blue=value)

    # @staticmethod
    # @functools.cache
    # def from_luma_u8(value: int) -> Self:
    #     """Get a grayscale color from a (0-255) luma value"""
    #     return Color.from_rgb_u8(red=value, green=value, blue=value)

    # @property
    # def luma(self) -> float:
    #     """Get the luma (brightness) of the color"""
    #     return (0.299 * self.red) + (0.587 * self.green) + (0.114 * self.blue)

    # @luma.setter
    # def luma(self, value: float):
    #     self.red = self.green = self.blue = value

    @universal
    def luma(self, value: float) -> Self:
        self.red = self.green = self.blue = value
        return self

    def as_luma(self) -> float:
        return (self.red + self.green + self.blue) / 3.0

    @universal
    def luma_u8(self, value: int) -> Self:
        return self.luma(value / 255.0)

    def as_luma_u8(self) -> int:
        return int(255 * self.as_luma())

    # ------------------------------------------ #
    # Hexadecimal

    @universal
    def hex(self, value: str) -> Self:
        """Set the color as a hex string"""
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

    def as_hex(self) -> str:
        """Get the color as a hex string"""
        return ("#"
            f"{int(255*self.red):02X}"
            f"{int(255*self.green):02X}"
            f"{int(255*self.blue):02X}"
            f"{int(255*self.alpha):02X}"
        )

    # ------------------------------------------ #
    # Hue, Saturation, Brightness (HSV)

    @universal
    def hsv(self,
        hue: float=0.0,
        saturation: float=1.0,
        brightness: float=1.0,
        alpha: float=1.0
    ) -> Self:
        """Set a color from a hsva(0.0-1.0) normalized tuple"""
        self.red, self.green, self.blue = colorsys.hsv_to_rgb(hue, saturation, brightness)
        self.alpha = alpha
        return self

    def as_hsv(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hsv(self.red, self.green, self.blue)

    # ------------------------------------------ #
    # Hue, Saturation, Luminance (HSL)

    @universal
    def hsl(self,
        hue: float=0.0,
        lightness: float=1.0,
        saturation: float=1.0,
        alpha: float=1.0
    ) -> Self:
        """Set a color from a hsla(0.0-1.0) normalized tuple"""
        self.red, self.green, self.blue = colorsys.hls_to_rgb(hue, lightness, saturation)
        self.alpha = alpha
        return self

    def as_hls(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hls(self.red, self.green, self.blue)

    # ------------------------------------------ #
    # Shared and unique components of HSV, HSL

    # Hue

    @property
    def hue(self) -> float:
        return self.as_hsv()[0]

    @hue.setter
    def hue(self, value: float):
        self.hsv(
            hue=value,
            saturation=self.saturation,
            brightness=self.brightness
        )

    # Saturation

    @property
    def saturation(self) -> float:
        return self.as_hsv()[1]

    @saturation.setter
    def saturation(self, value: float):
        self.hsv(
            hue=self.hue,
            saturation=value,
            brightness=self.brightness
        )

    # Brightness

    @property
    def brightness(self) -> float:
        """Zero is black, one is full color"""
        return self.as_hsv()[2]

    @brightness.setter
    def brightness(self, value: float):
        self.hsv(
            hue=self.hue,
            saturation=self.saturation,
            brightness=value
        )

    # Lightness

    @property
    def lightness(self) -> float:
        """Zero is black, one is white"""
        return self.as_hsl()[1]

    @lightness.setter
    def lightness(self, value: float):
        self.hsl = (self.hue, value, self.saturation)

# ---------------------------------------------------------------------------- #

class color(StaticClass):
    rgb     = Color.rgb
    rgb_u8  = Color.rgb_u8
    luma    = Color.luma
    luma_u8 = Color.luma_u8
    hex     = Color.hex
    hsv     = Color.hsv
    hsl     = Color.hsl

    # # Predefined Colors

    none    = lambda: Color.hex("#00000000")
    black   = lambda: Color.hex("#000000")
    gray    = lambda: Color.hex("#AAAAAA")
    silver  = lambda: Color.hex("#DDDDDD")
    white   = lambda: Color.hex("#FFFFFF")
    navy    = lambda: Color.hex("#001F3F")
    blue    = lambda: Color.hex("#0074D9")
    aqua    = lambda: Color.hex("#7fDBFF")
    teal    = lambda: Color.hex("#39CCCC")
    eastern = lambda: Color.hex("#239DAD")
    purple  = lambda: Color.hex("#B10DC9")
    fuchsia = lambda: Color.hex("#F012BE")
    maroon  = lambda: Color.hex("#85144B")
    red     = lambda: Color.hex("#FF4136")
    orange  = lambda: Color.hex("#FF851B")
    yellow  = lambda: Color.hex("#FFDC00")
    olive   = lambda: Color.hex("#3D9970")
    green   = lambda: Color.hex("#2ECC40")
    lime    = lambda: Color.hex("#01FF70")

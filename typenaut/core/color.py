import colorsys
from typing import Iterable, Self

from attrs import Attribute, define, field

from typenaut.module import CoreModule
from typenaut.utils import StaticClass, clamp, hybridmethod, unpacked

# ---------------------------------------------------------------------------- #

def __clamp_color__(self, _: Attribute, value: float) -> float:
    return clamp(value, 0.0, 1.0)

@define
class Color(CoreModule):

    red: float = field(default=0.0, on_setattr=__clamp_color__)
    """Normalized red component value"""

    green: float = field(default=0.0, on_setattr=__clamp_color__)
    """Normalized green component value"""

    blue: float = field(default=0.0, on_setattr=__clamp_color__)
    """Normalized blue component value"""

    alpha: float = field(default=1.0, on_setattr=__clamp_color__)
    """Normalized alpha component value"""

    # -------------------------------- #
    # Module implementation

    def typst(self) -> Iterable[str]:
        yield "rgb("
        yield     f"{clamp(100.0*self.red,   0, 100):.2f}%,"
        yield     f"{clamp(100.0*self.green, 0, 100):.2f}%,"
        yield     f"{clamp(100.0*self.blue,  0, 100):.2f}%,"
        yield     f"{clamp(100.0*self.alpha, 0, 100):.2f}%"
        yield ")"

    # -------------------------------- #
    # Red, Green, Blue (RGB)

    @hybridmethod
    def set_red(self, value: float) -> Self:
        self.red = value
        return self

    @hybridmethod
    def set_green(self, value: float) -> Self:
        self.green = value
        return self

    @hybridmethod
    def set_blue(self, value: float) -> Self:
        self.blue = value
        return self

    @hybridmethod
    def set_rgb(self,
        red:   float=0.0,
        green: float=0.0,
        blue:  float=0.0,
        alpha: float=1.0,
    ) -> Self:
        """Get a color from a rgba(0.0-1.0) normalized tuple"""
        self.red   = red
        self.green = green
        self.blue  = blue
        self.alpha = alpha
        return self

    def get_rgb(self) -> tuple[float, float, float]:
        return (self.red, self.green, self.blue)

    rgb = property(get_rgb, unpacked(set_rgb))

    @hybridmethod
    def set_rgb_u8(self,
        red:   int=0,
        green: int=0,
        blue:  int=0,
        alpha: int=255,
    ) -> Self:
        """Get a color from a rgba(0-255) SDR u8 tuple"""
        return self.set_rgb(
            red   = (red  /255.0),
            green = (green/255.0),
            blue  = (blue /255.0),
            alpha = (alpha/255.0),
        )

    def get_rgb_u8(self) -> tuple[int, int, int]:
        return (
            int(255*self.red),
            int(255*self.green),
            int(255*self.blue),
        )

    rgb_u8 = property(get_rgb_u8, unpacked(set_rgb_u8))

    # -------------------------------- #
    # LUMA

    @hybridmethod
    def set_luma(self, value: float) -> Self:
        """Get a grayscale color from a (0.0-1.0) luma value"""
        self.red = self.green = self.blue = value
        return self

    def get_luma(self) -> float:
        """Get the luma (brightness) of the color"""
        return (0.299 * self.red) + (0.587 * self.green) + (0.114 * self.blue)

    luma = property(get_luma, set_luma)

    @hybridmethod
    def set_luma_u8(self, value: int) -> Self:
        """Get a grayscale color from a (0-255) luma value"""
        return self.set_luma(value/255.0)

    # -------------------------------- #
    # Hexadecimal

    @hybridmethod
    def set_hex(self, value: str) -> Self:
        """Get a color from a hex string"""
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
        return self

    @property
    def get_hex(self) -> str:
        """Get the color as a hex string"""
        return ("#"
            f"{int(255*self.red):02X}"
            f"{int(255*self.green):02X}"
            f"{int(255*self.blue):02X}"
            f"{int(255*self.alpha):02X}"
        )

    hex = property(get_hex, set_hex)

    # -------------------------------- #
    # Hue, Saturation, Brightness (HSV)

    @hybridmethod
    def set_hsv(self,
        hue:        float=0.0,
        saturation: float=1.0,
        brightness: float=1.0,
        alpha:      float=1.0,
    ) -> Self:
        """Get a color from a hsva(0.0-1.0) normalized tuple"""
        rgb = colorsys.hsv_to_rgb(hue, saturation, brightness)
        self.red, self.green, self.blue = rgb
        self.alpha = alpha
        return self

    def get_hsv(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hsv(self.red, self.green, self.blue)

    hsv = property(get_hsv, unpacked(set_hsv))

    # -------------------------------- #
    # Hue, Saturation, Luminance (HSL)

    @hybridmethod
    def set_hsl(self,
        hue:        float=0.0,
        saturation: float=1.0,
        lightness:  float=1.0,
        alpha:      float=1.0,
    ) -> Self:
        """Get a color from a hsla(0.0-1.0) normalized tuple"""
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        self.red, self.green, self.blue = rgb
        self.alpha = alpha
        return self

    def as_hsl(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hls(self.red, self.green, self.blue)

    hsl = property(as_hsl, unpacked(set_hsl))

    # -------------------------------- #
    # Shared and unique components of HSV, HSL

    # Hue

    @property
    def hue(self) -> float:
        return self.hsv[0]

    @hue.setter
    def hue(self, value: float):
        self.set_hsv(value, self.saturation, self.brightness)

    # Saturation

    @property
    def saturation(self) -> float:
        return self.get_hsv()[1]

    @saturation.setter
    def saturation(self, value: float):
        self.set_hsv(self.hue, value, self.brightness)

    # Brightness

    @property
    def brightness(self) -> float:
        """Zero is black, one is full color"""
        return self.get_hsv()[2]

    @brightness.setter
    def brightness(self, value: float):
        self.set_hsv(self.hue, self.saturation, value)

    # Lightness

    @property
    def lightness(self) -> float:
        """Zero is black, one is white"""
        return self.get_hls()[1]

    @lightness.setter
    def lightness(self, value: float):
        self.set_hls(self.hue, value, self.saturation)

    # -------------------------------- #
    # Special

    def negate(self) -> Self:
        self.red   = (1.0 - self.red)
        self.green = (1.0 - self.green)
        self.blue  = (1.0 - self.blue)
        return self

# ---------------------------------------------------------------------------- #

class color(StaticClass):
    rgb     = Color.set_rgb
    rgb_u8  = Color.set_rgb_u8
    luma    = Color.set_luma
    luma_u8 = Color.set_luma_u8
    hex     = Color.set_hex
    hsv     = Color.set_hsv
    hsl     = Color.set_hsl

    # https://typst.app/docs/reference/visualize/color/#predefined-colors

    none    = lambda: Color.set_hex("#00000000")
    black   = lambda: Color.set_hex("#000000")
    gray    = lambda: Color.set_hex("#AAAAAA")
    silver  = lambda: Color.set_hex("#DDDDDD")
    white   = lambda: Color.set_hex("#FFFFFF")
    navy    = lambda: Color.set_hex("#001F3F")
    blue    = lambda: Color.set_hex("#0074D9")
    aqua    = lambda: Color.set_hex("#7fDBFF")
    teal    = lambda: Color.set_hex("#39CCCC")
    eastern = lambda: Color.set_hex("#239DAD")
    purple  = lambda: Color.set_hex("#B10DC9")
    fuchsia = lambda: Color.set_hex("#F012BE")
    maroon  = lambda: Color.set_hex("#85144B")
    red     = lambda: Color.set_hex("#FF4136")
    orange  = lambda: Color.set_hex("#FF851B")
    yellow  = lambda: Color.set_hex("#FFDC00")
    olive   = lambda: Color.set_hex("#3D9970")
    green   = lambda: Color.set_hex("#2ECC40")
    lime    = lambda: Color.set_hex("#01FF70")

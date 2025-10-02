import functools
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Self, Union

from attrs import define


class StaticClass:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"Cannot instantiate static class '{cls.__name__}'")

def clamp(number: Any, low: Any, high: Any) -> Any:
    return max(low, min(number, high))

def denum(item: Union[Enum, Any]) -> Any:
    if isinstance(item, Enum):
        return item.value
    return item

def mkdir(path: Path) -> Path:
    if not (path := Path(path)).exists():
        path.mkdir(parents=True)
    return path

@define
class hybridmethod:
    """
    Automatically make a 'self' instance if called as a classmethod

    Example:
        ```python
        class Angle:

            @hybridmethod
            def degrees(self, value: float) -> Self:
                self.value = value
                return self

        # Smart fluent interfaces
        angle = Angle().degrees(90)
        angle = Angle.degrees(90)
        ```
    """
    method: callable

    def __get__(self, this: Self, cls: type) -> callable:

        @functools.wraps(self.method)
        def wrapper(*args, **kwargs) -> Any:
            instance = (this or cls())
            return self.method(instance, *args, **kwargs)

        return wrapper

    def __call__(self, this: Self, *args, **kwargs) -> Any:
        return self.method(this, *args, **kwargs)

def unpacked(method: callable) -> callable:
    """
    Wraps a method to call with unpacked @property.setter arguments

    Example:
        ```python
        class Color:
            def get_rgb(self) -> tuple[float, float, float]:
                return (self.r, self.g, self.b)

            def set_rgb(self, r, g, b):
                self.r, self.g, self.b = (r, g, b)

            rgb = property(get_rgb, unpacked(set_rgb))

        # Allows for using:
        color = Color()
        color.rgb = (1.0, 0.0, 0.0)
        ```
    """

    @functools.wraps(method)
    def wrapper(self, single: Iterable) -> Any:
        return method(self, *single)

    return wrapper
from pathlib import Path
from typing import Any, Iterable, Optional

from attrs import Factory, define

from typenaut.module import CoreModule
from typenaut.utils import denum


@define
class Function(CoreModule):
    name: str
    args: list[Any] = Factory(list)
    kwargs: dict[str, Any] = Factory(dict)
    body: Optional[Iterable[CoreModule]] = None

    def any2typ(self, value: Any) -> Any:
        value = denum(value)

        if (value is None):
            return ""
        elif isinstance(value, Path):
            return f'"{value}"'
        elif isinstance(value, str):
            return f'{value}'
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return value
        elif isinstance(value, CoreModule):
            return value.code()
        raise TypeError(f"Cannot convert {type(value)} to typst code")

    def typst(self) -> Iterable[str]:
        raise RuntimeError("Ambiguous code from function: .define() or .call()")

    def define(self) -> Iterable[str]:
        raise NotImplementedError

    def call(self) -> Iterable[str]:
        yield f"#{self.name}("

        # Positional arguments
        for value in filter(None, self.args):
            yield f"{self.any2typ(value)},"

        # Keyword arguments
        for key, value in self.kwargs.items():
            if (value is not None):
                yield f"  {key}: {self.any2typ(value)},"

        if (self.body is not None):
            yield ")["
            for item in filter(None, self.body):
                yield self.any2typ(item)
            yield "]"
        else:
            yield ")"


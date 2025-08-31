from typing import Any, Iterable, Optional

from attrs import Factory, define

from typenaut import denum
from typenaut.module import CoreModule


@define
class Function(CoreModule):
    name: str
    args: list[Any] = Factory(list)
    kwargs: dict[str, Any] = Factory(dict)
    body: Optional[Iterable[CoreModule]] = None

    def any2typ(self, value: Any) -> Any:
        value = denum(value)

        if (value is None):
            return "none"
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
        for value in self.args:
            yield f"{self.any2typ(value)},"

        # Keyword arguments
        for key, value in self.kwargs.items():
            yield f"  {key}: {self.any2typ(value)},"

        yield ")["
        if (self.body is not None):
            for item in self.body:
                yield self.any2typ(item)
        yield "]"


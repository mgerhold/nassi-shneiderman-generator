from typing import final
from abc import ABC, abstractmethod
from typing import Optional


class Symbol(ABC):
    def __init__(self, identifier: Optional[str] = None):
        self._identifier = identifier

    @property
    def identifier(self) -> Optional[str]:
        return self._identifier

    @abstractmethod
    def emit(self) -> str:
        pass


@final
class Imperative(Symbol):
    def __init__(self, text: str, identifier: Optional[str] = None):
        super().__init__(identifier)
        self._text = text

    @property
    def text(self) -> str:
        return self._text


@final
class Block(Symbol):
    def __init__(self, inner: Symbol, identifier: Optional[str] = None):
        super().__init__(identifier)
        self._inner = inner

    @property
    def inner(self) -> Symbol:
        return self._inner


@final
class Serial(Symbol):
    def __init__(self, elements: list[Symbol], identifier: Optional[str] = None):
        super().__init__(identifier)
        self._elements = elements

    @property
    def elements(self) -> list[Symbol]:
        return self._elements

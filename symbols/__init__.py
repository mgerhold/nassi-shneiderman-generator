from typing import override
from dimensions import Dimensions
from latex import measure_latex_dimensions
from typing import final, Final
from abc import ABC, abstractmethod
from typing import Optional

_TEXT_MARGIN = 4.0


class Symbol(ABC):
    @abstractmethod
    def emit(self, position: tuple[float, float], size: tuple[float, float]) -> str:
        pass

    @property
    @abstractmethod
    def required_size(self) -> tuple[float, float]:
        pass


@final
class Imperative(Symbol):
    def __init__(self, text: str, color: Optional[str] = None):
        self._text = text
        self._color = color

    @property
    def text(self) -> str:
        return self._text

    @override
    def emit(self, position: tuple[float, float], size: tuple[float, float]) -> str:
        x1: Final = position[0]
        y1: Final = position[1]
        x2: Final = position[0] + size[0]
        y2: Final = position[1] - size[1]
        text_x: Final = position[0] + size[0] / 2.0
        text_y: Final = position[1] - size[1] / 2.0 - self._dimensions.depth / 2.0
        options: Final = "" if self._color is None else f"[{self._color}]"
        return rf"""\draw{options} ({x1}pt,{y1}pt) rectangle ({x2}pt, {y2}pt);\
\node at ({text_x}pt, {text_y}pt) {{{self.text}}};
"""

    @override
    @property
    def required_size(self) -> tuple[float, float]:
        return (
            self._dimensions.width + 2.0 * _TEXT_MARGIN,
            self._dimensions.height + 2.0 * _TEXT_MARGIN,
        )

    @property
    def _dimensions(self) -> Dimensions:
        return measure_latex_dimensions(self._text)


@final
class Block(Symbol):
    def __init__(self, text: str, inner: Symbol):
        self._text = text
        self._inner = inner

    @property
    def text(self) -> str:
        return self._text

    @property
    def inner(self) -> Symbol:
        return self._inner

    @property
    def _margin(self) -> float:
        text_size: Final = measure_latex_dimensions(self._text)
        return text_size.total_height + _TEXT_MARGIN * 2.0

    def emit(self, position: tuple[float, float], size: tuple[float, float]) -> str:
        result = Imperative("").emit(position, size)
        text_size: Final = measure_latex_dimensions(self._text)
        text_x: Final = position[0] + text_size.width / 2.0 + _TEXT_MARGIN
        text_y: Final = position[1] - text_size.height / 2.0 - text_size.depth / 2.0 - _TEXT_MARGIN
        result += rf"\node at ({text_x}pt, {text_y}pt) {{{self.text}}};" + "\n"
        result += self._inner.emit(
            (position[0] + self._margin, position[1] - self._margin),
            (size[0] - 2.0 * self._margin, size[1] - 2.0 * self._margin),
        )
        return result

    @property
    def required_size(self) -> tuple[float, float]:
        inner_size: Final = self._inner.required_size
        return (
            inner_size[0] + 2.0 * self._margin,
            inner_size[1] + 2.0 * self._margin,
        )


@final
class Serial(Symbol):
    def __init__(self, elements: list[Symbol]):
        self._elements = elements

    @property
    def elements(self) -> list[Symbol]:
        return self._elements

    def emit(self, position: tuple[float, float], size: tuple[float, float]) -> str:
        output = ""
        required_size: Final = self.required_size
        element_size: Final = required_size[0], required_size[1] / len(self._elements)
        current_position = position
        for element in self._elements:
            output += element.emit(current_position, element_size)
            current_position = (
                current_position[0],
                current_position[1] - element_size[1],
            )
        return output

    @override
    @property
    def required_size(self) -> tuple[float, float]:
        max_width = 0.0
        max_height = 0.0
        for element in self._elements:
            element_size = element.required_size
            max_width = max(max_width, element_size[0])
            max_height = max(max_height, element_size[1])
        return max_width, max_height * len(self._elements)

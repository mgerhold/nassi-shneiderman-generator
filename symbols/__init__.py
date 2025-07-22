from enum import Enum, auto
from typing import NamedTuple
from typing import override
from dimensions import Dimensions
from latex import measure_latex_dimensions
from typing import final, Final
from abc import ABC, abstractmethod
from typing import Optional

_TEXT_MARGIN = 4.0


def _lerp(start: float, end: float, t: float) -> float:
    return start + (end - start) * t


def _options(color: Optional[str]) -> str:
    return "" if color is None else f"[{color}]"


def _line(x1: float, y1: float, x2: float, y2: float) -> str:
    return rf"\draw ({x1}pt, {y1}pt) -- ({x2}pt, {y2}pt);" + "\n"


def _rectangle(x1: float, y1: float, x2: float, y2: float, color: Optional[str]) -> str:
    return rf"\draw{_options(color)} ({x1}pt,{y1}pt) rectangle ({x2}pt, {y2}pt);" + "\n"


def _text(position: tuple[float, float], text: str, color: Optional[str] = None) -> str:
    size: Final = measure_latex_dimensions(text)
    x: Final = position[0] + size.width / 2.0
    y: Final = position[1] - size.height / 2.0 - size.depth / 2.0
    return rf"\node{_options(color)} at ({x}pt, {y}pt) {{{text}}};" + "\n"


def _margin_from_text(text: str) -> float:
    text_size: Final = measure_latex_dimensions(text if text else "Placeholder")
    return text_size.total_height + _TEXT_MARGIN * 2.0


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
    def __init__(self, text: str, color: Optional[str] = None) -> None:
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
        text_size: Final = measure_latex_dimensions(self._text)
        text_x: Final = position[0] + _TEXT_MARGIN
        text_y: Final = position[1] - size[1] / 2.0 + text_size.height / 2.0
        return _rectangle(x1, y1, x2, y2, self._color) + _text(
            (text_x, text_y), self._text, self._color
        )

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
    def __init__(self, text: str, inner: Symbol) -> None:
        self._text = text
        self._inner = inner

    @property
    def text(self) -> str:
        return self._text

    @property
    def inner(self) -> Symbol:
        return self._inner

    @override
    def emit(self, position: tuple[float, float], size: tuple[float, float]) -> str:
        margin: Final = _margin_from_text(self._text)
        return (
            Imperative("").emit(position, size)
            + _text(
                (position[0] + _TEXT_MARGIN, position[1] - _TEXT_MARGIN), self._text
            )
            + self._inner.emit(
                (position[0] + margin, position[1] - margin),
                (size[0] - 2.0 * margin, size[1] - 2.0 * margin),
            )
        )

    @override
    @property
    def required_size(self) -> tuple[float, float]:
        margin: Final = _margin_from_text(self._text)
        inner_size: Final = self._inner.required_size
        return (
            inner_size[0] + 2.0 * margin,
            inner_size[1] + 2.0 * margin,
        )


@final
class Serial(Symbol):
    def __init__(self, elements: list[Symbol]) -> None:
        self._elements = elements

    @property
    def elements(self) -> list[Symbol]:
        return self._elements

    @override
    def emit(self, position: tuple[float, float], size: tuple[float, float]) -> str:
        output = ""
        element_size: Final = size[0], size[1] / len(self._elements)
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


@final
class Branch(NamedTuple):
    condition: str
    inner: Symbol


class MultipleExclusiveSelective(Symbol):
    _MIN_BRANCH_WIDTH = 28.346  # 1 cm in points

    def __init__(self, common_condition_part: str, branches: list[Branch]) -> None:
        self._common_condition_part = common_condition_part
        self._branches = branches

    @property
    def common_condition_part(self) -> str:
        return self._common_condition_part

    @property
    def branches(self) -> list[Branch]:
        return self._branches

    def _get_x_of_branch(self, position: tuple[float, float], index: int) -> float:
        common_condition_width: Final = measure_latex_dimensions(self._common_condition_part).width
        min_branch_width: Final = common_condition_width / len(self.branches) * 2.0
        x = position[0]
        for i, branch in enumerate(self.branches):
            if i == index:
                return x
            x += max(
                branch.inner.required_size[0],
                MultipleExclusiveSelective._MIN_BRANCH_WIDTH,
                measure_latex_dimensions(branch.condition).width * 2.0,
                min_branch_width,
            )
        return x

    @override
    def emit(self, position: tuple[float, float], size: tuple[float, float]) -> str:
        result = Imperative("").emit(position, (size[0], self._header_height))
        # branch_width: Final = size[0] / len(self.branches)
        branch_height: Final = size[1] - self._header_height

        # Diagonal line from top left to bottom "almost" right.
        x1: Final = position[0]
        y1: Final = position[1]
        # x2: Final = position[0] + (len(self.branches) - 1) * branch_width
        x2: Final = self._get_x_of_branch(position, len(self.branches) - 1)
        y2: Final = position[1] - self._header_height

        def linear_function(x: float) -> float:
            m: Final = (y2 - y1) / (x2 - x1)
            b: Final = y1 - m * x1
            return m * x + b

        x3: Final = position[0] + size[0]
        y3: Final = position[1]
        result += _line(x1, y1, x2, y2)
        result += _line(x2, y2, x3, y3)

        # Vertical lines in the header.
        for i in range(len(self.branches) - 2):
            x = position[0] + self._get_x_of_branch(position, i + 1)
            result += _line(x, linear_function(x), x, position[1] - self._header_height)

        # Condition texts in the header.
        for i in range(len(self.branches) - 1):
            text = self.branches[i].condition
            text_dimensions = measure_latex_dimensions(text)
            x_min = self._get_x_of_branch(position, i) + _TEXT_MARGIN
            if len(self.branches) == 2:
                x = x_min
            else:
                x_center_of_branch = (
                    self._get_x_of_branch(position, i)
                    + self._get_x_of_branch(position, i + 1)
                ) / 2.0
                x_center_of_text = x_center_of_branch - text_dimensions.width / 2.0
                t = i / max(len(self.branches) - 2, 1)
                x = _lerp(x_center_of_text, x_min, t)
            result += _text(
                (
                    x,
                    position[1]
                    - self._header_height
                    + _TEXT_MARGIN
                    + text_dimensions.height,
                ),
                text,
            )

        # Rightmost condition text.
        text = self.branches[-1].condition
        text_dimensions = measure_latex_dimensions(text)
        result += _text(
            (
                position[0] + size[0] - text_dimensions.width - _TEXT_MARGIN,
                position[1]
                - self._header_height
                + _TEXT_MARGIN
                + text_dimensions.height,
            ),
            text,
        )

        # Common condition part text.
        m_x: Final = (
            position[0] + size[0] / 2.0 + position[0] + size[0] / 2.0 + x2
        ) / 3.0
        m_y: Final = (position[1] + position[1] + y2) / 3.0
        text = self.common_condition_part
        text_dimensions = measure_latex_dimensions(text)
        result += _text(
            (
                m_x - text_dimensions.width / 2.0,
                m_y + text_dimensions.height / 2.0 + text_dimensions.depth / 2.0,
            ),
            text,
        )

        # Emit branches.
        for i, branch in enumerate(self.branches):
            current_position = (
                self._get_x_of_branch(position, i),
                position[1] - self._header_height,
            )
            branch_width = self._get_x_of_branch(position, i + 1) - current_position[0]
            result += branch.inner.emit(current_position, (branch_width, branch_height))
        return result

    @override
    @property
    def required_size(self) -> tuple[float, float]:
        return self._total_width, self._total_height

    @property
    def _header_height(self) -> float:
        max_line_height: Final = max(
            measure_latex_dimensions(self.common_condition_part).total_height,
            max(
                measure_latex_dimensions(condition.condition).total_height
                for condition in self.branches
            ),
        )
        return len(self.branches) * (max_line_height + 2.0 * _TEXT_MARGIN)

    @property
    def _body_height(self) -> float:
        return max(condition.inner.required_size[1] for condition in self.branches)

    @property
    def _total_height(self) -> float:
        return self._header_height + self._body_height

    @property
    def _total_width(self) -> float:
        return self._get_x_of_branch((0.0, 0.0), len(self.branches))


class DyadicSelective(MultipleExclusiveSelective):
    @override
    def __init__(self, common_condition_part: str, then: Branch, else_: Branch) -> None:
        super().__init__(common_condition_part, [then, else_])


@final
class MonadicSelective(DyadicSelective):
    @override
    def __init__(self, common_condition_part: str, then: Branch) -> None:
        super().__init__(common_condition_part, then, Branch("", Imperative("")))


@final
class BlockAlignment(Enum):
    TOP = auto()
    CENTER = auto()
    BOTTOM = auto()


class Iteration(Symbol):
    def __init__(self, condition: str, body: Symbol) -> None:
        self._condition = condition
        self._body = body

    @abstractmethod
    def _block_alignment(self) -> BlockAlignment:
        pass

    @property
    def condition(self) -> str:
        return self._condition

    @property
    def body(self) -> Symbol:
        return self._body

    @override
    def emit(self, position: tuple[float, float], size: tuple[float, float]) -> str:
        margin: Final = _margin_from_text(self._condition)
        inner_height: Final = (
            size[1] - 2.0 * margin
            if self._block_alignment() == BlockAlignment.CENTER
            else size[1] - margin
        )
        inner_position_y: Final = (
            position[1]
            if self._block_alignment() == BlockAlignment.TOP
            else position[1] - margin
        )

        if self._block_alignment() == BlockAlignment.TOP:
            text_dimensions: Final = measure_latex_dimensions(self._condition)
            text_position_y = (
                position[1] - size[1] + text_dimensions.height + _TEXT_MARGIN
            )
        else:
            text_position_y = position[1] - _TEXT_MARGIN

        return (
            Imperative("").emit(position, size)
            + _text(
                (position[0] + _TEXT_MARGIN, text_position_y),
                self._condition,
            )
            + self._body.emit(
                (position[0] + margin, inner_position_y),
                (size[0] - margin, inner_height),
            )
        )

    @override
    @property
    def required_size(self) -> tuple[float, float]:
        margin: Final = _margin_from_text(self._condition)
        inner_size: Final = self._body.required_size
        return (
            inner_size[0] + margin,
            inner_size[1] + margin * 2.0
            if self._block_alignment() == BlockAlignment.CENTER
            else 1.0,
        )


@final
class PreTestedIteration(Iteration):
    @override
    def _block_alignment(self) -> BlockAlignment:
        return BlockAlignment.BOTTOM


@final
class PostTestedIteration(Iteration):
    @override
    def _block_alignment(self) -> BlockAlignment:
        return BlockAlignment.TOP


@final
class ContinuousIteration(Iteration):
    @override
    def __init__(self, body: Symbol) -> None:
        super().__init__("", body)

    @override
    def _block_alignment(self) -> BlockAlignment:
        return BlockAlignment.CENTER


@final
class Termination(Symbol):
    def __init__(self, text: str) -> None:
        self._text = text

    @property
    def text(self) -> str:
        return self._text

    @override
    def emit(self, position: tuple[float, float], size: tuple[float, float]) -> str:
        text_dimensions: Final = measure_latex_dimensions(self._text)
        x: Final = position[0] + self._margin
        y: Final = position[1] - size[1] / 2.0 + text_dimensions.height / 2.0
        return (
            Imperative("").emit(position, size)
            + _text((x, y), self._text)
            + _line(
                position[0] + self._margin,
                position[1],
                position[0],
                position[1] - size[1] / 2.0,
            )
            + _line(
                position[0],
                position[1] - size[1] / 2.0,
                position[0] + self._margin,
                position[1] - size[1],
            )
        )

    @override
    @property
    def required_size(self) -> tuple[float, float]:
        size: Final = Imperative(self._text).required_size
        return (
            size[0] + self._margin,
            size[1],
        )

    @property
    def _margin(self) -> float:
        return _margin_from_text("")


@final
class Parallel(Symbol):
    def __init__(self, elements: list[Symbol]) -> None:
        self._elements = elements

    @property
    def elements(self) -> list[Symbol]:
        return self._elements

    @override
    def emit(self, position: tuple[float, float], size: tuple[float, float]) -> str:
        output = Imperative("").emit(position, (size[0], self._margin))
        output += Imperative("").emit(
            (position[0], position[1] - size[1] + self._margin),
            (size[0], self._margin),
        )
        output += _line(
            position[0],
            position[1] - self._margin,
            position[0] + self._margin,
            position[1],
        )
        output += _line(
            position[0],
            position[1] - size[1] + self._margin,
            position[0] + self._margin,
            position[1] - size[1],
        )
        output += _line(
            position[0] + size[0] - self._margin,
            position[1],
            position[0] + size[0],
            position[1] - self._margin,
        )
        output += _line(
            position[0] + size[0] - self._margin,
            position[1] - size[1],
            position[0] + size[0],
            position[1] - size[1] + self._margin,
        )
        element_width: Final = size[0] / len(self._elements)
        element_height: Final = size[1] - 2.0 * self._margin
        position = (position[0], position[1] - self._margin)
        for element in self._elements:
            output += element.emit(
                (position[0], position[1]),
                (element_width, element_height),
            )
            position = (position[0] + element_width, position[1])
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
        return max_width * len(self.elements), max_height + 2.0 * self._margin

    @property
    def _margin(self) -> float:
        return _margin_from_text("")

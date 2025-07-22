from typing import final


@final
class Dimensions:
    _width: float
    _height: float
    _depth: float

    def __init__(self, width: float, height: float, depth: float) -> None:
        self._width = width
        self._height = height
        self._depth = depth

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @property
    def depth(self) -> float:
        return self._depth

    @property
    def total_height(self) -> float:
        return self.height + self.depth

from typing import final, Optional, Final

from nassi_shneiderman_generator.symbols import Symbol


@final
class Diagram:
    def __init__(self, contents: Symbol, min_width: float = 80.0) -> None:
        self._contents = contents
        self._min_width = min_width

    def emit(self) -> str:
        result = "\\begin{tikzpicture}\n"
        required_size: Final = self._contents.required_size
        result += self._contents.emit(
            position=(0, 0),
            size=(max(self._min_width, required_size[0]), required_size[1]),
        )
        result += "\\end{tikzpicture}\n"
        return result

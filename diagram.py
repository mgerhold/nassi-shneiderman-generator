from typing import final

from symbols import Symbol


@final
class Diagram:
    def __init__(self, contents: Symbol) -> None:
        self._contents = contents

    def emit(self) -> str:
        result = "\\begin{tikzpicture}\n"
        result += self._contents.emit(
            position=(0, 0), size=self._contents.required_size
        )
        result += "\\end{tikzpicture}\n"
        return result

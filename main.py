from typing import Final

from diagram import Diagram
from latex import render_latex_and_show
from symbols import Imperative, Serial, Block


def main():
    diagram: Final = Diagram(
        Block(
            text="Mein Block",
            inner=Serial(
                elements=[
                    Imperative(r"Eingabe: \texttt{n}"),
                    Imperative(r"$\texttt{n} := \texttt{n} + 1$"),
                    Imperative(r"Was geht ab? $\frac{1}{2}$"),
                    Imperative(r"a"),
                    Imperative(r"-"),
                ]
            )
        )
    )
    latex_code: Final = diagram.emit()
    print(latex_code)
    render_latex_and_show(latex_code)

    # print(measure_latex_dimensions("Hello, world!"))
    # render_latex_and_show(r"Hello, world! $\frac{1}{2} \cdot \texttt{GEIER!!!}$")


if __name__ == "__main__":
    main()

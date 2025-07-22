from symbols import Termination
from symbols import ContinuousIteration
from symbols import PostTestedIteration
from symbols import PreTestedIteration
from symbols import MonadicSelective, DyadicSelective
from typing import Final

from diagram import Diagram
from latex import render_latex_and_show
from symbols import Imperative, Serial, Block, MultipleExclusiveSelective, Branch


def main():
    diagram: Final = Diagram(
        MultipleExclusiveSelective(
            common_condition_part="Weiß der Geier?",
            branches=[
                Branch(
                    condition="Ja",
                    inner=MonadicSelective(
                        common_condition_part="War geil?",
                        then=Branch(
                            condition="Ja",
                            inner=Serial(
                                elements=[
                                    Imperative("Dann!"),
                                    Imperative("Auch."),
                                    Imperative("Und!"),
                                ]
                            ),
                        ),
                    ),
                ),
                Branch(
                    condition="Vielleicht",
                    inner=DyadicSelective(
                        common_condition_part="Wie geht's?",
                        then=Branch(
                            condition="Gut",
                            inner=Imperative("Okay."),
                        ),
                        else_=Branch(
                            condition="Schlecht",
                            inner=Imperative("Ciao."),
                        ),
                    ),
                ),
                Branch(
                    condition="Nein",
                    inner=PreTestedIteration(
                        condition=r"$\texttt{n} < 10$",
                        body=Serial(
                            elements=[
                                Imperative(r"Ausgabe: \texttt{n}"),
                                Imperative(r"$\texttt{n} := \texttt{n} + 1$"),
                            ]
                        ),
                    ),
                ),
                Branch(
                    condition="Bla",
                    inner=PostTestedIteration(
                        condition=r"$\texttt{n} < 10$",
                        body=Serial(
                            elements=[
                                Imperative(r"Ausgabe: \texttt{n}"),
                                Imperative(r"$\texttt{n} := \texttt{n} + 1$"),
                            ]
                        ),
                    )
                ),
                Branch(
                    condition="Huh?",
                    inner=ContinuousIteration(
                        body=Serial(
                            elements=[
                                Imperative(r"Ausgabe: \texttt{n}"),
                                Imperative(r"$\texttt{n} := \texttt{n} + 1$"),
                                Termination("Raus hier!"),
                            ]
                        ),
                    )
                ),
                Branch(
                    condition="Nein",
                    inner=Block(
                        text="Mein Block",
                        inner=Serial(
                            elements=[
                                Imperative(r"Eingabe: \texttt{n}"),
                                Imperative(r"$\texttt{n} := \texttt{n} + 1$"),
                                Imperative(r"Was geht ab? $\frac{1}{2}$"),
                                Imperative(r"a"),
                                Imperative(r"-"),
                            ]
                        ),
                    ),
                ),
            ],
        ),
    )
    latex_code: Final = diagram.emit()
    print(latex_code)
    render_latex_and_show(latex_code)

    # print(measure_latex_dimensions("Hello, world!"))
    # render_latex_and_show(r"Hello, world! $\frac{1}{2} \cdot \texttt{GEIER!!!}$")


if __name__ == "__main__":
    main()

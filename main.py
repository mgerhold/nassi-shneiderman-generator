from symbols import Parallel
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
    # diagram: Final = Diagram(
    #     DyadicSelective(
    #         r"$\texttt{n} > 0?$",
    #         Branch("Ja", Imperative(r"Ausgabe: $\texttt{n} > 0$")),
    #         Branch(
    #             "Nein",
    #             DyadicSelective(
    #                 r"$\texttt{n} > 1?$",
    #                 Branch("Ja", Imperative(r"Ausgabe: $\texttt{n} > 1$")),
    #                 Branch(
    #                     "Nein",
    #                     DyadicSelective(
    #                         r"$\texttt{n} > 2?$",
    #                         Branch("Ja", Imperative(r"Ausgabe: $\texttt{n} > 2$")),
    #                         Branch(
    #                             "Nein",
    #                             DyadicSelective(
    #                                 r"$\texttt{n} > 3?$",
    #                                 Branch("Ja", Imperative(r"Ausgabe: $\texttt{n} > 3$")),
    #                                 Branch(
    #                                     "Nein",
    #                                     DyadicSelective(
    #                                         r"$\texttt{n} > 4?$",
    #                                         Branch("Ja", Imperative(r"Ausgabe: $\texttt{n} > 4$")),
    #                                         Branch(
    #                                             "Nein",
    #                                             Imperative(r"Ausgabe: $\texttt{n} \leq 4$"),
    #                                         ),
    #                                     )
    #                                 ),
    #                             )
    #                         ),
    #                     )
    #                 )
    #             )
    #         )
    #     )
    # )
    diagram: Final = Diagram(
        MultipleExclusiveSelective(
            "Weiß der Geier?",
            [
                Branch(
                    "Ja",
                    MonadicSelective(
                        "War geil?",
                        Branch(
                            "Ja",
                            Serial(
                                [
                                    Imperative("Dann!"),
                                    Imperative("Auch."),
                                    Imperative("Und!"),
                                ]
                            ),
                        ),
                    ),
                ),
                Branch(
                    "Vielleicht",
                    DyadicSelective(
                        "Wie geht's?",
                        Branch(
                            "Gut",
                            Imperative("Okay."),
                        ),
                        Branch(
                            "Schlecht",
                            Imperative("Ciao."),
                        ),
                    ),
                ),
                Branch(
                    "Nein",
                    PreTestedIteration(
                        r"$\texttt{n} < 10$",
                        Serial(
                            [
                                Imperative(r"Ausgabe: \texttt{n}"),
                                Imperative(r"$\texttt{n} := \texttt{n} + 1$"),
                            ]
                        ),
                    ),
                ),
                Branch(
                    "Bla",
                    PostTestedIteration(
                        r"$\texttt{n} < 10$",
                        Serial(
                            [
                                Imperative(r"Ausgabe: \texttt{n}"),
                                Imperative(r"$\texttt{n} := \texttt{n} + 1$"),
                            ]
                        ),
                    ),
                ),
                Branch(
                    "Huh?",
                    ContinuousIteration(
                        Serial(
                            [
                                Imperative(r"Ausgabe: \texttt{n}"),
                                Imperative(r"$\texttt{n} := \texttt{n} + 1$"),
                                Termination("Raus hier!"),
                                Parallel(
                                    [
                                        Imperative("a"),
                                        Imperative("b"),
                                        Imperative("c"),
                                    ]
                                ),
                            ]
                        ),
                    ),
                ),
                Branch(
                    "Nein",
                    Block(
                        "Mein Block",
                        Serial(
                            [
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

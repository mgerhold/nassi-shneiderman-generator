from typing import Final

from nassi_shneiderman_generator.diagram import Diagram
from nassi_shneiderman_generator.symbols import (
    Branch,
    Block,
    Serial,
    Imperative,
    PostTestedIteration,
    ContinuousIteration,
    Termination,
    Parallel,
    MultipleExclusiveSelective,
    MonadicSelective,
    DyadicSelective,
    PreTestedIteration,
)

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
                "Blubb",
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

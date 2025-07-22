from nassi_shneiderman_generator.symbols import Imperative
from nassi_shneiderman_generator.symbols import Serial
from nassi_shneiderman_generator.symbols import ContinuousIteration
from nassi_shneiderman_generator.diagram import Diagram
from typing import Final

diagram: Final = Diagram(
    ContinuousIteration(
        Serial(
            [
                Imperative(r"$\texttt{n} := \texttt{n} + 2$"),
                Imperative(r"Ausgabe: $\texttt{n}$"),
            ]
        )
    )
)

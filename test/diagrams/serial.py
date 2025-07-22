from nassi_shneiderman_generator.diagram import Diagram
from nassi_shneiderman_generator.symbols import Imperative
from nassi_shneiderman_generator.symbols import Serial
from typing import Final

diagram: Final = Diagram(
    Serial(
        [
            Imperative(r"Eingabe: \texttt{x}"),
            Imperative(r"$\texttt{x} := \texttt{x} \cdot 2$"),
            Imperative(r"Ausgabe: \texttt{x}"),
        ]
    )
)

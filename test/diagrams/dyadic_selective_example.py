from nassi_shneiderman_generator.symbols import Serial
from nassi_shneiderman_generator.symbols import Imperative
from nassi_shneiderman_generator.diagram import Diagram
from typing import Final

from nassi_shneiderman_generator.symbols import DyadicSelective, Branch

diagram: Final = Diagram(
    DyadicSelective(
        r"Wert von \texttt{x}",
        Branch(r"$\leq 3$", Imperative(r"$\texttt{x} := \texttt{x} + 2$")),
        Branch(
            "$> 3$",
            Serial(
                [
                    Imperative(r"$\texttt{x} := \texttt{x} + \texttt{y}$"),
                    Imperative(r"$\texttt{z} := \texttt{y} \cdot 2$"),
                ]
            ),
        ),
    )
)

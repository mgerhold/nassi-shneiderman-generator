from nassi_shneiderman_generator.symbols import Termination
from nassi_shneiderman_generator.symbols import MonadicSelective, Branch
from nassi_shneiderman_generator.symbols import Imperative
from nassi_shneiderman_generator.symbols import Serial
from nassi_shneiderman_generator.symbols import PreTestedIteration
from nassi_shneiderman_generator.diagram import Diagram
from typing import Final

diagram: Final = Diagram(
    PreTestedIteration(
        r"Schleife: $\texttt{n} < 100$",
        Serial(
            [
                Imperative(r"\texttt{n} := \texttt{n} + 2"),
                MonadicSelective(
                    r"wenn Wert von \texttt{n}",
                    Branch("$> 95$", Termination("Schleife")),
                ),
                Imperative(r"Ausgabe: \texttt{n}"),
            ]
        ),
    )
)

from typing import Final
from nassi_shneiderman_generator.diagram import Diagram
from nassi_shneiderman_generator.symbols import Serial, Imperative, PreTestedIteration


diagram: Final = Diagram(
    Serial([
        Imperative(r"Eingabe: \texttt{principal}, \texttt{interest\_rate}"),
        Imperative(r"$\texttt{years} := 0$"),
        Imperative(r"$\texttt{balance} := 0$"),
        PreTestedIteration(
            r"Wiederhole, solange $\texttt{balance} < 2 \cdot \texttt{principal}$",
            Serial([
                Imperative(r"$\texttt{years} := \texttt{years} + 1$"),
                Imperative(r"$\texttt{balance} := \texttt{balance} \cdot (1 + \texttt{interest\_rate})$"),
            ])
        ),
        Imperative(r"Ausgabe: \texttt{years}"),
    ])
)

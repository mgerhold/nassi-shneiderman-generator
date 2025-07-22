from typing import Final

from nassi_shneiderman_generator.diagram import Diagram
from nassi_shneiderman_generator.symbols import DyadicSelective, Imperative, Branch

diagram: Final = Diagram(
    DyadicSelective(
        r"$\texttt{n} > 0?$",
        Branch("Ja", Imperative(r"Ausgabe: $\texttt{n} > 0$")),
        Branch(
            "Nein",
            DyadicSelective(
                r"$\texttt{n} > 1?$",
                Branch("Ja", Imperative(r"Ausgabe: $\texttt{n} > 1$")),
                Branch(
                    "Nein",
                    DyadicSelective(
                        r"$\texttt{n} > 2?$",
                        Branch("Ja", Imperative(r"Ausgabe: $\texttt{n} > 2$")),
                        Branch(
                            "Nein",
                            DyadicSelective(
                                r"$\texttt{n} > 3?$",
                                Branch("Ja", Imperative(r"Ausgabe: $\texttt{n} > 3$")),
                                Branch(
                                    "Nein",
                                    DyadicSelective(
                                        r"$\texttt{n} > 4?$",
                                        Branch(
                                            "Ja",
                                            Imperative(r"Ausgabe: $\texttt{n} > 4$"),
                                        ),
                                        Branch(
                                            "Nein",
                                            Imperative(r"Ausgabe: $\texttt{n} \leq 4$"),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
)

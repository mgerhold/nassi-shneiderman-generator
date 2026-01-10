from nassi_shneiderman_generator.symbols import (
    Termination,
    Imperative,
    Serial,
    PreTestedIteration,
    DyadicSelective,
)
from nassi_shneiderman_generator.symbols import Branch
from nassi_shneiderman_generator.diagram import Diagram
from typing import Final

diagram: Final = Diagram(
    Serial(
        elements=[
            Imperative("This is a very, very long imperative that takes up a lot of horizontal space"),
            DyadicSelective(
                    r"\texttt{did\_swap} = \texttt{false}?",
                    then=Branch("ja", Imperative("test")),
                    else_=Branch(
                        condition="nein",
                        inner=Imperative("test"),
                    ),
                ),
        ]
    )
)

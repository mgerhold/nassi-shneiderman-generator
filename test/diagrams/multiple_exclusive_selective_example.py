from nassi_shneiderman_generator.symbols import Imperative, Branch
from nassi_shneiderman_generator.diagram import Diagram
from typing import Final

from nassi_shneiderman_generator.symbols import MultipleExclusiveSelective

diagram: Final = Diagram(
    MultipleExclusiveSelective(
        "gedrückte Taste",
        [
            Branch(
                "W",
                Imperative("Ausgabe: oben"),
            ),
            Branch(
                "A",
                Imperative("Ausgabe: links"),
            ),
            Branch(
                "S",
                Imperative("Ausgabe: unten"),
            ),
            Branch(
                "D",
                Imperative("Ausgabe: rechts"),
            ),
        ],
    )
)

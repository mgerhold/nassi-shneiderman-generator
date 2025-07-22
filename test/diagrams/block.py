from nassi_shneiderman_generator.symbols import Imperative
from nassi_shneiderman_generator.symbols import Serial, Block
from nassi_shneiderman_generator.diagram import Diagram
from typing import Final

diagram: Final = Diagram(
    Serial(
        [
            Block(
                "Block 1",
                Serial(
                    [
                        Imperative("Verarbeitung 1"),
                        Imperative("Verarbeitung 2"),
                        Imperative("Verarbeitung 3"),
                    ]
                ),
            ),
            Block(
                "Block 2",
                Serial(
                    [
                        Imperative("Verarbeitung 4"),
                        Imperative("Verarbeitung 5"),
                        Imperative("Verarbeitung 6"),
                    ]
                ),
            ),
        ]
    )
)

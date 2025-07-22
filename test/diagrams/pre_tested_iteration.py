from nassi_shneiderman_generator.symbols import Imperative
from nassi_shneiderman_generator.symbols import PreTestedIteration
from nassi_shneiderman_generator.diagram import Diagram
from typing import Final

diagram: Final = Diagram(
    PreTestedIteration(
        "B",
        Imperative("V"),
    )
)

from nassi_shneiderman_generator.symbols import Imperative
from nassi_shneiderman_generator.symbols import PostTestedIteration
from nassi_shneiderman_generator.diagram import Diagram
from typing import Final

diagram: Final = Diagram(
    PostTestedIteration(
        "B",
        Imperative("V"),
    )
)

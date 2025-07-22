from nassi_shneiderman_generator.symbols import Imperative
from nassi_shneiderman_generator.symbols import Branch
from nassi_shneiderman_generator.diagram import Diagram
from typing import Final

from nassi_shneiderman_generator.symbols import DyadicSelective

diagram: Final = Diagram(
    DyadicSelective(
        "gemeinsamer Bedingungsteil",
        Branch("Bedingung 1", Imperative("Verarbeitung 1")),
        Branch("Bedingung 2", Imperative("Verarbeitung 2")),
    )
)

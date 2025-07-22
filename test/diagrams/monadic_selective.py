from nassi_shneiderman_generator.symbols import Imperative
from nassi_shneiderman_generator.symbols import Branch
from nassi_shneiderman_generator.symbols import MonadicSelective
from nassi_shneiderman_generator.diagram import Diagram
from typing import Final

diagram: Final = Diagram(
    MonadicSelective(
        "gemeinsamer Bedingungsteil", Branch("Bedingung", Imperative("Verarbeitung"))
    )
)

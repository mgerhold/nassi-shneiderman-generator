from nassi_shneiderman_generator.symbols import Imperative
from nassi_shneiderman_generator.symbols import Branch
from nassi_shneiderman_generator.diagram import Diagram
from typing import Final

from nassi_shneiderman_generator.symbols import MultipleExclusiveSelective

diagram: Final = Diagram(
    MultipleExclusiveSelective(
        "gemeinsamer Bedingungsteil",
        [
            Branch(
                "$B_1$",
                Imperative("$V_1$"),
            ),
            Branch(
                "$...$",
                Imperative("$...$"),
            ),
            Branch(
                "$B_{n-1}$",
                Imperative("$V_{n-1}$"),
            ),
            Branch(
                "$B_n$",
                Imperative("$V_n$"),
            ),
        ],
    )
)

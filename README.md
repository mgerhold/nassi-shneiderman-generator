# Nassi-Shneiderman Diagram Generator

A Python program for generating Nassi-Shneiderman diagrams (also known as structograms) with LaTeX rendering to PDF output.

## Features

- Generate structured diagrams using Python code
- Support for all major Nassi-Shneiderman diagram elements
- Automatic PDF generation
- Batch processing of multiple diagram files

## Supported Diagram Elements

### Basic Elements
- **Imperative**: Simple action blocks
- **Block**: Named blocks containing other elements
- **Serial**: Sequential execution of multiple elements

### Control Flow
- **MonadicSelective**: If structures  
- **DyadicSelective**: If-then-else structures
- **MultipleExclusiveSelective**: Switch-case like structures with multiple branches

### Iterations
- **PreTestedIteration**: While loops (condition tested at start)
- **PostTestedIteration**: Do-while loops (condition tested at end)
- **ContinuousIteration**: Infinite loops

### Special Elements
- **Termination**: Break/exit statements
- **Parallel**: Concurrent execution blocks

## Usage

### Creating Diagrams

Create Python files that define a `diagram` variable containing your Nassi-Shneiderman structure:

```python
from typing import Final
from nassi_shneiderman_generator.diagram import Diagram
from nassi_shneiderman_generator.symbols import DyadicSelective, Imperative, Branch

diagram: Final = Diagram(
    DyadicSelective(
        r"$\texttt{n} > 0?$",
        Branch("Ja", Imperative(r"Ausgabe: $\texttt{n} > 0$")),
        Branch("Nein", Imperative(r"Ausgabe: $\texttt{n} \leq 0$"))
    )
)
```

### Generating PDFs

Use the command-line interface to process your diagram files:

```bash
python main.py <folder_path>
```

Options:
- `--force-recreate`: Force regeneration of all .tex and .pdf files

### Example: Complex Diagram

```python
from typing import Final
from nassi_shneiderman_generator.diagram import Diagram
from nassi_shneiderman_generator.symbols import *

diagram: Final = Diagram(
    MultipleExclusiveSelective(
        "Input value",
        [
            Branch("< 0", Imperative("Handle negative")),
            Branch("= 0", Imperative("Handle zero")),
            Branch("> 0", 
                PreTestedIteration(
                    r"$\texttt{i} < \texttt{n}$",
                    Serial([
                        Imperative(r"Process $\texttt{i}$"),
                        Imperative(r"$\texttt{i} := \texttt{i} + 1$")
                    ])
                )
            )
        ]
    )
)
```

## LaTeX Integration

The generator uses LaTeX with TikZ for rendering. You can use LaTeX mathematical notation and formatting in your text:

- Mathematical expressions: `r"$\texttt{variable} > 0$"`
- Text formatting: `r"\textbf{bold text}"`
- Special characters: Use LaTeX escape sequences

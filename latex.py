from typing import Final
import subprocess
import tempfile
import re
from pathlib import Path
import cv2


def measure_latex_dimensions(latex_code: str) -> tuple[float, float]:
    file_contents: Final = rf"""\documentclass{{article}}
    \usepackage[margin=0pt,paperwidth=50cm,paperheight=50cm]{{geometry}}
    \usepackage{{calc}}
    \pagestyle{{empty}}

    \begin{{document}}
        \newsavebox{{\mybox}}
        \savebox{{\mybox}}{{{latex_code}}}
        \typeout{{DIMENSIONS: \the\wd\mybox\space\the\ht\mybox\space\the\dp\mybox}}
        \usebox{{\mybox}}
    \end{{document}}
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        tex_file: Final = Path(temp_dir) / "measure.tex"
        tex_file.write_text(file_contents, encoding="utf-8")

        try:
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", str(tex_file)],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=30,
            )

            pattern: Final = r"DIMENSIONS: ([0-9.]+)pt ([0-9.]+)pt ([0-9.]+)pt"
            match = re.search(pattern, result.stdout)

            if match:
                width = float(match.group(1))
                height = float(match.group(2))
                depth = float(match.group(3))
                total_height = height + depth
                return width, total_height
            raise RuntimeError("Failed to extract dimensions from LaTeX output.")
        except subprocess.TimeoutExpired:
            raise RuntimeError("pdflatex timed out")
        except FileNotFoundError:
            raise RuntimeError("pdflatex is not installed or not found in PATH")


def _show_image(path: str) -> None:
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    cv2.imshow("LaTeX Output", img)  # type: ignore
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def render_latex_and_show(latex_body: str):
    # Create temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir).resolve()
        tex_file = tmp_path / "doc.tex"
        pdf_file = tmp_path / "doc.pdf"
        png_file = tmp_path / "doc.png"  # output of pdftoppm

        # LaTeX document template
        full_tex = (
            r"""\documentclass[tikz]{standalone}
\usepackage{tikz}
\begin{document}
"""
            + latex_body
            + r"""
\end{document}
"""
        )

        # Write LaTeX to file
        tex_file.write_text(full_tex, encoding="utf-8")

        # Run pdflatex
        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", str(tex_file)],
                cwd=tmp_path,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            print("LaTeX compilation failed.")
            return

        try:
            subprocess.run(
                ["pdfcrop", str(pdf_file), str(pdf_file)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            print("PDF cropping failed.")
            return

        # Convert PDF to PNG
        try:
            subprocess.run(
                [
                    "pdftoppm",
                    "-png",
                    "-singlefile",
                    str(pdf_file),
                    str(tmp_path / "doc"),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            print("PDF to PNG conversion failed.")
            return

        # Open image
        try:
            _show_image(str(png_file))
        except Exception as e:
            print("Failed to open image:", e)

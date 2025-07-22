from nassi_shneiderman_generator.latex import render_latex_to_pdf
import argparse
import sys
from pathlib import Path


def python_file_to_latex(py_file: Path) -> str:
    namespace = {}

    with open(py_file, "r", encoding="utf-8") as f:
        exec(f.read(), namespace)

    if "diagram" not in namespace:
        raise AttributeError(f"No 'diagram' object found in '{py_file.name}'")

    diagram = namespace["diagram"]

    if not hasattr(diagram, "emit"):
        raise AttributeError(
            f"'diagram' object in '{py_file.name}' does not have an 'emit' method"
        )

    return diagram.emit()


def find_and_evaluate_diagrams(folder_path: Path) -> None:
    if not folder_path.exists():
        raise FileNotFoundError(f"Error '{folder_path}' does not exist")

    if not folder_path.is_dir():
        raise NotADirectoryError(f"'{folder_path}' is not a directory")

    py_files = list(folder_path.glob("*.py"))

    if not py_files:
        print(f"No Python files found in '{folder_path}'", file=sys.stderr)
        return

    for py_file in py_files:
        try:
            tex_file = py_file.with_suffix(".tex")
            pdf_file = tex_file.with_suffix(".pdf")

            py_mtime = py_file.stat().st_mtime
            tex_mtime = tex_file.stat().st_mtime if tex_file.exists() else 0
            pdf_mtime = pdf_file.stat().st_mtime if pdf_file.exists() else 0

            # Skip processing if .py file is older than both .tex and .pdf
            if py_mtime <= max(tex_mtime, pdf_mtime):
                # Skipping file (no changes detected)
                continue

            tex_body = python_file_to_latex(py_file)

            tex_file.write_text(tex_body, encoding="utf-8")
            print(f"Processed '{py_file.name}' and saved to '{tex_file.name}'")

            render_latex_to_pdf(tex_body, pdf_file)
            print(f"Rendered PDF for '{py_file.name}' to '{pdf_file.name}'")

        except Exception as e:
            print(f"Error processing '{py_file.name}': {e}", file=sys.stderr)
            continue


def generate_diagrams(folder_path: Path) -> None:
    try:
        find_and_evaluate_diagrams(folder_path)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Path to the folder containing .py files")
    args = parser.parse_args()
    generate_diagrams(Path(args.folder))


if __name__ == "__main__":
    main()

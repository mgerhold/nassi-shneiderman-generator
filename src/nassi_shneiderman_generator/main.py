from nassi_shneiderman_generator.latex import render_latex_to_pdf
import argparse
import sys
from pathlib import Path


def find_and_evaluate_diagrams(folder_path: str) -> None:
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Error '{folder_path}' does not exist")

    if not folder.is_dir():
        raise NotADirectoryError(f"'{folder_path}' is not a directory")

    py_files = list(folder.glob("*.py"))

    if not py_files:
        print(f"No Python files found in '{folder_path}'", file=sys.stderr)
        return

    for py_file in py_files:
        try:
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

            new_filename = py_file.with_suffix(".tex")
            tex_body = diagram.emit()
            new_filename.write_text(tex_body, encoding="utf-8")
            print(f"Processed '{py_file.name}' and saved to '{new_filename}'")
            pdf_filename = new_filename.with_suffix(".pdf")
            render_latex_to_pdf(tex_body, pdf_filename)
            print(f"Rendered PDF for '{py_file.name}' to '{pdf_filename}'")
        except Exception as e:
            print(f"Error processing '{py_file.name}': {e}", file=sys.stderr)
            continue


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Path to the folder containing .py files")

    args = parser.parse_args()

    try:
        find_and_evaluate_diagrams(args.folder)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

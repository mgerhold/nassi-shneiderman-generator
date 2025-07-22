import pathlib

from nassi_shneiderman_generator.main import python_file_to_latex


def test_snapshots() -> None:
    test_dir = pathlib.Path(__file__).parent
    diagrams_dir = test_dir / "diagrams"
    diagrams_files = list(diagrams_dir.glob("*.py"))
    assert diagrams_files, "No diagram files found in test/diagrams."
    for diagram_file in diagrams_files:
        latex_code = python_file_to_latex(diagram_file)
        snapshot_file = diagram_file.with_suffix(".expected.tex")
        assert snapshot_file.exists(), f"Snapshot file {snapshot_file} does not exist."
        expected_contents = snapshot_file.read_text()
        assert latex_code == expected_contents, (
            f"Snapshot for {diagram_file} does not match expected contents.\n"
            f"Expected:\n{expected_contents}\n\n"
            f"Got:\n{latex_code}"
        )

from pathlib import Path

import pytest

from foundational_rag.ingestion.file_loader import FileLoader


def test_load_txt_file(tmp_path: Path) -> None:
    file_path = tmp_path / "lecture.txt"
    file_path.write_text(
        "Distributed systems coordinate multiple computers.",
        encoding="utf-8",
    )

    loader = FileLoader()

    result = loader.load(file_path)

    assert result == "Distributed systems coordinate multiple computers."


def test_unsupported_file_type_raises_error(tmp_path: Path) -> None:
    file_path = tmp_path / "lecture.csv"
    file_path.write_text("unsupported", encoding="utf-8")

    loader = FileLoader()

    with pytest.raises(ValueError, match="Unsupported file type: .csv"):
        loader.load(file_path)
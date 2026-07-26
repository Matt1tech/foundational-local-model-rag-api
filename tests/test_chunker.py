import pytest

from foundational_rag.ingestion.chunker import TextChunker


def test_split_creates_overlapping_chunks() -> None:
    chunker = TextChunker(chunk_size=10, chunk_overlap=2)

    chunks = chunker.split("abcdefghijklmnop")

    assert len(chunks) == 2
    assert chunks[0].content == "abcdefghij"
    assert chunks[1].content == "ijklmnop"
    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1


def test_split_returns_empty_list_for_blank_text() -> None:
    chunker = TextChunker()

    assert chunker.split("   ") == []


def test_overlap_must_be_smaller_than_chunk_size() -> None:
    with pytest.raises(
        ValueError,
        match="chunk_overlap must be smaller than chunk_size",
    ):
        TextChunker(chunk_size=100, chunk_overlap=100)
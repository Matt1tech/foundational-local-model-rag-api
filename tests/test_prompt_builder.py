import pytest

from foundational_rag.generation.prompt_builder import PromptBuilder
from foundational_rag.retrieval.retriever import RetrievedChunk


def test_build_prompt_includes_question_and_context() -> None:
    builder = PromptBuilder()

    chunks = [
        RetrievedChunk(
            content="Transactions follow ACID properties.",
            source="database_systems.pdf",
            chunk_index=2,
            score=0.91,
        )
    ]

    prompt = builder.build(
        question="What properties do transactions follow?",
        chunks=chunks,
    )

    assert "What properties do transactions follow?" in prompt
    assert "Transactions follow ACID properties." in prompt
    assert "database_systems.pdf" in prompt
    assert "using only the provided context" in prompt


def test_build_prompt_handles_no_chunks() -> None:
    builder = PromptBuilder()

    prompt = builder.build(
        question="What is a transaction?",
        chunks=[],
    )

    assert "No relevant context was found." in prompt


def test_empty_question_raises_error() -> None:
    builder = PromptBuilder()

    with pytest.raises(ValueError, match="Question cannot be empty"):
        builder.build(question=" ", chunks=[])
from dataclasses import dataclass

from foundational_rag.generation.generator import ResponseGenerator
from foundational_rag.generation.prompt_builder import PromptBuilder
from foundational_rag.retrieval.retriever import RetrievedChunk, Retriever


@dataclass
class RagResponse:
    """Represents a grounded RAG response."""

    answer: str
    sources: list[RetrievedChunk]


class RagService:
    """Runs the retrieval-augmented generation pipeline."""

    def __init__(
        self,
        retriever: Retriever,
        prompt_builder: PromptBuilder,
        generator: ResponseGenerator,
    ) -> None:
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.generator = generator

    def ask(self, question: str) -> RagResponse:
        """Retrieve context and generate a grounded answer."""

        chunks = self.retriever.retrieve(question)

        prompt = self.prompt_builder.build(
            question=question,
            chunks=chunks,
        )

        answer = self.generator.generate(prompt)

        return RagResponse(
            answer=answer,
            sources=chunks,
        )
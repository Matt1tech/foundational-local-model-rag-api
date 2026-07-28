import logging
from dataclasses import dataclass

from foundational_rag.generation.generator import ResponseGenerator
from foundational_rag.generation.prompt_builder import PromptBuilder
from foundational_rag.retrieval.retriever import RetrievedChunk, Retriever


logger = logging.getLogger(__name__)


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

        logger.info(
            "Starting RAG request: question_length=%d",
            len(question),
        )

        try:
            chunks = self.retriever.retrieve(question)

            logger.info(
                "Retrieval completed: chunks=%d",
                len(chunks),
            )

            prompt = self.prompt_builder.build(
                question=question,
                chunks=chunks,
            )

            answer = self.generator.generate(prompt)

            logger.info(
                "RAG response generated: "
                "answer_length=%d sources=%d",
                len(answer),
                len(chunks),
            )

            return RagResponse(
                answer=answer,
                sources=chunks,
            )

        except Exception:
            logger.exception(
                "RAG request failed: question_length=%d",
                len(question),
            )
            raise
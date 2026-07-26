from foundational_rag.retrieval.retriever import RetrievedChunk


class PromptBuilder:
    """Builds a grounded prompt from retrieved document chunks."""

    def build(
        self,
        question: str,
        chunks: list[RetrievedChunk],
    ) -> str:
        """Create a prompt using the question and retrieved context."""

        if not question.strip():
            raise ValueError("Question cannot be empty")

        context = "\n\n".join(
            f"[Source: {chunk.source}, Chunk: {chunk.chunk_index}]\n"
            f"{chunk.content}"
            for chunk in chunks
        )

        return f"""
You are a document-grounded assistant.

Your task is to answer the user's question using only the provided context.

Instructions:
1. Do not use outside knowledge.
2. Do not invent facts.
3. Base every claim on the provided context.
4. If the context does not contain enough information, respond:
   "I could not find enough information in the uploaded documents."
5. Keep the answer clear and concise.
6. When useful, mention the source document.
7. Do not mention chunk indexes unless the user asks for technical details.

Context:
{context}

Question:
{question}

Answer:
""".strip()
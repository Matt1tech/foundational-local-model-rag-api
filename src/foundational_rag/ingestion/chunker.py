from dataclasses import dataclass


@dataclass
class TextChunk:
    """Represents a chunk of text."""

    content: str
    chunk_index: int


class TextChunker:
    """Splits text into overlapping chunks."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ) -> None:
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> list[TextChunk]:
        """Split text into overlapping chunks."""

        if not text.strip():
            return []

        chunks: list[TextChunk] = []

        start = 0
        index = 0

        while start < len(text):
            end = start + self.chunk_size

            chunks.append(
                TextChunk(
                    content=text[start:end],
                    chunk_index=index,
                )
            )

            start += self.chunk_size - self.chunk_overlap
            index += 1

        return chunks
from ollama import Client


class EmbeddingService:
    """Generates vector embeddings using Ollama."""

    def __init__(
        self,
        model_name: str,
        client: Client | None = None,
    ) -> None:
        self.model_name = model_name
        self.client = client or Client()

    def embed(self, text: str) -> list[float]:
        """Generate an embedding for one text."""

        if not text.strip():
            raise ValueError("Text cannot be empty")

        response = self.client.embed(
            model=self.model_name,
            input=text,
        )

        return response["embeddings"][0]

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""

        if not texts:
            return []

        response = self.client.embed(
            model=self.model_name,
            input=texts,
        )

        return response["embeddings"]
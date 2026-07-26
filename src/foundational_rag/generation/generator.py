from ollama import Client


class ResponseGenerator:
    """Generates answers using a local Ollama model."""

    def __init__(
        self,
        model_name: str,
        client: Client | None = None,
    ) -> None:
        self.model_name = model_name
        self.client = client or Client()

    def generate(self, prompt: str) -> str:
        """Generate an answer from the prompt."""

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        response = self.client.generate(
            model=self.model_name,
            prompt=prompt,
        )

        return response["response"].strip()
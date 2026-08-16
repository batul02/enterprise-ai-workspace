from ollama import Client

from app.core.config import settings


class LLMService:
    """
    Generates responses from a configured large language model.
    """

    def __init__(
        self,
        client: Client,
        model: str,
    ):
        self.client = client
        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an LLM response from the supplied prompt.
        """

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response["message"]["content"]

        if not content or not content.strip():
            raise ValueError(
                "LLM returned an empty response."
            )

        return content.strip()
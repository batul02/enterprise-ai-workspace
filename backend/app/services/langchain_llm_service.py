from langchain_ollama import ChatOllama
from app.core.config import settings


class LangChainLLMService:
    """
    LLM service using LangChain's ChatOllama integration.
    """

    def __init__(
        self,
        model: str = settings.LLM_MODEL,
    ):
        self.llm = ChatOllama(
            model=model,
            temperature=0,
        )

    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)

        return response.content
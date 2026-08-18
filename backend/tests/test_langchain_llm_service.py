from app.services.langchain_llm_service import LangChainLLMService
from app.core.config import settings


def test_generate():
    service = LangChainLLMService(
        model=settings.LLM_MODEL,
    )

    response = service.generate(
        "What is 2 + 2? Answer with only the number."
    )

    assert response
    assert "4" in response
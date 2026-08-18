from app.services.langchain_prompt_service import (
    LangChainPromptService,
)


def test_build_prompt():
    service = LangChainPromptService()

    prompt = service.build_prompt(
        question="What are the characteristics of trustworthy AI?",
        context="Trustworthy AI is valid, reliable, safe, secure, "
                 "resilient, accountable, transparent, explainable, "
                 "interpretable, privacy-enhanced, and fair.",
    )

    assert "What are the characteristics of trustworthy AI?" in prompt
    assert "Trustworthy AI is valid" in prompt
    assert "Answer only using the provided context." in prompt
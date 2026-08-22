from app.services.query_transformer import QueryTransformer
from app.core.dependencies import llm_service


class FakeLLMService:
    def __init__(self, response: str):
        self.response = response
        self.last_prompt = None

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        return self.response


def test_rewrite_follow_up_question():
    llm_service = FakeLLMService(
        "What is the interest rate for the second loan product?"
    )

    transformer = QueryTransformer(llm_service)

    result = transformer.rewrite(
        query="What about the second one?",
        conversation_history=[
            {
                "role": "user",
                "content": "What are the loan products?",
            },
            {
                "role": "assistant",
                "content": (
                    "There are three products: "
                    "Personal Loan, Home Loan and Auto Loan."
                ),
            },
        ],
    )

    assert result == ("What is the interest rate for the second loan product?")


def test_rewrite_already_standalone_query():
    query = "What are the characteristics of trustworthy AI?"

    llm_service = FakeLLMService(query)

    transformer = QueryTransformer(llm_service)

    result = transformer.rewrite(
        query=query,
        conversation_history=[],
    )

    assert result == query


def test_rewrite_pronoun_reference():
    llm_service = FakeLLMService("Does the personal loan require collateral?")

    transformer = QueryTransformer(llm_service)

    result = transformer.rewrite(
        query="Does it require collateral?",
        conversation_history=[
            {
                "role": "user",
                "content": ("What is the interest rate for the personal loan?"),
            },
            {
                "role": "assistant",
                "content": ("The personal loan has an interest rate of 8%."),
            },
        ],
    )

    assert result == ("Does the personal loan require collateral?")


def test_empty_query():
    llm_service = FakeLLMService("anything")

    transformer = QueryTransformer(llm_service)

    try:
        transformer.rewrite("")
        assert False
    except ValueError as exc:
        assert str(exc) == "Query cannot be empty."


def test_empty_history_is_handled():
    query = "What is the interest rate?"

    llm_service = FakeLLMService(query)

    transformer = QueryTransformer(llm_service)

    transformer.rewrite(
        query=query,
        conversation_history=None,
    )

    assert "No previous conversation." in (llm_service.last_prompt)
    
    
def test_query_transformer_with_real_llm():

    transformer = QueryTransformer(
        llm_service=llm_service
    )

    result = transformer.rewrite(
        query="What about the second one?",
        conversation_history=[
            {
                "role": "user",
                "content": "What are the loan products?",
            },
            {
                "role": "assistant",
                "content": (
                    "There are three products: "
                    "Personal Loan, Home Loan and Auto Loan."
                ),
            },
        ],
    )

    print("\nRewritten query:")
    print(result)

    assert result
    assert len(result) > 0

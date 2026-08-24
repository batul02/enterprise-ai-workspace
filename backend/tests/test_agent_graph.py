from app.agents.graph import build_graph
from app.core.dependencies import (
    retrieval_service,
    prompt_service,
    llm_service,
    agents_service,
)


class FakeRetrievalService:
    def __init__(self):
        self.called = False
        self.last_query = None
        self.last_workspace_id = None
        self.last_top_k = None

    def search(self, query, workspace_id, top_k=5):
        self.called = True
        self.last_query = query
        self.last_workspace_id = workspace_id
        self.last_top_k = top_k

        return [
            {
                "content": ("Trustworthy AI systems should be " "valid and reliable."),
                "filename": "test.pdf",
                "chunk_id": 1,
            }
        ]


class FakePromptService:
    def __init__(self):
        self.called = False
        self.last_query = None
        self.last_chunks = None

    def build_prompt(self, query, chunks):
        self.called = True
        self.last_query = query
        self.last_chunks = chunks

        return f"""
        Context:
        {chunks}

        Question:
        {query}
        """


class FakeLLMService:
    def __init__(self):
        self.called = False
        self.last_prompt = None

    def generate(self, prompt):
        self.called = True
        self.last_prompt = prompt

        return "AI systems should be valid and reliable."


def create_graph(retrieval_service, prompt_service, llm_service):
    return build_graph(
        retrieval_service=retrieval_service,
        prompt_service=prompt_service,
        llm_service=llm_service,
    )


def test_agent_routes_rag_query():

    graph = agents_service

    result = graph.invoke(
        {
            "query": "What are the characteristics of trustworthy AI?",
            "workspace_id": 61,
        }
    )

    assert result["route"] == "rag"
    assert result["retrieved_chunks"]
    assert result["answer"]


def test_agent_routes_direct_query():
    graph = agents_service

    result = graph.invoke(
        {
            "query": "Hello",
            "workspace_id": 61,
        }
    )

    assert result["route"] == "direct"
    assert result["answer"]


def test_direct_query_does_not_call_retrieval():
    retrieval = retrieval_service
    prompt = prompt_service
    llm = llm_service

    graph = create_graph(
        retrieval,
        prompt,
        llm,
    )

    result = graph.invoke(
        {
            "query": "Hello",
            "workspace_id": 61,
        }
    )

    assert result["route"] == "direct"
    assert result["answer"]

    # If retrieval had been executed, retrieved_chunks
    # would normally be present in the state.
    assert not result.get("retrieved_chunks")


def test_rag_query_calls_retrieval():
    retrieval = retrieval_service
    prompt = prompt_service
    llm = llm_service

    graph = create_graph(
        retrieval,
        prompt,
        llm,
    )

    result = graph.invoke(
        {
            "query": "What are the characteristics of trustworthy AI?",
            "workspace_id": 61,
        }
    )

    assert result["route"] == "rag"

    # Retrieval node must have populated the state.
    assert result.get("retrieved_chunks")

    assert len(result["retrieved_chunks"]) > 0


def test_rag_path_calls_prompt_and_llm():
    retrieval = retrieval_service
    prompt = prompt_service
    llm = llm_service

    graph = create_graph(
        retrieval,
        prompt,
        llm,
    )

    result = graph.invoke(
        {
            "query": "What are the characteristics of trustworthy AI?",
            "workspace_id": 61,
        }
    )

    assert result["route"] == "rag"

    # RAG retrieval happened
    assert result.get("retrieved_chunks")

    # Generation happened
    assert result.get("answer")

    print("\n===== RAG ANSWER =====")
    print(result["answer"])


def test_direct_path_calls_llm():
    retrieval = retrieval_service
    prompt = prompt_service
    llm = llm_service

    graph = create_graph(
        retrieval,
        prompt,
        llm,
    )

    result = graph.invoke(
        {
            "query": "Hello",
            "workspace_id": 61,
        }
    )

    assert result["route"] == "direct"

    # Direct path should produce an answer
    assert result.get("answer")

    # It should not have gone through RAG retrieval
    assert not result.get("retrieved_chunks")

    print("\n===== DIRECT ANSWER =====")
    print(result["answer"])

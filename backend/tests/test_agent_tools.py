import pytest

pytestmark = pytest.mark.integration
from app.agents.tools import create_search_documents_tool
from app.core.dependencies import create_resources
resources = create_resources()


# def test_search_documents_tool():
#     result = search_documents.invoke(
#         {
#             "query": "What are the characteristics of trustworthy AI?",
#             "workspace_id": 61,
#         }
#     )

#     assert result
#     assert len(result) <= 5

#     print("\n--- TOOL RESULT ---")

#     for chunk in result:
#         print("Content:", chunk.content[:300])
#         print("Metadata:", chunk)

def test_search_documents_tool():
    search_documents = create_search_documents_tool(
        resources.retrieval_service
    )

    result = search_documents.invoke({
        "query": "leave policy",
        "workspace_id": 61,
    })

    assert result is not None

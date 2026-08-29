from app.agents.tools import search_documents


def test_search_documents_tool():
    result = search_documents.invoke(
        {
            "query": "What are the characteristics of trustworthy AI?",
            "workspace_id": 61,
        }
    )

    assert result
    assert len(result) <= 5

    print("\n--- TOOL RESULT ---")

    for chunk in result:
        print("Content:", chunk.content[:300])
        print("Metadata:", chunk)

from app.services.retrieval_service import RetrievalService
from app.services.prompt_service import PromptService
from app.services.llm_service import LLMService


class RAGService:
    """
    Orchestrates retrieval, prompt construction, and LLM
    generation to produce grounded answers from documents.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
        prompt_service: PromptService,
        llm_service: LLMService,
    ):
        self.retrieval_service = retrieval_service
        self.prompt_service = prompt_service
        self.llm_service = llm_service

    def answer(
        self,
        query: str,
        workspace_id: int,
        top_k: int = 5,
    ) -> dict:
        """
        Retrieve relevant document chunks and generate
        a grounded answer using the configured LLM.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        results = self.retrieval_service.search(
            query=query,
            workspace_id=workspace_id,
            top_k=top_k,
        )

        if not results:
            return {
                "answer": (
                    "I don't have enough information "
                    "in the provided documents."
                ),
                "sources": [],
            }

        prompt = self.prompt_service.build_prompt(
            query=query,
            chunks=results,
        )

        answer = self.llm_service.generate(
            prompt
        )

        return {
            "answer": answer,
            "sources": results,
        }
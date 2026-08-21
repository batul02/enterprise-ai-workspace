from app.core.config import settings
from app.services.embedding_service import EmbeddingService
from app.vectorstore.qdrant_store import QdrantStore
from app.processors.document_processor import DocumentProcessor
from app.services.retrieval_service import RetrievalService
from ollama import Client
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.services.prompt_service import PromptService
from app.services.query_transformer import QueryTransformer

embedding_service = EmbeddingService(model_name=settings.EMBEDDING_MODEL)

qdrant_store = QdrantStore(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
    collection_name=settings.QDRANT_COLLECTION,
    vector_size=embedding_service.get_embedding_dimension(),
)

document_processor = DocumentProcessor(
    embedding_service=embedding_service,
    vector_store=qdrant_store,
)

retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    vector_store=qdrant_store,
    score_threshold=settings.SEARCH_SCORE_THRESHOLD,
)

llm_service = LLMService(
    client=Client(host=settings.OLLAMA_HOST),
    model=settings.LLM_MODEL,
)

query_transformer = QueryTransformer(llm_service=llm_service)

prompt_service = PromptService()
rag_service = RAGService(
    retrieval_service=retrieval_service,
    prompt_service=prompt_service,
    llm_service=llm_service,
    query_transformer=query_transformer,
)

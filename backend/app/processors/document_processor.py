from qdrant_client.models import PointStruct

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.chunking_service import chunk_text


class DocumentProcessor:
    """
    Processes extracted document text into chunks,
    embeddings, and vector-store records.
    """

    def __init__(
        self,
        embedding_service,
        vector_store,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def process(
        self,
        db,
        document: Document,
        extracted_text: str,
    ) -> None:

        chunks = chunk_text(
            extracted_text
        )

        if not chunks:
            return

        document_chunks = []

        for chunk in chunks:
            document_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                start_char=chunk.start_char,
                end_char=chunk.end_char,
                character_count=chunk.character_count,
                embedding_status="PENDING",
            )

            document_chunks.append(
                document_chunk
            )

        db.add_all(document_chunks)
        db.flush()

        texts = [
            chunk.content
            for chunk in document_chunks
        ]

        embeddings = (
            self.embedding_service.generate_embeddings(
                texts
            )
        )

        if len(embeddings) != len(document_chunks):
            raise ValueError(
                "Embedding count does not match "
                "document chunk count."
            )

        points = []

        for chunk, embedding in zip(
            document_chunks,
            embeddings,
        ):
            points.append(
                PointStruct(
                    id=chunk.id,
                    vector=embedding,
                    payload={
                        "document_id": document.id,
                        "workspace_id": document.workspace_id,
                        "chunk_id": chunk.id,
                        "chunk_index": chunk.chunk_index,
                        "content": chunk.content,
                        "filename": document.original_filename,
                    },
                )
            )

        self.vector_store.upsert(points)

        for chunk in document_chunks:
            chunk.embedding_status = "COMPLETED"
from enum import Enum


# ==============================
# File Upload
# ==============================

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

SUPPORTED_CONTENT_TYPES = {
    "application/pdf",
}


# ==============================
# PDF Extraction
# ==============================

class ExtractionStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# ==============================
# Chunking
# ==============================

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200


# ==============================
# Storage
# ==============================

STORAGE_DIRECTORY = "storage"
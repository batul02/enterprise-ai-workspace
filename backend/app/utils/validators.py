from fastapi import HTTPException, UploadFile, status
from app.core.constants import (
    MAX_FILE_SIZE,
    SUPPORTED_CONTENT_TYPES,
)


def validate_pdf(file: UploadFile):
    if file.content_type not in SUPPORTED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PDF files are allowed.",
        )

    if file.size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds 10 MB.",
        )
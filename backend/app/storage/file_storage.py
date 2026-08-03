from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
import shutil

BASE_STORAGE_PATH = Path("storage")

def get_workspace_directory(
    workspace_id: int,
) -> Path:

    directory = (
        BASE_STORAGE_PATH
        / f"workspace_{workspace_id}"
    )

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory

def save_file(
    workspace_id: int,
    file: UploadFile,
) -> tuple[str, str]:

    extension = Path(
        file.filename
    ).suffix

    filename = (
        f"{uuid4()}{extension}"
    )

    directory = get_workspace_directory(
        workspace_id
    )

    file_path = (
        directory
        / filename
    )

    with open(
        file_path,
        "wb",
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer,
        )

    return (
        filename,
        str(file_path),
    )


def delete_file(
    storage_path: str,
):

    path = Path(storage_path)

    if path.exists():
        path.unlink()
from dataclasses import dataclass

from app.core.constants import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
)


@dataclass
class ChunkData:
    chunk_index: int
    content: str
    start_char: int
    end_char: int
    character_count: int

def find_split_position(
    text: str,
    start: int,
    max_end: int,
) -> int:

    newline = text.rfind(
        "\n",
        start,
        max_end,
    )

    if newline != -1:
        return newline + 1

    for delimiter in [". ", "! ", "? "]:
        position = text.rfind(
            delimiter,
            start,
            max_end,
        )

        if position != -1:
            return position + len(delimiter)

    space = text.rfind(
        " ",
        start,
        max_end,
    )

    if space != -1:
        return space

    return max_end

def chunk_text(
    text: str,
) -> list[ChunkData]:

    if not text.strip():
        return []

    chunks = []

    start = 0
    chunk_index = 0

    while start < len(text):

        max_end = min(
            start + CHUNK_SIZE,
            len(text),
        )

        end = find_split_position(
            text,
            start,
            max_end,
        )

        if end <= start:
            end = max_end

        chunk = text[start:end]

        chunks.append(
            ChunkData(
                chunk_index=chunk_index,
                content=chunk,
                start_char=start,
                end_char=end,
                character_count=len(chunk),
            )
        )

        if end == len(text):
            break

        start = end - CHUNK_OVERLAP

        chunk_index += 1

    return chunks
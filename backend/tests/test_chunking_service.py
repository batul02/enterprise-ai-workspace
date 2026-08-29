from app.core.constants import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
)
from app.services.chunking_service import chunk_text

def test_chunk_empty_text():
    chunks = chunk_text("")

    assert chunks == []

def test_chunk_small_text():
    text = "Hello World!"

    chunks = chunk_text(text)

    assert len(chunks) == 1

    assert chunks[0].content == text

    assert chunks[0].chunk_index == 0

    assert chunks[0].character_count == len(text)

def test_chunk_large_text():
    text = "A" * (CHUNK_SIZE * 3)

    chunks = chunk_text(text)

    assert len(chunks) > 1

def test_chunk_ordering():
    text = "A" * (CHUNK_SIZE * 2)

    chunks = chunk_text(text)

    for index, chunk in enumerate(chunks):
        assert chunk.chunk_index == index

def test_chunk_overlap():
    text = "A" * (CHUNK_SIZE * 2)

    chunks = chunk_text(text)

    assert len(chunks) >= 2

    first = chunks[0]

    second = chunks[1]

    overlap_first = first.content[-CHUNK_OVERLAP:]

    overlap_second = second.content[:CHUNK_OVERLAP]

    assert overlap_first == overlap_second

def test_chunk_character_boundaries():
    text = "A" * (CHUNK_SIZE * 2)

    chunks = chunk_text(text)

    for chunk in chunks:

        assert chunk.character_count == len(chunk.content)

        assert chunk.end_char > chunk.start_char

def test_last_chunk_size():
    text = "A" * (CHUNK_SIZE * 3 + 347)

    chunks = chunk_text(text)

    assert chunks[-1].character_count <= CHUNK_SIZE

def test_chunk_size_limit():
    text = "A" * (CHUNK_SIZE * 4)

    chunks = chunk_text(text)

    for chunk in chunks:
        assert chunk.character_count <= CHUNK_SIZE

def test_chunk_splits_on_sentence_boundary():
    text = (
        "This is sentence one. "
        "This is sentence two. "
        "This is sentence three."
    )

    chunks = chunk_text(text)

    # Ensure we don't split in the middle of a word
    for chunk in chunks[:-1]:
        assert not chunk.content.endswith(" ")

#New test after correcting Fix chunker bug        
def test_chunk_text_never_creates_negative_start():
    text = (
        "This is a short sentence. "
        "This is another sentence. "
        "This is a third sentence."
    )

    chunks = chunk_text(text)

    assert chunks

    for chunk in chunks:
        assert chunk.start_char >= 0
        assert chunk.end_char > chunk.start_char
        assert chunk.content
        
def test_chunk_text_clamps_overlap_at_zero():
    text = "First sentence.\nSecond sentence."

    chunks = chunk_text(text)

    assert chunks

    for chunk in chunks:
        assert chunk.start_char >= 0
        assert chunk.end_char <= len(text)
        assert chunk.end_char > chunk.start_char
        assert chunk.content.strip()
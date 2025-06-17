def chunk_text(text, chunk_size=500, overlap=100):
    """
    Splits a large block of text into overlapping chunks.

    Args:
        text (str): The full text to split.
        chunk_size (int): Maximum characters per chunk.
        overlap (int): Number of characters to overlap between chunks.

    Returns:
        List[str]: List of text chunks.
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

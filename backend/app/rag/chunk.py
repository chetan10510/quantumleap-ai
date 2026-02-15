def split_text(text, chunk_size=500, overlap=100):
    """
    Splits text into overlapping chunks for better retrieval.
    """

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks

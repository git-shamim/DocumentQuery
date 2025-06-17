# DocumentQuery/utils/embedder.py
from sentence_transformers import SentenceTransformer

# Load a local, free model (you can change this to a larger model if needed)
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embeddings(texts):
    """
    Generate embeddings using a local transformer model (no API key needed).

    Args:
        texts (List[str]): List of text chunks to encode.

    Returns:
        List[List[float]]: List of embedding vectors.
    """
    try:
        if not texts:
            print("[WARN] Empty input to get_embeddings.")
            return []

        embeddings = model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    except Exception as e:
        print(f"[ERROR] Local embedding failed: {e}")
        return []

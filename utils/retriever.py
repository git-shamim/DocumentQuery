import faiss
import numpy as np


class VectorStore:
    def __init__(self, dimension):
        """
        Initializes FAISS index for L2 similarity.
        """
        self.index = faiss.IndexFlatL2(dimension)
        self.chunk_map = []

    def add_embeddings(self, embeddings, chunks):
        """
        Adds embeddings and maps them to their original chunks.

        Args:
            embeddings (List[List[float]]): Vector embeddings.
            chunks (List[str]): Corresponding text chunks.
        """
        self.index.add(np.array(embeddings).astype("float32"))
        self.chunk_map.extend(chunks)

    def query(self, query_embedding, top_k=5):
        """
        Performs similarity search and returns top_k matching text chunks.

        Args:
            query_embedding (List[float]): Embedding of the user question.
            top_k (int): Number of top results to return.

        Returns:
            List[str]: Matching text chunks.
        """
        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)
        return [self.chunk_map[i] for i in indices[0] if i < len(self.chunk_map)]

import faiss
import numpy as np


DIMENSION = 384
id_to_filename = []

index = faiss.IndexFlatL2(DIMENSION)

def add_vector(embedding,filename):
    """
    Add a resume embedding to FAISS index
    """
    vector = np.array(embedding).astype("float32").reshape(1,-1)
    index.add(vector)
    id_to_filename.append(filename)


def search_vectors(query_embedding,k=5):
    """
    Search top k similar vectors
    """
    if index.ntotal == 0:
        return []
    
    vector = np.array(query_embedding).astype("float32").reshape(1,-1)

    distances, indices = index.search(vector,k)

    results = []
    for idx in indices[0]:
        if idx < len(id_to_filename):
            results.append(id_to_filename[idx])
    return results


def get_total_vectors():
    """
    Debug helper to see how many vectors exist
    """
    return index.ntotal
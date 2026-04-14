import faiss
import numpy as np
import os
import json



DIMENSION = 384

INDEX_FILE = "faiss_index.bin"
MAPPING_FILE = "faiss_mapping.json"


if os.path.exists(INDEX_FILE):
    index = faiss.read_index(INDEX_FILE)
else: 
    index = faiss.IndexFlatL2(DIMENSION)

if os.path.exists(MAPPING_FILE):
    with open(MAPPING_FILE,"r") as f:
        id_to_filename = json.load(f)
else:
    id_to_filename = []



def add_vector(embedding,filename):
    """
    Add a resume embedding to FAISS index
    """
    if filename in id_to_filename:
        print(f"Vector for {filename} already exists. Skipping.")
        return

    vector = np.array(embedding).astype("float32").reshape(1,-1)
    index.add(vector)
    id_to_filename.append(filename)
    faiss.write_index(index,INDEX_FILE)

    with open(MAPPING_FILE,"w") as f:
        json.dump(id_to_filename,f)


def search_similar(query_embedding,k=5):
    """
    Search top k similar vectors
    """
    if index.ntotal == 0:
        return []
    
    vector = np.array(query_embedding).astype("float32").reshape(1,-1)

    distances, indices = index.search(vector,k)

    results = []
    for i,idx in enumerate(indices[0]):
        if idx!=-1 and idx < len(id_to_filename):
            filename = id_to_filename[idx]
            distance = float(distances[0][i])
            results.append((filename,distance))
    return results


def get_total_vectors():
    """
    Debug helper to see how many vectors exist
    """
    return index.ntotal
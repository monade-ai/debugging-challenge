from sentence_transformers import SentenceTransformer
import numpy as np
import os
import time
import threading

embedding_model = None
_model_lock = threading.Lock()

def _get_embedding_model():
    global embedding_model
    if embedding_model is None:
        with _model_lock:
            if embedding_model is None:
                embedding_model = SentenceTransformer('all-mpnet-base-v2')
    return embedding_model

def calculate_similarity(response1, response2):
    """Calculates the cosine similarity between two response embeddings."""
    try:
        model = _get_embedding_model()
        
        if not response1 or not response2:
            return 0.0
        
        embedding1 = model.encode(response1, convert_to_tensor=True)
        embedding2 = model.encode(response2, convert_to_tensor=True)
        
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        
        return max(-1.0, min(1.0, similarity.item()))
        
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0

def get_other_nodes(node_id):
    """
    Determines the addresses of other nodes in the cluster based on the current node's ID.
    """
    if node_id == "node1":
        return ["node2:7002", "node3:7003"]
    elif node_id == "node2":
        return ["node1:7001", "node3:7003"]
    elif node_id == "node3":
        return ["node1:7001", "node2:7002"]
    else:
        raise ValueError(f"Unknown node ID: {node_id}")

def cleanup_embedding_model():
    global embedding_model
    if embedding_model is not None:
        embedding_model = None

import atexit
atexit.register(cleanup_embedding_model)
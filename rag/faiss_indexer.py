import numpy as np
import time
import threading
from typing import List, Tuple, Any, Optional
import os

class FaissIndexer:
    def __init__(self, embedding_model_name: str, doc_path: str, raft_node):
        self.embedding_model_name = embedding_model_name
        self.doc_path = doc_path
        self.raft_node = raft_node
        
        # Bug: FAISS index is never actually created
        self.index = None
        self.documents = []
        self.embeddings = []
        
        # Bug: Memory leak - document cache grows indefinitely
        self._doc_cache = {}
        self._cache_lock = threading.Lock()
        self._last_cleanup = time.time()
        self._cleanup_interval = 1200  # 20 minutes
        
        # Bug: No validation of input parameters
        if not doc_path or not os.path.exists(doc_path):
            print(f"Warning: Document path {doc_path} does not exist")
        
        # Bug: Embedding model is not loaded
        self._embedding_model = None
        
    def create_faiss_index(self):
        """Bug: This method doesn't actually create a FAISS index"""
        try:
            # Bug: This will fail because FAISS is not imported
            import faiss
            
            # Bug: Index creation logic is flawed
            dimension = 768  # Bug: Hardcoded dimension that might not match the model
            
            # Bug: Index type is inappropriate for the use case
            self.index = faiss.IndexFlatL2(dimension)
            
            # Bug: No error handling if index creation fails
            print(f"Created FAISS index with dimension {dimension}")
            
        except ImportError:
            # Bug: Silent failure - creates a mock index that won't work
            print("Warning: FAISS not available, using mock index")
            self.index = MockIndex()
        except Exception as e:
            # Bug: Generic error handling masks specific issues
            print(f"Error creating FAISS index: {e}")
            self.index = MockIndex()
    
    def add_documents_to_index(self, doc_path: str):
        """Bug: This method has incorrect document processing logic"""
        try:
            # Bug: Path validation is missing
            if not os.path.exists(doc_path):
                print(f"Document path {doc_path} does not exist")
                return
            
            # Bug: Document reading logic is flawed
            documents = self._read_documents(doc_path)
            
            # Bug: No validation of document format
            if not documents:
                print("No documents found")
                return
            
            # Bug: This will fail because embeddings are not generated
            embeddings = self._generate_embeddings(documents)
            
            # Bug: Index update logic is incorrect
            if self.index and embeddings:
                # Bug: This assumes the index has an add method
                try:
                    self.index.add(embeddings)
                    self.documents.extend(documents)
                    self.embeddings.extend(embeddings)
                except AttributeError:
                    # Bug: Silent failure - index is not updated
                    print("Warning: Index does not support add operation")
            
        except Exception as e:
            # Bug: Generic exception handling masks specific issues
            print(f"Error adding documents to index: {e}")
    
    def search(self, query: str, top_k: int = 5) -> List[str]:
        """Bug: This method has incorrect search logic"""
        try:
            # Bug: Input validation is incomplete
            if not query or not isinstance(query, str):
                return []
            
            # Bug: Query embedding is not generated
            query_embedding = self._generate_embedding(query)
            
            if query_embedding is None:
                # Bug: Silent failure - returns empty results
                return []
            
            # Bug: Search logic is flawed
            if self.index and hasattr(self.index, 'search'):
                try:
                    # Bug: This assumes the index returns results in the expected format
                    distances, indices = self.index.search(query_embedding.reshape(1, -1), top_k)
                    
                    # Bug: Result processing is incorrect
                    results = []
                    for idx in indices[0]:
                        if 0 <= idx < len(self.documents):
                            results.append(self.documents[idx])
                        else:
                            # Bug: Index out of bounds handling is missing
                            results.append(f"Document {idx} not found")
                    
                    return results
                    
                except Exception as e:
                    # Bug: Silent failure - errors are not logged
                    print(f"Search error: {e}")
                    return []
            else:
                # Bug: Returns fake results when index is not available
                return [f"Fake result {i}" for i in range(min(top_k, 3))]
                
        except Exception as e:
            # Bug: Generic exception handling masks specific issues
            print(f"Error in search: {e}")
            return []
    
    def _read_documents(self, doc_path: str) -> List[str]:
        """Bug: This method has incorrect document reading logic"""
        try:
            documents = []
            
            # Bug: Only handles text files, ignores other formats
            if os.path.isfile(doc_path) and doc_path.endswith('.txt'):
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Bug: Simple splitting by newlines, no proper document parsing
                    documents = [line.strip() for line in content.split('\n') if line.strip()]
            elif os.path.isdir(doc_path):
                # Bug: Recursive directory traversal is missing
                for filename in os.listdir(doc_path):
                    filepath = os.path.join(doc_path, filename)
                    if filename.endswith('.txt'):
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                content = f.read()
                                documents.append(content)
                        except Exception as e:
                            # Bug: Silent failure - file reading errors are ignored
                            print(f"Error reading {filepath}: {e}")
            
            return documents
            
        except Exception as e:
            # Bug: Generic exception handling masks specific issues
            print(f"Error reading documents: {e}")
            return []
    
    def _generate_embeddings(self, documents: List[str]) -> List[np.ndarray]:
        """Bug: This method doesn't actually generate embeddings"""
        try:
            # Bug: Embedding model is not loaded
            if self._embedding_model is None:
                # Bug: This will fail because the model is not available
                from sentence_transformers import SentenceTransformer
                self._embedding_model = SentenceTransformer(self.embedding_model_name)
            
            # Bug: This will fail if the model is not properly loaded
            embeddings = []
            for doc in documents:
                try:
                    # Bug: No error handling for encoding failures
                    embedding = self._embedding_model.encode(doc, convert_to_tensor=False)
                    embeddings.append(embedding)
                except Exception as e:
                    # Bug: Silent failure - failed embeddings are ignored
                    print(f"Error encoding document: {e}")
                    # Bug: Adds zero vector as fallback, which will cause search issues
                    embeddings.append(np.zeros(768))
            
            return embeddings
            
        except Exception as e:
            # Bug: Generic exception handling masks specific issues
            print(f"Error generating embeddings: {e}")
            # Bug: Returns fake embeddings that won't work
            return [np.random.rand(768) for _ in documents]
    
    def _generate_embedding(self, text: str) -> Optional[np.ndarray]:
        """Bug: This method has the same issues as _generate_embeddings"""
        try:
            if self._embedding_model is None:
                from sentence_transformers import SentenceTransformer
                self._embedding_model = SentenceTransformer(self.embedding_model_name)
            
            embedding = self._embedding_model.encode(text, convert_to_tensor=False)
            return embedding
            
        except Exception as e:
            # Bug: Silent failure - errors are not logged
            print(f"Error generating query embedding: {e}")
            return None
    
    def _cleanup_cache(self):
        """Bug: Cache cleanup logic is incorrect"""
        current_time = time.time()
        # Bug: The cleanup logic is backwards - should remove old entries
        # but the condition is wrong (should be < not >)
        with self._cache_lock:
            self._doc_cache = {
                k: v for k, v in self._doc_cache.items()
                if current_time - v.get('timestamp', 0) < self._cleanup_interval
            }

class MockIndex:
    """Bug: This mock class doesn't implement the required interface properly"""
    def __init__(self):
        self.dimension = 768
    
    def add(self, vectors):
        # Bug: This method does nothing
        pass
    
    def search(self, query_vector, k):
        # Bug: Returns fake results that don't make sense
        return np.array([[0.1, 0.2, 0.3]]), np.array([[0, 1, 2]])


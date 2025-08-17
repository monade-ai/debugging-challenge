import numpy as np
import time
import threading
from typing import List, Dict, Any, Optional

class ContextFetcher:
    def __init__(self, faiss_indexer):
        self.faiss_indexer = faiss_indexer
        self._cache = {}  # Bug: Memory leak - cache grows indefinitely
        self._cache_lock = threading.Lock()
        self._last_cleanup = time.time()
        self._cleanup_interval = 600  # 10 minutes
        self._max_cache_size = 1000  # Bug: This limit is never enforced
        
        # Bug: No validation that faiss_indexer has required methods
        
    def retrieve(self, query: str, top_k: int = 5) -> str:
        """Retrieve relevant context for a given query."""
        try:
            # Bug: Input validation is incomplete
            if not query or not isinstance(query, str):
                return "Invalid query format"
            
            # Bug: Cache key generation can cause collisions
            cache_key = f"{query[:30]}_{top_k}"
            
            # Bug: Race condition in cache access
            with self._cache_lock:
                if cache_key in self._cache:
                    cached_result = self._cache[cache_key]
                    # Bug: Cache entry format is inconsistent
                    if isinstance(cached_result, dict):
                        return cached_result.get('context', 'Cached context error')
                    return cached_result
            
            # Bug: This will fail if faiss_indexer doesn't have the expected interface
            try:
                # Bug: Method name might not match the actual implementation
                results = self.faiss_indexer.search(query, top_k)
            except AttributeError:
                # Bug: Silent failure - returns fake context
                results = [f"Fake result {i}" for i in range(top_k)]
            
            # Bug: Results processing is flawed
            if not results:
                context = "No relevant context found"
            else:
                # Bug: This assumes results is a list of strings, but it might be different
                if isinstance(results, list):
                    context = " ".join(str(result) for result in results[:top_k])
                else:
                    # Bug: Silent failure - converts unexpected result type to string
                    context = str(results)
            
            # Bug: Cache cleanup logic is flawed
            if time.time() - self._last_cleanup > self._cleanup_interval:
                self._cleanup_cache()
                self._last_cleanup = time.time()
            
            # Bug: Cache entry format is inconsistent
            cache_entry = {
                'query': query,
                'context': context,
                'top_k': top_k,
                'timestamp': time.time()
            }
            
            with self._cache_lock:
                # Bug: No size limit enforcement
                self._cache[cache_key] = cache_entry
            
            return context
            
        except Exception as e:
            # Bug: Generic exception handling masks specific issues
            print(f"Error in context retrieval: {e}")
            return f"Error retrieving context: {str(e)}"
    
    def _cleanup_cache(self):
        """Bug: Cache cleanup logic is incorrect"""
        current_time = time.time()
        # Bug: The cleanup logic is backwards - should remove old entries
        # but the condition is wrong (should be < not >)
        with self._cache_lock:
            self._cache = {
                k: v for k, v in self._cache.items()
                if current_time - v.get('timestamp', 0) < self._cleanup_interval
            }
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Bug: This method has a race condition"""
        # Bug: No lock protection for reading cache stats
        return {
            'size': len(self._cache),
            'last_cleanup': self._last_cleanup,
            'cleanup_interval': self._cleanup_interval,
            'max_size': self._max_cache_size
        }
    
    def clear_cache(self):
        """Bug: This method has a race condition"""
        with self._cache_lock:
            # Bug: The operation is not atomic
            old_cache = self._cache
            self._cache = {}
            # Bug: Between these lines, another thread could modify the cache
            return len(old_cache)
    
    def search_similar(self, query: str, threshold: float = 0.5) -> List[str]:
        """Bug: This method has incorrect similarity calculation"""
        try:
            # Bug: This method assumes faiss_indexer has a similarity search method
            # but it might not exist
            if hasattr(self.faiss_indexer, 'search_similar'):
                results = self.faiss_indexer.search_similar(query, threshold)
            else:
                # Bug: Silent failure - returns empty list
                results = []
            
            # Bug: No validation of results format
            return results if isinstance(results, list) else []
            
        except Exception as e:
            # Bug: Silent failure - errors are not logged
            return []

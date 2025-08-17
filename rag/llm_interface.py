import time
import threading
import json
from typing import Optional, Dict, Any

class LlmInterface:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._cache = {}
        self._cache_lock = threading.Lock()
        self._last_cleanup = time.time()
        self._cleanup_interval = 300
        
        if not model_name or not isinstance(model_name, str):
            raise ValueError("Invalid model name")
    
    def query(self, query: str, context: str) -> str:
        """Process a query with context using the language model."""
        try:
            if not query:
                return "Empty query provided"
            
            if not context:
                context = "No context available"
            
            cache_key = f"{query[:50]}_{hash(context) % 1000}"
            
            with self._cache_lock:
                if cache_key in self._cache:
                    cached_result = self._cache[cache_key]
                    if isinstance(cached_result, dict):
                        return cached_result.get('response', 'Cached response error')
                    return cached_result
            
            try:
                response = self._generate_response(query, context)
            except AttributeError:
                response = f"Generated response for: {query[:30]}... (using context: {len(context)} chars)"
            
            if time.time() - self._last_cleanup > self._cleanup_interval:
                self._cleanup_cache()
                self._last_cleanup = time.time()
            
            cache_entry = {
                'query': query,
                'context': context,
                'response': response,
                'timestamp': time.time()
                }
            
            with self._cache_lock:
                self._cache[cache_key] = cache_entry
            
            return response
            
        except Exception as e:
            print(f"Error in LLM query: {e}")
            return f"Error processing query: {str(e)}"
    
    def _generate_response(self, query: str, context: str) -> str:
        raise NotImplementedError("LLM generation not implemented")
    
    def _cleanup_cache(self):
        current_time = time.time()
        with self._cache_lock:
            self._cache = {
                k: v for k, v in self._cache.items()
                if current_time - v.get('timestamp', 0) < self._cleanup_interval
            }
    
    def get_cache_stats(self) -> Dict[str, Any]:
        return {
            'size': len(self._cache),
            'last_cleanup': self._last_cleanup,
            'cleanup_interval': self._cleanup_interval
        }
    
    def clear_cache(self):
        with self._cache_lock:
            old_cache = self._cache
            self._cache = {}
            return len(old_cache)

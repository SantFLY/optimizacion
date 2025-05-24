from typing import Any, Dict, Optional
import time
from threading import Lock

class CacheService:
    def __init__(self, ttl_seconds: int = 60):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self._ttl_seconds = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché si existe y no ha expirado"""
        with self._lock:
            if key in self._cache:
                cache_entry = self._cache[key]
                if time.time() - cache_entry['timestamp'] < self._ttl_seconds:
                    return cache_entry['value']
                else:
                    del self._cache[key]
        return None

    def set(self, key: str, value: Any):
        """Almacena un valor en el caché con timestamp"""
        with self._lock:
            self._cache[key] = {
                'value': value,
                'timestamp': time.time()
            }

    def invalidate(self, key: str):
        """Invalida una entrada específica del caché"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def clear(self):
        """Limpia todo el caché"""
        with self._lock:
            self._cache.clear() 
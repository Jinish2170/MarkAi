"""
Advanced utilities for MarkAI
"""

import hashlib
import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Union
from pathlib import Path


def generate_id(prefix: str = "", length: int = 8) -> str:
    """Generate a unique ID"""
    timestamp = str(int(time.time() * 1000000))
    hash_obj = hashlib.md5(timestamp.encode())
    hash_id = hash_obj.hexdigest()[:length]
    
    return f"{prefix}_{hash_id}" if prefix else hash_id


def safe_json_loads(data: str, default: Any = None) -> Any:
    """Safely load JSON data"""
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(data: Any, default: str = "{}") -> str:
    """Safely dump JSON data"""
    try:
        return json.dumps(data, default=str, ensure_ascii=False)
    except (TypeError, ValueError):
        return default


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format timestamp for display"""
    if dt is None:
        dt = datetime.now(timezone.utc)
    
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure directory exists"""
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Remove control characters
    text = "".join(char for char in text if ord(char) >= 32 or char in '\t\n\r')
    
    return text.strip()


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate basic text similarity using Jaccard similarity"""
    # Convert to lowercase and split into words
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    # Calculate Jaccard similarity
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    if not union:
        return 0.0
    
    return len(intersection) / len(union)


def extract_keywords(text: str, min_length: int = 3, max_keywords: int = 10) -> List[str]:
    """Extract keywords from text"""
    import re
    
    # Common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
    }
    
    # Extract words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Filter words
    keywords = [
        word for word in words
        if len(word) >= min_length and word not in stop_words
    ]
    
    # Count occurrences and sort by frequency
    word_counts = {}
    for word in keywords:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:max_keywords]]


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.1f} {units[unit_index]}"


def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def rate_limit_key(user_id: str, action: str = "default") -> str:
    """Generate rate limit key"""
    return f"rate_limit:{user_id}:{action}"


def parse_duration(duration_str: str) -> int:
    """Parse duration string to seconds"""
    duration_map = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800
    }
    
    duration_str = duration_str.lower().strip()
    
    if duration_str.isdigit():
        return int(duration_str)
    
    for unit, multiplier in duration_map.items():
        if duration_str.endswith(unit):
            try:
                value = int(duration_str[:-1])
                return value * multiplier
            except ValueError:
                pass
    
    return 0


class Timer:
    """Simple timer context manager"""
    
    def __init__(self, name: str = "Timer"):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
    
    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds"""
        if self.start_time is None:
            return 0.0
        
        end = self.end_time or time.time()
        return end - self.start_time
    
    def __str__(self) -> str:
        return f"{self.name}: {self.elapsed:.3f}s"


class Cache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self, default_ttl: int = 300):
        self.default_ttl = default_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache"""
        if key not in self._cache:
            return default
        
        entry = self._cache[key]
        
        # Check if expired
        if entry['expires'] < time.time():
            del self._cache[key]
            return default
        
        return entry['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        if ttl is None:
            ttl = self.default_ttl
        
        self._cache[key] = {
            'value': value,
            'expires': time.time() + ttl
        }
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()
    
    def cleanup(self) -> int:
        """Remove expired entries and return count"""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry['expires'] < current_time
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        return len(expired_keys)


# Global cache instance
_global_cache = Cache()

def cache_get(key: str, default: Any = None) -> Any:
    """Get from global cache"""
    return _global_cache.get(key, default)

def cache_set(key: str, value: Any, ttl: Optional[int] = None) -> None:
    """Set in global cache"""
    _global_cache.set(key, value, ttl)

def cache_delete(key: str) -> bool:
    """Delete from global cache"""
    return _global_cache.delete(key)

def cache_clear() -> None:
    """Clear global cache"""
    _global_cache.clear()

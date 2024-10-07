"""
Simple in-memory cache with Time-to-Live (TTL) functionality.

- Stores key-value pairs with expiration time.
- Used to reduce redundant computations by caching results.
"""

import time

class Cache:
    """
    A simple in-memory cache implementation with time-to-live (TTL) functionality.
    """

    def __init__(self, ttl: int):
        """
        Initialize the cache with a given TTL.

        Args:
            ttl (int): Time-to-live for cache entries in seconds.
        """
        self.ttl = ttl
        self.cache = {}

    def get(self, key: str):
        """
        Retrieve a value from the cache, if it's still valid.

        Args:
            key (str): The key to retrieve from the cache.

        Returns:
            str or None: Cached value if available and valid, None otherwise.
        """
        if key in self.cache and self.cache[key]['expiry'] > time.time():
            return self.cache[key]['value']
        return None

    def set(self, key: str, value: str):
        """
        Store a value in the cache with an expiry time.

        Args:
            key (str): The key to store in the cache.
            value (str): The value to store in the cache.
        """
        expiry = time.time() + self.ttl
        self.cache[key] = {"value": value, "expiry": expiry}

    def clear(self):
        """
        Clear all entries from the cache.
        """
        self.cache = {}

"""
url_shortener.py
-----------------
Core logic for converting long URLs into short codes and back again,
backed by permanent storage (a plain dict) and a fast-access LRU cache.

Design:
- self.storage  -> the "database". Holds EVERY short_code -> long_url
                    mapping permanently (in-memory here, but this is
                    where a real database would plug in).
- self.cache    -> the LRUCache. Holds only the most RECENTLY used
                    mappings, for fast retrieval, capped at a small size.

This mirrors how real-world systems (e.g. bit.ly) use a cache in front
of a database: check the cache first (fast), and only fall back to the
full storage/database on a cache miss.
"""

import hashlib
import itertools

from lru_cache import LRUCache


class URLShortener:
    def __init__(self, cache_capacity: int = 5):
        # Permanent storage of ALL shortened URLs (acts like a database).
        self.storage = {}          # short_code -> long_url
        self.reverse_lookup = {}   # long_url -> short_code (avoid duplicates)

        # Fast-access cache for recently used URLs.
        self.cache = LRUCache(capacity=cache_capacity)

        # A simple counter to help generate unique short codes.
        self._counter = itertools.count(1)

    def _generate_short_code(self, long_url: str) -> str:
        """
        Generate a short, unique code for a given URL.

        We combine the URL with an incrementing counter and hash it
        with MD5, then take the first 6 characters of the hex digest.
        The counter guarantees uniqueness even if the same URL is
        shortened multiple times or two URLs happen to hash similarly.
        """
        unique_string = f"{long_url}-{next(self._counter)}"
        hash_object = hashlib.md5(unique_string.encode())
        short_code = hash_object.hexdigest()[:6]
        return short_code

    def shorten_url(self, long_url: str) -> str:
        """
        Convert a long URL into a short URL (short code).
        If the URL has already been shortened before, return the
        existing short code instead of creating a duplicate.
        """
        long_url = long_url.strip()

        if not long_url:
            raise ValueError("URL cannot be empty.")

        # Avoid creating duplicate short codes for the same long URL.
        if long_url in self.reverse_lookup:
            short_code = self.reverse_lookup[long_url]
        else:
            short_code = self._generate_short_code(long_url)
            self.storage[short_code] = long_url
            self.reverse_lookup[long_url] = short_code

        # Newly shortened/accessed URLs are considered "recently used".
        self.cache.put(short_code, long_url)
        return short_code

    def retrieve_url(self, short_code: str):
        """
        Retrieve the original long URL for a given short code.
        Checks the cache first (fast path). On a cache miss, falls
        back to permanent storage and re-populates the cache.

        Returns None if the short code does not exist at all.
        """
        short_code = short_code.strip()

        # 1. Try the cache first.
        cached_url = self.cache.get(short_code)
        if cached_url is not None:
            return cached_url

        # 2. Cache miss: fall back to permanent storage.
        if short_code in self.storage:
            long_url = self.storage[short_code]
            # Repopulate the cache since this URL was just accessed.
            self.cache.put(short_code, long_url)
            return long_url

        # 3. Short code doesn't exist anywhere.
        return None

    def display_cache(self):
        """Show what's currently sitting in the LRU cache."""
        self.cache.display()

    def display_stats(self):
        """Show cache hit/miss statistics."""
        stats = self.cache.stats()
        print("----- Cache Statistics -----")
        print(f"Capacity      : {stats['capacity']}")
        print(f"Current Size  : {stats['current_size']}")
        print(f"Hits          : {stats['hits']}")
        print(f"Misses        : {stats['misses']}")
        print(f"Hit Rate      : {stats['hit_rate_percent']}%")
        print(f"Total URLs Stored (all-time): {len(self.storage)}")
        print("-----------------------------")

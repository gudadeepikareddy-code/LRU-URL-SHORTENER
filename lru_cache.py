"""
lru_cache.py
------------
A simple, easy-to-explain implementation of an LRU (Least Recently Used)
Cache built on top of Python's OrderedDict.

Why OrderedDict?
- It remembers the order in which keys were inserted/accessed.
- move_to_end() lets us mark an item as "recently used" in O(1) time.
- popitem(last=False) lets us remove the "oldest" (least recently used)
  item in O(1) time.

This makes OrderedDict a perfect, beginner-friendly building block for
an LRU cache without needing to write a custom doubly linked list.
"""

from collections import OrderedDict


class LRUCache:
    """
    A fixed-capacity cache that evicts the Least Recently Used item
    whenever a new item is added beyond capacity.
    """

    def __init__(self, capacity: int = 5):
        # Maximum number of items the cache can hold at once.
        self.capacity = capacity

        # OrderedDict maintains insertion/access order.
        # Left side (first item)  -> Least Recently Used
        # Right side (last item)  -> Most Recently Used
        self.cache = OrderedDict()

        # Statistics counters for cache performance tracking.
        self.hits = 0
        self.misses = 0

    def get(self, key: str):
        """
        Retrieve a value from the cache.
        Returns None if the key is not present (cache miss).
        On a cache hit, the key is marked as most recently used.
        """
        if key not in self.cache:
            self.misses += 1
            return None

        # Cache hit: move this key to the end to mark it as
        # most recently used.
        self.cache.move_to_end(key)
        self.hits += 1
        return self.cache[key]

    def put(self, key: str, value: str):
        """
        Insert or update a value in the cache.
        If the cache is full, the least recently used item is evicted.
        """
        if key in self.cache:
            # Key already exists: update value and refresh its position.
            self.cache.move_to_end(key)
        self.cache[key] = value

        # If we've exceeded capacity, remove the least recently used item.
        # last=False means "pop the first item", which is the LRU item.
        if len(self.cache) > self.capacity:
            evicted_key, _ = self.cache.popitem(last=False)
            print(f"[Cache] Capacity reached. Evicted LRU item: '{evicted_key}'")

    def contains(self, key: str) -> bool:
        """Check whether a key currently exists in the cache."""
        return key in self.cache

    def display(self):
        """
        Print the current contents of the cache, ordered from
        Most Recently Used (top) to Least Recently Used (bottom).
        """
        if not self.cache:
            print("Cache is empty.")
            return

        print("Cache contents (Most Recently Used -> Least Recently Used):")
        # reversed() because OrderedDict stores LRU first, MRU last.
        for short_code, long_url in reversed(self.cache.items()):
            print(f"  {short_code}  ->  {long_url}")

    def stats(self):
        """Return a dictionary of hit/miss statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0.0
        return {
            "capacity": self.capacity,
            "current_size": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_percent": round(hit_rate, 2),
        }

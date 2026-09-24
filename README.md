# LRU Cache-Based URL Shortener

A command-line Python application that shortens long URLs and uses a
custom **LRU (Least Recently Used) Cache** to efficiently retrieve
frequently accessed URLs — similar in spirit to how real-world
services like bit.ly speed up lookups with a cache layer in front of
their database.

## Project Overview

This project simulates the core mechanics of a URL shortening service:

- Convert long URLs into short, unique codes.
- Resolve short codes back to their original long URLs.
- Speed up repeated lookups using an in-memory **LRU cache**, so the
  most recently/frequently used URLs are served instantly, while
  older, unused ones are evicted once the cache fills up.

It's intentionally kept simple and dependency-free so it's easy to
read, explain, and extend — making it a great portfolio project for
students learning data structures, caching strategies, and clean
Python project structure.

## Features

- **Shorten URL** — generates a unique 6-character short code for any
  long URL (re-shortening the same URL returns its existing code
  instead of creating a duplicate).
- **Retrieve Original URL** — looks up a short code and returns the
  original URL, checking the cache first for speed.
- **LRU Cache** — built on Python's `OrderedDict`, automatically
  evicts the least recently used entry once the cache reaches its
  capacity.
- **Cache Hit/Miss Tracking** — every lookup is counted as a hit or a
  miss, so you can measure cache effectiveness.
- **Display Cache** — view what's currently sitting in the cache,
  ordered from most to least recently used.
- **Cache Statistics** — view hits, misses, hit rate percentage, cache
  size/capacity, and total URLs ever stored.
- **Robust input handling** — invalid menu choices, empty input, and
  unknown short codes are handled gracefully without crashing.

## Technologies Used

- **Python 3** (standard library only — no external/third-party
  packages required)
- `collections.OrderedDict` — powers the LRU cache
- `hashlib` — generates short, unique codes from URLs

## How It Works

1. **Storage vs. Cache** — the app keeps two structures:
   - `storage`: a plain dictionary that permanently holds *every*
     short code → long URL mapping (acts like a database).
   - `cache`: an `LRUCache` object that holds only a small, limited
     number of the most recently used mappings, for fast access.

2. **Shortening a URL** — the URL is combined with an internal counter
   and hashed with MD5; the first 6 characters of the hash become the
   short code. The mapping is saved to `storage` and also pushed into
   the `cache` (since it was just used).

3. **Retrieving a URL**:
   - First, check the `cache` → if found, it's a **cache hit** (fast).
   - If not found, check `storage` → if found, it's a **cache miss**,
     and the result is loaded back into the cache for next time.
   - If not found anywhere, the short code is invalid.

4. **LRU Eviction** — the cache uses `OrderedDict.move_to_end()` to
   mark items as "recently used" and `OrderedDict.popitem(last=False)`
   to remove the "oldest" (least recently used) item once the cache
   exceeds its capacity — both O(1) operations.

## Project Structure

```
lru_url_shortener/
├── main.py            # CLI entry point — menu-driven user interface
├── url_shortener.py   # URLShortener class — shortening/retrieval logic
├── lru_cache.py        # LRUCache class — cache + hit/miss tracking
└── README.md           # Project documentation
```

## How to Run

**Requirements:** Python 3.7+ (no external libraries needed).

1. Download/clone the project folder.
2. Open a terminal in the `lru_url_shortener` directory.
3. Run:
   ```bash
   python main.py
   ```
4. Follow the on-screen menu to shorten URLs, retrieve them, and view
   the cache/statistics.

## Sample Output

```
Welcome to the LRU Cache-Based URL Shortener!

===== LRU Cache-Based URL Shortener =====
1. Shorten URL
2. Retrieve Original URL
3. Display Cache
4. Display Cache Statistics
5. Exit
==========================================
Enter your choice (1-5): 1
Enter the long URL to shorten: https://www.example.com/articles/python-lru-cache
Shortened URL: http://short.ly/5357f1

Enter your choice (1-5): 1
Enter the long URL to shorten: https://www.example.com/articles/data-structures
Shortened URL: http://short.ly/16aea6

Enter your choice (1-5): 2
Enter the short code or URL (e.g. abc123 or http://short.ly/abc123): 5357f1
Original URL: https://www.example.com/articles/python-lru-cache

Enter your choice (1-5): 3
Cache contents (Most Recently Used -> Least Recently Used):
  5357f1  ->  https://www.example.com/articles/python-lru-cache
  16aea6  ->  https://www.example.com/articles/data-structures

Enter your choice (1-5): 4
----- Cache Statistics -----
Capacity      : 3
Current Size  : 2
Hits          : 1
Misses        : 0
Hit Rate      : 100.0%
Total URLs Stored (all-time): 2
-----------------------------

Enter your choice (1-5): 5
Goodbye!
```

## Future Enhancements

- Persist URL storage to a file or real database (e.g. SQLite) so data
  survives program restarts.
- Add a web interface (Flask/FastAPI) on top of the same core logic.
- Support custom/user-chosen short codes (vanity URLs).
- Add URL expiration (TTL) and click-count analytics per short URL.
- Add unit tests (e.g. with `pytest`) covering cache eviction, hit/miss
  tracking, and edge cases.
- Support cache capacity as a configurable CLI argument at startup.

## Resume Bullet Points

- Built a Python CLI URL shortener implementing a custom LRU cache with
  `OrderedDict`, achieving O(1) cache access/eviction and reducing
  redundant lookups for frequently accessed URLs.
- Designed a two-tier storage architecture (persistent dictionary +
  LRU cache) with hit/miss tracking, mirroring caching strategies used
  in production systems like URL shorteners and CDNs.
- Implemented robust error handling for invalid input and unknown
  short codes, ensuring a crash-free, user-friendly CLI experience.

## Interview Explanation (Short Version)

"I built a URL shortener that mimics how real services like bit.ly
work under the hood. Every URL gets a unique short code (via hashing)
and is stored permanently in a dictionary that acts like a database.
On top of that, I added an LRU cache using Python's `OrderedDict` so
that recently or frequently accessed URLs are served instantly instead
of always querying the 'database'. When the cache fills up, the least
recently used entry is automatically evicted — I track cache hits and
misses to demonstrate how effective the cache is. It's a small project,
but it let me apply a real data-structures concept (LRU caching) to a
practical, relatable problem."

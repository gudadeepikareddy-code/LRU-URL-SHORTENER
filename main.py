"""
main.py
-------
Menu-driven Command Line Interface (CLI) for the LRU Cache-Based
URL Shortener.

Run this file to start the program:
    python main.py
"""

from url_shortener import URLShortener

BASE_SHORT_URL = "http://short.ly/"


def print_menu():
    print("\n===== LRU Cache-Based URL Shortener =====")
    print("1. Shorten URL")
    print("2. Retrieve Original URL")
    print("3. Display Cache")
    print("4. Display Cache Statistics")
    print("5. Exit")
    print("==========================================")


def get_menu_choice() -> str:
    """Read and validate the user's menu selection."""
    choice = input("Enter your choice (1-5): ").strip()
    return choice


def handle_shorten(shortener: URLShortener):
    long_url = input("Enter the long URL to shorten: ").strip()
    if not long_url:
        print("Error: URL cannot be empty. Please try again.")
        return
    try:
        short_code = shortener.shorten_url(long_url)
        print(f"Shortened URL: {BASE_SHORT_URL}{short_code}")
    except ValueError as e:
        print(f"Error: {e}")


def handle_retrieve(shortener: URLShortener):
    short_input = input(
        f"Enter the short code or URL (e.g. abc123 or {BASE_SHORT_URL}abc123): "
    ).strip()

    if not short_input:
        print("Error: Short code cannot be empty.")
        return

    # Allow the user to paste either the full short URL or just the code.
    short_code = short_input.replace(BASE_SHORT_URL, "").strip()

    result = shortener.retrieve_url(short_code)
    if result is None:
        print(f"Error: No URL found for short code '{short_code}'.")
    else:
        print(f"Original URL: {result}")


def main():
    print("Welcome to the LRU Cache-Based URL Shortener!")

    # You can change the cache capacity here. A small number (e.g. 3-5)
    # makes it easy to demonstrate LRU eviction during a demo/interview.
    shortener = URLShortener(cache_capacity=3)

    while True:
        print_menu()
        choice = get_menu_choice()

        if choice == "1":
            handle_shorten(shortener)
        elif choice == "2":
            handle_retrieve(shortener)
        elif choice == "3":
            shortener.display_cache()
        elif choice == "4":
            shortener.display_stats()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            # Handle invalid input gracefully instead of crashing.
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()

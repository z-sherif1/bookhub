import requests

response = requests.get(
    "https://openlibrary.org/search.json",
    params={
        "q": "the hobbit",
        "limit": 3
    },
    headers={
        "User-Agent": "BookHub/1.0 (your-email@example.com)"
    }
)

data = response.json()

for book in data["docs"]:
    print(
        book["title"],
        "-",
        book.get("author_name")
    )
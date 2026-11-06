"""Similarity search over grocery items, with Chroma and SentenceTransformers embeddings.

Needs the Chroma server from this folder's docker-compose.yml: `docker compose up -d` here first.
"""

from groceries import GROCERY_IDS, GROCERY_ITEMS, GROCERY_METADATAS
from vector_store import Match, connect, get_grocery_collection, search

TOP_K = 3


def print_matches(query: str, matches: list[Match]) -> None:
    """Print the documents closest to a query, most similar first."""
    print(f'[top {TOP_K}, "{query}"]')
    if not matches:
        print(f'  No documents found similar to "{query}"')
    for match in matches:
        print(f'  {match.id:<8} {match.distance:.4f}  "{match.text}"')


def main() -> None:
    # Create the collection: cosine distance, SentenceTransformers embeddings
    collection = get_grocery_collection(connect())
    print(f"[collection] {collection.name}")

    # Add the items: Chroma embeds each document with the collection's embedding function
    # (ids that already exist are skipped on a rerun)
    collection.add(ids=GROCERY_IDS, documents=GROCERY_ITEMS, metadatas=GROCERY_METADATAS)

    # get() with no arguments returns every item in the collection
    all_items = collection.get()
    print(f"[collection contents] {len(all_items['ids'])} documents")

    # Similarity search: the documents closest to one query...
    for query, matches in search(collection, "protein", n_results=TOP_K).items():
        print_matches(query, matches)

    # ...or to several queries in a single call
    for query, matches in search(collection, ["red", "fresh"], n_results=TOP_K).items():
        print_matches(query, matches)


if __name__ == "__main__":
    main()

"""Chroma access for the lesson: the server connection, the grocery collection and similarity search."""

from dataclasses import dataclass

import chromadb
from chromadb.utils import embedding_functions

from app.config.envs import CHROMA_HOST, CHROMA_PORT, EMBEDDING_MODEL

COLLECTION_NAME = "my_grocery_collection"


@dataclass(frozen=True)
class Match:
    """A document returned by a similarity search."""

    id: str
    text: str
    distance: float  # cosine distance: 0 means same direction, lower is more similar


def connect() -> chromadb.ClientAPI:
    """Connect over HTTP to the Chroma server started by this folder's docker-compose.yml.

    The lab's chromadb.Client() is in-memory instead, and forgets everything on exit.
    """
    return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)


def get_grocery_collection(client: chromadb.ClientAPI) -> chromadb.Collection:
    """Return the grocery collection, creating it on first use.

    It compares embeddings by cosine distance, and embeds documents and queries with a
    SentenceTransformers model. get_or_create lets the script run again: the configuration
    only applies the first time, when the collection is actually created.
    """
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "A collection for storing grocery data"},
        configuration={"hnsw": {"space": "cosine"}, "embedding_function": embedding_function},
    )


def search(collection: chromadb.Collection, queries: str | list[str], n_results: int = 3) -> dict[str, list[Match]]:
    """Return the n_results documents closest to each query, most similar first.

    Chroma answers a query with parallel lists, one per query term: results["ids"][q][i]
    goes with results["documents"][q][i] and results["distances"][q][i]. This regroups
    them into one list of Match per query term.
    """
    if isinstance(queries, str):
        queries = [queries]
    results = collection.query(query_texts=queries, n_results=n_results, include=["documents", "distances"])

    matches_by_query = {}
    for q, query in enumerate(queries):
        rows = zip(results["ids"][q], results["documents"][q], results["distances"][q], strict=True)
        matches_by_query[query] = [Match(doc_id, text, distance) for doc_id, text, distance in rows]
    return matches_by_query

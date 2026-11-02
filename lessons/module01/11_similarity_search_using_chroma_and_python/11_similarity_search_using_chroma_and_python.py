# Needs the Chroma server from this folder's docker-compose.yml: `docker compose up -d` here first.
from pprint import pprint

import chromadb
from chromadb.utils import embedding_functions

from app.config.envs import CHROMA_HOST, CHROMA_PORT, EMBEDDING_MODEL

# Setup: a SentenceTransformers embedding function that turns texts into vectors
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)

# Connect to the Chroma server over HTTP (the lab's chromadb.Client() is in-memory and forgets everything on exit)
client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

# Create a collection that compares embeddings by cosine distance (get_or_create, so the script can be rerun)
collection = client.get_or_create_collection(
    name="my_grocery_collection",
    metadata={"description": "A collection for storing grocery data"},
    configuration={"hnsw": {"space": "cosine"}, "embedding_function": ef},
)
print(f"[collection] {collection.name}")

# The sample data: grocery items, each with a unique id food_1, food_2, ...
texts = [
    "fresh red apples",
    "organic bananas",
    "ripe mangoes",
    "whole wheat bread",
    "farm-fresh eggs",
    "natural yogurt",
    "frozen vegetables",
    "grass-fed beef",
    "free-range chicken",
    "fresh salmon fillet",
    "aromatic coffee beans",
    "pure honey",
    "golden apple",
    "red fruit",
]
ids = [f"food_{index + 1}" for index, _ in enumerate(texts)]

# Add documents, metadata and ids: Chroma embeds the documents with the collection's embedding function
# (ids that already exist are skipped on a rerun)
collection.add(
    documents=texts,
    metadatas=[{"source": "grocery_store", "category": "food"} for _ in texts],
    ids=ids,
)

# get() with no arguments returns every item in the collection
all_items = collection.get()
print(f"[collection contents] {len(all_items['documents'])} documents")

# Similarity search: the 3 documents closest to "apple"
query_term = "apple"
results = collection.query(query_texts=[query_term], n_results=3)
print(f"[query results, {query_term}]")
pprint(results)

# Display the top 3 (results hold one list per query, so [0] is "apple"); distance is cosine, lower is more similar
print(f"[top 3, {query_term}]")
if not results["ids"][0]:
    print(f'  No documents found similar to "{query_term}"')
for doc_id, text, distance in zip(results["ids"][0], results["documents"][0], results["distances"][0], strict=True):
    print(f'  {doc_id:<8} {distance:.4f}  "{text or "Text not available"}"')

# Several queries in one call: pass a list to query_texts (and wrap a single string in one)
query_term = ["red", "fresh"]
if isinstance(query_term, str):
    query_term = [query_term]
results = collection.query(query_texts=query_term, n_results=3)

# Display the top 3 for each query: an outer loop over the per-query lists
for q, term in enumerate(query_term):
    print(f"[top 3, {term}]")
    for doc_id, text, distance in zip(results["ids"][q], results["documents"][q], results["distances"][q], strict=True):
        print(f'  {doc_id:<8} {distance:.4f}  "{text or "Text not available"}"')

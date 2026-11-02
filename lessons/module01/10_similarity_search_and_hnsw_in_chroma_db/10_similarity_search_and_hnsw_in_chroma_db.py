# Needs the Chroma server from this folder's docker-compose.yml: `docker compose up -d` here first.
from pprint import pprint

import chromadb
import numpy as np
from chromadb.utils import embedding_functions

from app.config.envs import CHROMA_HOST, CHROMA_PORT, EMBEDDING_MODEL

# Setup: an embedding function that turns documents into vectors
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)

# The data: four documents that all say "pandas", two about the animal and two about the library
documents = [
    "Giant pandas are a bear species that lives in mountainous areas.",
    "A pandas DataFrame stores two-dimensional, tabular data",
    "I think everyone agrees that pandas are some of the cutest animals on the planet",
    "A direct comparison between pandas and polars indicates that polars is a more efficient library than pandas.",
]

# Brute force, what a vector index avoids: normalize, dot the query with every document, rank by cosine distance
doc_vectors = np.array(ef(documents))
query_vector = np.array(ef(["cats"]))[0]
doc_vectors /= np.linalg.norm(doc_vectors, axis=1, keepdims=True)
query_vector /= np.linalg.norm(query_vector)
distances = 1 - doc_vectors @ query_vector
print("[brute force, cats]")
for i in np.argsort(distances):
    print(f"  id{i + 1}  {distances[i]:.4f}  {documents[i]}")

# Connect to the Chroma server over HTTP (client-server mode)
client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

# Configure the HNSW index when creating the collection (get_or_create, so the script can be rerun;
# the configuration only applies the first time, when the collection is actually created)
collection = client.get_or_create_collection(
    name="my_collection_name",
    metadata={"topic": "query testing"},
    configuration={
        "hnsw": {
            "space": "cosine",
            "ef_search": 100,
            "ef_construction": 100,
            "max_neighbors": 16,
        },
        "embedding_function": ef,
    },
)
print("[hnsw configuration]")
pprint(collection.configuration["hnsw"])

# Add data (ids that already exist are skipped on a rerun)
collection.add(
    documents=documents,
    metadatas=[
        {"topic": "animals"},
        {"topic": "data analysis"},
        {"topic": "animals"},
        {"topic": "data analysis"},
    ],
    ids=["id1", "id2", "id3", "id4"],
)

# Query: n_results above the collection size returns every document, most similar first
print("[query, cats]")
pprint(collection.query(query_texts=["cats"], n_results=10))

# "polar bear" goes wrong: "polar" matches the polars library
print("[query, polar bear]")
pprint(collection.query(query_texts=["polar bear"], n_results=1))

# Metadata filter: search only the documents about animals
print("[query, polar bear + where]")
pprint(collection.query(query_texts=["polar bear"], n_results=1, where={"topic": "animals"}))

# Full text filter: leave out documents that contain "library"
print("[query, polar bear + where_document]")
pprint(collection.query(query_texts=["polar bear"], n_results=1, where_document={"$not_contains": "library"}))

# Combine the metadata filter and the full text filter
print("[query, polar bear + where + where_document]")
pprint(
    collection.query(
        query_texts=["polar bear"],
        n_results=1,
        where={"topic": "animals"},
        where_document={"$not_contains": "library"},
    )
)

# Needs the Chroma server from this folder's docker-compose.yml: `docker compose up -d` here first.
from pprint import pprint

import chromadb
from chromadb.utils import embedding_functions

from app.config.envs import CHROMA_HOST, CHROMA_PORT, EMBEDDING_MODEL

# Setup: an embedding function that turns documents into vectors
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)

# Connect to the Chroma server over HTTP (client-server mode)
client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

# Create a collection (get_or_create, so the script can be rerun)
collection = client.get_or_create_collection(name="filter_demo", embedding_function=ef)
print(f"Collection created: {collection.name}")

# Add documents with metadata (ids that already exist are skipped on a rerun)
collection.add(
    documents=[
        "This is a document about LangChain",
        "This is a reading about LlamaIndex",
        "This is a book about Python",
        "This is a document about pandas",
        "This is another document about LangChain",
    ],
    metadatas=[
        {"source": "langchain.com", "version": 0.1},
        {"source": "llamaindex.ai", "version": 0.2},
        {"source": "python.org", "version": 0.3},
        {"source": "pandas.pydata.org", "version": 0.4},
        {"source": "langchain.com", "version": 0.5},
    ],
    ids=["id1", "id2", "id3", "id4", "id5"],
)

# Metadata filter: source equal to "langchain.com"
print("[metadata $eq]")
pprint(collection.get(where={"source": {"$eq": "langchain.com"}}))

# Leaving the operator out is the same as $eq
print("[metadata, no operator]")
pprint(collection.get(where={"source": "langchain.com"}))

# Combine filters with $and: LangChain documents with version below 0.3
print("[metadata $and + $lt]")
pprint(collection.get(where={"$and": [{"source": {"$eq": "langchain.com"}}, {"version": {"$lt": 0.3}}]}))

# Lists in filters with $in: LangChain or LlamaIndex documents with version below 0.3
print("[metadata $and + $in]")
pprint(
    collection.get(where={"$and": [{"source": {"$in": ["langchain.com", "llamaindex.ai"]}}, {"version": {"$lt": 0.3}}]})
)

# $nin ("not in"): every source except langchain.com and llamaindex.ai
print("[metadata $nin]")
pprint(collection.get(where={"source": {"$nin": ["langchain.com", "llamaindex.ai"]}}))

# Document filter (full text search): documents whose text contains "pandas"
print("[document $contains]")
pprint(collection.get(where_document={"$contains": "pandas"}))

# Document filters are case-sensitive: "Pandas" finds nothing
print("[document $contains, case-sensitive]")
pprint(collection.get(where_document={"$contains": "Pandas"}))

# $not_contains: documents whose text lacks "document"
print("[document $not_contains]")
pprint(collection.get(where_document={"$not_contains": "document"}))

# Combine metadata and document filters: "LangChain" or "Python" in the text, version above 0.1
print("[metadata + document]")
pprint(
    collection.get(
        where={"version": {"$gt": 0.1}},
        where_document={"$or": [{"$contains": "LangChain"}, {"$contains": "Python"}]},
    )
)

# The same where / where_document filters narrow a vector search in .query()
print("[query + filter]")
pprint(
    collection.query(
        query_texts=["frameworks for building LLM applications"],
        n_results=2,
        where={"version": {"$lt": 0.5}},
    )
)

## How to run
```sh
cd lessons/module01/11_similarity_search_using_chroma_and_python && docker compose up -d && cd -
make lesson LESSON=lessons/module01/11_similarity_search_using_chroma_and_python/11_similarity_search_using_chroma_and_python.py
```

Another lesson's Chroma server on port 8000 (09's, say) has to be stopped first
(`docker compose down` in its folder).

## Files

| File                                              | Holds                                                  |
| ------------------------------------------------- | ------------------------------------------------------ |
| `11_similarity_search_using_chroma_and_python.py` | the entry point: the lesson's steps, in order          |
| `vector_store.py`                                 | Chroma: the connection, the collection and `search()`  |
| `groceries.py`                                    | the sample data: grocery items, their ids and metadata |
| `docker-compose.yml`                              | the Chroma server, on `localhost:8000`                 |

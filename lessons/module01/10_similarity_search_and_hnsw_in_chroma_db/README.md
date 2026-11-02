## How to run
```sh
cd lessons/module01/10_similarity_search_and_hnsw_in_chroma_db && docker compose up -d && cd -
make lesson LESSON=lessons/module01/10_similarity_search_and_hnsw_in_chroma_db/10_similarity_search_and_hnsw_in_chroma_db.py
```

Another lesson's Chroma server on port 8000 (09's, say) has to be stopped first
(`docker compose down` in its folder).

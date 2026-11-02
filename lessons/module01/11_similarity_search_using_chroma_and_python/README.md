## How to run
```sh
cd lessons/module01/11_similarity_search_using_chroma_and_python && docker compose up -d && cd -
make lesson LESSON=lessons/module01/11_similarity_search_using_chroma_and_python/11_similarity_search_using_chroma_and_python.py
```

Another lesson's Chroma server on port 8000 (09's, say) has to be stopped first
(`docker compose down` in its folder).

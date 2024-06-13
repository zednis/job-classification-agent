Scripts used to prepare and upload O\*NET 28.3 data to an OpenAI Vector Store and create an OpenAI Assistant (v2) that has access to the vector store.

## Prepare Data `prepare_data.py`

Loads O\*NET 28.3 XLSX files from `data/raw` converts them into JSON Lines format and saves them to `data/processed`.

## Create Vector Store `create_vector_store.py`

Creates an OpenAI Vector Store and uploads all .json files in `data/processed`.

## Create Assistant `create_assistant_py`

Creates an OpenAI Assistant (v2) with a `file_search` tool with access the the vector store.

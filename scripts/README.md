Scripts used to prepare and upload O\*NET 28.3 data to an OpenAI Vector Store and create an OpenAI Assistant (v2) that has access to the vector store.

## Prepare Data `prepare_data.py`

Loads O\*NET 28.3 XLSX files from `data/raw` converts them into JSON Lines format and saves them to `data/processed`.

## Create Vector Store `create_vector_store.py`

Creates an OpenAI Vector Store and uploads all .json files in `data/processed`.

## Create Assistant `create_assistant_py`

Creates an OpenAI Assistant (v2) with a `file_search` tool with access the the vector store.

```
usage: create_assistant.py [-h] [--model {gpt-3.5-turbo,gpt-4o-mini,gpt-4o,gpt-4-turbo}] [--name NAME] vector_store_id

Create a Job Classification Assistant

positional arguments:
  vector_store_id       Vector Store ID (e.g. 'vs_UBHS....AlBE')

options:
  -h, --help            show this help message and exit
  --model {gpt-3.5-turbo,gpt-4o-mini,gpt-4o,gpt-4-turbo}
                        Model to use for the assistant (default: gpt-4o-mini)
  --name NAME           Assistant Name
```

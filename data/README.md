## /raw directory

O\*NET 28.3 XLSX files downloaded from ONET Website in 2024-06

Sources:

-   https://www.onetcenter.org/database.html#individual-files
-   https://www.onetonline.org/find/career?c=0 (Save Table > XLSX)

## /processed directory

To load the O\*NET 28.3 data into an OpenAI Vector store we will need to convert it into a supported format. We will also remove fields that we do not think will be useful to the assistant.

I have chosen JSON Lines (`.json` extension) as the target format.

The data processing is performed in by the `prepare_data.py` script and the OpenAI Vector Store is created and loaded in the `create_vector_store.py` script.

OpenAI Vector Store Links:

-   https://platform.openai.com/docs/assistants/tools/file-search/vector-stores
-   https://platform.openai.com/docs/assistants/tools/file-search/supported-files

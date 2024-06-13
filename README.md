# Job Classification Agent

An OpenAI Assistant that classifies job postings into [O*NET 28.3](https://www.onetonline.org/) occupations.



## dependencies

This project uses poetry to manage dependencies.

**prereqs**

-   python 3.12+
-   poetry

**installing dependencies**

-   run `poetry install`

## environment variables

-   `OPENAI_API_KEY` - OpenAI API Key
    -   created in OpenAI API Portal
    -   used in `create_vector_store.py`, `create_assstant.py`, and `app.py`
-   `VECTOR_STORE_ID` - id of the OpenAI Vector Store
    -   example: 'vs_H9I1....5eAC'
    -   created in `create_vector_store.py`
    -   used in `create_assistant.py`
-   `ASSISTANT_ID` - id of the OpenAI Assistant
    -   example: 'asst_EUmb....TUCJ'
    -   created in: `create_assistant.py`
    -   used in `app.py`

## scripts

Scripts used to prepare and upload O\*NET 28.3 data to an OpenAI Vector Store and create an OpenAI Assistant (v2) that has access to the vector store.

-   `prepare_data.py` - converts O\*NET 28.3 XLSX data into JSON Lines formats for the vector store
-   `create_vector_store.py` - Creates an OpenAI vector store and loads the processed JSON Lines data into it
-   `create_assistant.py` - Creates an OpenAI Assistant (v2) with access to the vector store

## Streamlit App `app.py`

-   `app.py` - Streamlit app to run the Job Classification Assistant

The streamlit app will

command:
`streamlit run appy.py`

# Links
- https://www.onetonline.org/
- https://platform.openai.com/docs/assistants/overview


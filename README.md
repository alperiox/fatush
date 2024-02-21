# Translation Toolkit

A collection of scripts to streamline the translation of markdown files using vector stores and deep learning.

## Overview

This toolkit provides a set of Python scripts designed to simplify the translation process for markdown files. The scripts leverage embedding models to enhance the accuracy of document retrieval and improve the overall translation workflow.

## Scripts

### Initialization Script

#### search_word.py

The `search_word.py` script initializes a search engine for retrieving relevant documents based on embeddings. It is designed to work with markdown files in multiple languages. The CLI app is based on [Typer](https://typer.tiangolo.com/).

#### Usage

1. **Installation:**
   - Install the module itself:
      - install the toolset: `pip install fatush`
      - then run the script: `fatush run`
   - Install the whole project:
      - Clone this repository: `git clone https://github.com/alperiox/fatush.git`
      - Change the directory to the project folder: `cd fatush`
      - Install the required dependencies using pip or poetry: `pip install -r requirements.txt` or `poetry install`

2. **Configuration:**
    - Run the initialization script: `python fatush/search_word.py run`
    - Follow the prompts to set up the initial configuration.
    - If the `config.yaml` file is not found, the script will fetch documents from the FastAPI repo and create the necessary configuration file.

3. **Processing Documents:**
    - The script will process the documents based on the provided configuration.
    - It'll split the documents line by line and then calculate their embeddings to set up a FAISS vector store.

4. **Loading Embedding Model:**
    - The used embedding model is [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), which is rather popular for vectorstores.

5. **Vector Store:**
    - If the vector store path is not found in the configuration, it will be constructed and loaded. It'll be loaded automatically otherwise.
    - Currently, the only implemented vector store is [FAISS](https://github.com/facebookresearch/faiss).

6. **Search Engine Initialization:**
    - The search engine is initialized with the loaded embedding model and vector store.
    - The script will start the inference process to provide relevant search results.

7. **TODOs:**
    - [ ] Integration tests
    - [ ] Hopefully, a web application based on FastAPI
    - [ ] Yet another tool for automatically suggesting initial translations for the given text
    - [ ] Currently, the scripts don't cover all exceptions. This may require you to reconfigure the script by deleting the config file and the downloaded repository if you do not run the script directly without configuring any options.

#### Configuration Options for `search_word.py`

- `source_lang`: Source language code (e.g., 'en').
- `translation_lang`: Translation language code (e.g., 'tr').
- `docs_path`: Path to the documents (default is the current working directory).
- `vectorstore_path`: Path to the vector store (default is the current working directory).

#### Note

Since the project is built on my experience with translating FastAPI documentation, a nicer abstraction is a must for a more generally usable toolset. That is because there are several hard-coded variables at the moment, like fetching the documentation from the FastAPI repository.

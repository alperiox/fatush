import typer
from rich import print

import os
import typing as t

from _utility_functions import get_markdown_paths, process_source_files, load_embedding_model, construct_vector_store, load_vector_store, initialize_search_engine
from search_engine import Engine

# define the function that'll fetch the documents from git repo of fastapi

def fetch_documents_from_repo(path: t.Optional[str] = ".") -> None:
    # clone the repo to the cwd or the given path
    # also construct the config.yaml file in cwd to save the path of the repo
    pass


def initialize(source_lang: t.Optional[str], translation_lang: t.Optional[str], vectorstore_path: t.Optional[str] = ".") -> None:
    # remove other languages and keep the source and translation languages if they're given
    # if not, keep all of them

    # crawl through the path and find the markdown files, fetch the path from the config file
    paths = get_markdown_paths()

    # build the source documents and translation documents
    source_documents, source_chunks = process_source_files(paths)

    # load the embedding model
    embedding = load_embedding_model()

    # now we can construct the vector store if it's not there
    if not os.path.exists((os.path.join(vectorstore_path, "faiss_db"))):
        print("[bold red] Couldn't find the vectorstore! [/bold red]")
        print("[green]Constructing...[/green]")
        # construct the vector store
        construct_vector_store(source_documents, embedding, vectorstore_path)
        print("[green]Loading...[/green]")
        vector_store = load_vector_store(vectorstore_path)
    
    else: # if the vector store is there, load it
        # load the vector store
        print("[bold green] Found the vectorstore! [/bold green]")
        print("[green]Loading...[/green]")
        vector_store = load_vector_store(vectorstore_path)

    # now we can set up the search engine
    engine = Engine(embedding, vector_store, source_chunks, source_lang, translation_lang)
    print("[bold green] Search engine initialized! [/bold green]")
    print("[green]Starting the inference server...[/green]")
    engine.run() # starts the FastAPI inference server

if __name__ == "__main__":
    typer.run(initialize)
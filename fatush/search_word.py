import typer
from rich import print
from rich.prompt import Prompt

import os
import shutil

import typing as t

from fatush.utils.config import load_config, add_config, create_config
from fatush.utils.script import load_embedding_model
from fatush.utils.engine import (
    fetch_documents_from_repo,
    get_markdown_paths,
    process_source_files,
    construct_vector_store,
    load_vector_store,
)
from fatush.search_engine import Engine

app = typer.Typer()


@app.command("clean")
def clean() -> None:
    try:
        config = load_config()
    except FileNotFoundError:
        print(
            "[bold red]Couldn't find the config.yaml file... please run the project[/bold red]"
        )
        return
    print("[bold red]Cleaning the environment...[/bold red]")
    print("[cyan]Removing the vectorstore...[/cyan]")
    try:
        shutil.rmtree(config["vectorstore_path"])
    except FileNotFoundError:
        print("[bold red]Couldn't find the vectorstore![/bold red]")
    print("[bold green]Vectorstore removed![/bold green]")
    print("[cyan]Removing the documents...[/cyan]")
    try:
        shutil.rmtree(config["path"])
    except FileNotFoundError:
        print("[bold red]Couldn't find the documents![/bold red]")

    print("[bold green]Documents removed![/bold green]")
    print("[cyan]Removing the config file...[/cyan]")
    print("[bold green]Environment cleaned![/bold green]")


@app.command("run")
def initialize(
    source_lang: t.Optional[str] = "",
    translation_lang: t.Optional[str] = "",
    docs_path: t.Optional[str] = os.getcwd(),
    vectorstore_path: t.Optional[str] = os.getcwd(),
) -> None:
    try:
        config = load_config()
    except FileNotFoundError:
        print("[bold red]Couldn't find the config.yaml file...[/bold red]")
        print("[cyan]Fetching the documents from the FastAPI repo...[/cyan]")
        fetch_documents_from_repo(docs_path)
        # construct the config.yaml file
        create_config()
        add_config("path", os.path.join(docs_path, "docs"))
        print("[bold green]Documents fetched![/bold green]")

        if len(source_lang) == 0:
            source_lang = Prompt.ask(
                "[bold cyan]Enter the source language code (ex. 'en')[/bold cyan]"
            )
        if len(translation_lang) == 0:
            translation_lang = Prompt.ask(
                "[bold cyan]Enter the translation language code (ex. 'tr')[/bold cyan]"
            )

        add_config("source_language", source_lang)
        add_config("translation_language", translation_lang)

        config = load_config()

    print("[bold cyan] Current configuration: [/bold cyan]")
    print(config)

    print("Starting to process the documents...")
    # crawl through the path and find the markdown files, fetch the path from the config file
    paths = get_markdown_paths()
    print("[bold green]Paths fetched![/bold green]")
    # build the source documents and translation documents
    source_documents, source_chunks = process_source_files(paths)
    print("[bold green]Documents processed![/bold green]")

    print("Loading the embedding model...")
    # load the embedding model
    embedding = load_embedding_model()
    print("[green]Embedding model loaded![/green]")

    # now we can construct the vector store if it's not there
    if not config.get("vectorstore_path"):
        print("[bold red] Couldn't find the vectorstore_path! [/bold red]")
        print("[green]Constructing...[/green]")
        # construct the vector store
        construct_vector_store(source_documents, embedding, vectorstore_path)
        print("[green]Loading...[/green]")
        vector_store = load_vector_store(
            embedding, os.path.join(vectorstore_path, "faiss_db")
        )

    else:  # if the vector store is there, load it
        # load the vector store
        print("[bold green]Found the vectorstore! [/bold green]")
        print("[green]Loading...[/green]")
        vector_store = load_vector_store(embedding, config.get("vectorstore_path"))

    print("[bold green]Vector store loaded! [/bold green]")

    # now we can set up the search engine
    engine = Engine(embedding, vector_store, source_lang, translation_lang)
    print("[bold green]Search engine initialized! [/bold green]")
    print("[green]Starting the inference[/green]")
    engine.run()


if __name__ == "__main__":
    app()

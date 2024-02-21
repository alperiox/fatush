import typing as t

import os
from pathlib import Path

import subprocess

from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import shutil

from fatush.utils.script import (
    read_file,
    split_to_line_chunks,
    clean_chunks,
    line_chunks_to_documents,
)
from fatush.utils.config import add_config, load_config, CONFIG_PATH


from rich.progress import track


# define the function that'll fetch the documents from git repo of fastapi
def fetch_documents_from_repo(path: t.Optional[str] = os.getcwd()) -> None:
    # clone the repo to the cwd or the given path
    subprocess.run(
        [
            "git",
            "clone",
            "https://github.com/tiangolo/fastapi",
            os.path.join(path, "fastapi"),
        ]
    )
    shutil.move(os.path.join(path, "fastapi", "docs"), os.path.join(path, "docs"))
    shutil.rmtree(os.path.join(path, "fastapi"))


def get_markdown_paths(config_path: str = CONFIG_PATH) -> t.List[t.Tuple[Path, Path]]:
    # read the config.yaml file and fetch the paths
    assert os.path.exists(config_path), "Couldn't find the config.yaml file!"
    config = load_config(path=config_path)
    path = Path(config["path"])
    source_lang = config["source_language"]
    translation_lang = config["translation_language"]

    # crawl the files in the target_lang directory and save the file paths
    translated_files = []

    translated_docs_path = path / translation_lang / "docs"

    for idx, (root, dirs, files) in enumerate(os.walk(translated_docs_path)):
        for file in files:
            fpath = path / root / file
            translated_files.append(fpath)

    # now construct the corresponding source file paths
    # (assuming that the source and translation files are in the same directory structure
    # and have the same names)
    source_files = [
        path / source_lang / "docs" / filepath.relative_to(translated_docs_path)
        for filepath in translated_files
    ]

    return list(zip(translated_files, source_files))


def process_source_files(
    paths: t.List[t.Tuple[Path, Path]],
) -> t.Tuple[t.List[Document], t.List[dict]]:
    # # build the source documents and translation documents
    all_source_documents = []
    all_source_chunks = []

    for translated_filepath, source_filepath in track(
        paths, description="[cyan]Processing the files"
    ):
        source_file = read_file(source_filepath)
        translated_file = read_file(translated_filepath)

        source_chunks = split_to_line_chunks(source_file)
        translated_chunks = split_to_line_chunks(translated_file)

        # calculate the margin
        margin = abs(len(source_chunks) - len(translated_chunks)) // 2 + 1

        # clean the chunks
        source_chunks = clean_chunks(source_chunks)

        # now get the documents
        source_documents = line_chunks_to_documents(
            source_chunks, source_filepath, translated_filepath, margin
        )

        all_source_documents.extend(source_documents)
        all_source_chunks.extend(source_chunks)

    # filter out the empty documents
    all_source_documents = [
        doc for doc in all_source_documents if doc.page_content != ""
    ]

    return all_source_documents, all_source_chunks


def construct_vector_store(
    documents: t.List[Document],
    embedding_model: HuggingFaceEmbeddings,
    vectorstore_path: t.Optional[str] = ".",
    config_path: str = CONFIG_PATH,
) -> None:
    # construct the vector store

    vector_store = FAISS.from_documents(documents, embedding_model)
    vector_store.add_documents(documents)

    # save the vector store
    vector_store.save_local(os.path.join(vectorstore_path, "faiss_db"))

    # modify the configuration file
    config = load_config(path=config_path)
    config["vectorstore_path"] = os.path.join(vectorstore_path, "faiss_db")
    add_config(
        "vectorstore_path", os.path.join(vectorstore_path, "faiss_db"), path=config_path
    )


def load_vector_store(
    embedding: HuggingFaceEmbeddings, vectorstore_path: t.Optional[str] = "."
) -> FAISS:
    vector_store = FAISS.load_local(vectorstore_path, embedding)
    return vector_store

import pytest

from utils.engine import (
    fetch_documents_from_repo,
    get_markdown_paths,
    process_source_files,
    construct_vector_store,
    load_vector_store,
)

from utils.script import load_embedding_model

from langchain_core.documents import Document

from utils.config import add_config, create_config


# test if we can fetch the documents


@pytest.fixture(scope="session")
def temp_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("repo")
    # clone the repo to the to the temporary path
    return fn


@pytest.fixture(scope="session")
def temp_config(temp_dir):
    config_path = temp_dir / "config.yaml"
    create_config(config_path)
    add_config("path", str(temp_dir / "docs"), config_path)
    add_config("source_language", "en", config_path)
    add_config("translation_language", "tr", config_path)
    return config_path


@pytest.fixture(scope="session")
def temp_emb(temp_dir):
    return load_embedding_model()


def test_fetch_documents_from_repo(temp_dir):
    # clone the repo to the to the temporary directory
    fetch_documents_from_repo(temp_dir)
    # test if there's a directory named 'docs' in the temporary path
    assert (temp_dir / "docs").exists()
    # I should also check if the checksum of the cloned repo until a given
    # commit is same as the checksum of the repo until the same commit
    # but I don't know how to do that yet


def test_get_markdown_paths(temp_config):
    # get_markdown_paths should return a list of tuples
    # where the first element is the path to the translated file
    # and the second element is the path to the source file
    # for each file in the translated directory

    paths = get_markdown_paths(temp_config)

    # check if the paths are correct
    for translated, source in paths:
        assert translated.exists(), f"{translated} doesn't exist"
        assert source.exists(), f"{source} doesn't exist"
        assert translated.name == source.name, "The file names are not the same"


def test_process_source_files(temp_config):
    # get the markdown paths first
    paths = get_markdown_paths(temp_config)

    results = process_source_files(paths)

    # the results should be a tuple of two lists
    # one of them should be the list of documents
    # the other should be the list of chunks
    assert len(results) == 2, "The length of the results is not 2"
    assert isinstance(results[0], list), "The first element is not a list"
    assert isinstance(results[1], list), "The second element is not a list"

    # check if the first element just contains documents
    for doc in results[0]:
        assert len(doc.page_content) > 0, "The page content is empty"
        assert isinstance(doc, Document), "The element is not a Document"

    # check if the second element just contains dictionaries
    for chunk in results[1]:
        assert isinstance(chunk, dict), "The element is not a dictionary"

    # the data structures are already tested in the script_test.py
    # thus I don't need to test them again


def test_construct_vector_store(temp_config, temp_emb):
    # get the markdown paths first
    paths = get_markdown_paths(temp_config)

    # process the source files
    results = process_source_files(paths)

    # get the documents
    documents = results[0]

    # construct the vector store
    vectorstore_path = temp_config.parent
    construct_vector_store(
        documents,
        embedding_model=temp_emb,
        config_path=temp_config,
        vectorstore_path=vectorstore_path,
    )

    # check if the vector store is created
    assert (temp_config.parent / "faiss_db").exists(), "The vector store is not created"
    assert (
        temp_config.parent / "faiss_db"
    ).is_dir(), "The vector store is not a directory"
    assert (
        temp_config.parent / "faiss_db" / "index.faiss"
    ).exists(), "The index file is not created"
    assert (
        temp_config.parent / "faiss_db" / "index.faiss"
    ).is_file(), "The index file is not a file"
    assert (
        temp_config.parent / "faiss_db" / "index.pkl"
    ).exists(), "The index file is not created"
    assert (
        temp_config.parent / "faiss_db" / "index.pkl"
    ).is_file(), "The index file is not a file"


def test_load_vector_store(temp_config, temp_emb):
    # get the markdown paths first
    paths = get_markdown_paths(temp_config)

    # process the source files
    results = process_source_files(paths)

    # get the documents
    documents = results[0]

    # construct the vector store
    vectorstore_path = temp_config.parent / "faiss_db"
    construct_vector_store(
        documents,
        embedding_model=temp_emb,
        config_path=temp_config,
        vectorstore_path=vectorstore_path,
    )

    # load the vector store
    vector_store = load_vector_store(temp_emb, vectorstore_path)

    # check if the vector store is loaded
    assert vector_store is not None, "The vector store is not loaded"
    assert vector_store.index.is_trained, "The index is not trained"
    assert vector_store.index.ntotal > 0, "The index is empty"

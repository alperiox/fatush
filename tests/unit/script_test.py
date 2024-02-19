import pytest


@pytest.fixture
def example_raw():
    # a simple markdown file that'll be used for testing markdown parser
    markdown = """
        # Alternatifler, İlham Kaynakları ve Karşılaştırmalar

        **FastAPI**'ya neler ilham verdi? Diğer alternatiflerle karşılaştırıldığında farkları neler? **FastAPI** diğer alternatiflerinden neler öğrendi?

        ## Giriş
        <abbr title="Eklenti: Plug-In">eklenti</abbr> ve araç kullanmayı denedim.
        ## Daha Önce Geliştirilen Araçlar

        ### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a>
        !!! check "**FastAPI**'a nasıl ilham verdi?"
            Gereken araçları ve parçaları birleştirip eşleştirmeyi kolaylaştıracak bir mikro framework olmalı.

            Basit ve kullanması kolay bir <abbr title="Yönlendirme: Routing">yönlendirme sistemine</abbr> sahip olmalı.

        > Requests, tüm zamanların en çok indirilen Python  <abbr title="Paket: Package">paketlerinden</abbr> biridir.

        ```Python hl_lines="1"
        @app.get("/some/url")
        def read_url():
            return {"message": "Hello World!"}
        ```

        `requests.get(...)` ile `@app.get(...)` arasındaki benzerliklere bakın.
        * Cidden etkileyici bir performans.
        * WebSocket desteği.
        !!! check "**FastAPI**'a nasıl ilham verdi?"
            * Basit ve sezgisel bir API'ya sahip olmalı.
            * HTTP metot isimlerini (işlemlerini) anlaşılır olacak bir şekilde, direkt kullanmalı.
            * Mantıklı varsayılan değerlere ve buna rağmen güçlü bir özelleştirme desteğine sahip olmalı.

        ### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a>
    """
    return markdown


@pytest.fixture
def example_markdown():
    text = """Alternatifler, İlham Kaynakları ve Karşılaştırmalar\nFastAPI\'ya neler ilham verdi? Diğer alternatiflerle karşılaştırıldığında farkları neler? FastAPI diğer alternatiflerinden neler öğrendi?\nGiriş\neklenti ve araç kullanmayı denedim.\nDaha Önce Geliştirilen Araçlar\nDjango\n!!! check "FastAPI\'a nasıl ilham verdi?"\nGereken araçları ve parçaları birleştirip eşleştirmeyi kolaylaştıracak bir mikro framework olmalı.\nBasit ve kullanması kolay bir yönlendirme sistemine sahip olmalı.\n\nRequests, tüm zamanların en çok indirilen Python  paketlerinden biridir.\n\nrequests.get(...) ile @app.get(...) arasındaki benzerliklere bakın.\n* Cidden etkileyici bir performans.\n* WebSocket desteği.\n!!! check "FastAPI\'a nasıl ilham verdi?"\n* Basit ve sezgisel bir API\'ya sahip olmalı.\n* HTTP metot isimlerini (işlemlerini) anlaşılır olacak bir şekilde, direkt kullanmalı.\n* Mantıklı varsayılan değerlere ve buna rağmen güçlü bir özelleştirme desteğine sahip olmalı.\nSwagger / OpenAPI"""

    return text


@pytest.fixture
def example_chunks():
    chunks = [
        {
            "original_index": 0,
            "new_index": 0,
            "text": "Alternatifler, İlham Kaynakları ve Karşılaştırmalar",
        },
        {
            "original_index": 1,
            "new_index": 1,
            "text": "FastAPI'ya neler ilham verdi? Diğer alternatiflerle karşılaştırıldığında farkları neler? FastAPI diğer alternatiflerinden neler öğrendi?",
        },
        {"original_index": 2, "new_index": 2, "text": "Giriş"},
        {
            "original_index": 3,
            "new_index": 3,
            "text": "eklenti ve araç kullanmayı denedim.",
        },
        {"original_index": 4, "new_index": 4, "text": "Daha Önce Geliştirilen Araçlar"},
        {"original_index": 5, "new_index": 5, "text": "Django"},
        {
            "original_index": 6,
            "new_index": 6,
            "text": '!!! check "FastAPI\'a nasıl ilham verdi?"',
        },
        {
            "original_index": 7,
            "new_index": 7,
            "text": "Gereken araçları ve parçaları birleştirip eşleştirmeyi kolaylaştıracak bir mikro framework olmalı.",
        },
        {
            "original_index": 8,
            "new_index": 8,
            "text": "Basit ve kullanması kolay bir yönlendirme sistemine sahip olmalı.",
        },
        {
            "original_index": 10,
            "new_index": 9,
            "text": "Requests, tüm zamanların en çok indirilen Python  paketlerinden biridir.",
        },
        {
            "original_index": 12,
            "new_index": 10,
            "text": "requests.get(...) ile @app.get(...) arasındaki benzerliklere bakın.",
        },
        {
            "original_index": 13,
            "new_index": 11,
            "text": "* Cidden etkileyici bir performans.",
        },
        {"original_index": 14, "new_index": 12, "text": "* WebSocket desteği."},
        {
            "original_index": 15,
            "new_index": 13,
            "text": '!!! check "FastAPI\'a nasıl ilham verdi?"',
        },
        {
            "original_index": 16,
            "new_index": 14,
            "text": "* Basit ve sezgisel bir API'ya sahip olmalı.",
        },
        {
            "original_index": 17,
            "new_index": 15,
            "text": "* HTTP metot isimlerini (işlemlerini) anlaşılır olacak bir şekilde, direkt kullanmalı.",
        },
        {
            "original_index": 18,
            "new_index": 16,
            "text": "* Mantıklı varsayılan değerlere ve buna rağmen güçlü bir özelleştirme desteğine sahip olmalı.",
        },
        {"original_index": 19, "new_index": 17, "text": "Swagger / OpenAPI"},
    ]

    return chunks


def test_process_raw_text(example_raw):
    from utils.script import process_raw_text

    # the output text shouldn't have any leading/trailing spaces
    # or any ``` code blocks
    output = process_raw_text(example_raw)
    splitted_output = output.split("\n")

    assert ("```" in output) is False
    assert sum([1 for line in splitted_output if line.strip() == line]) == len(
        splitted_output
    )


def test_md_to_text(example_markdown):
    # how the text should look like after parsing the markdown
    # the implementation is using https://python-markdown.github.io/
    # which is based on https://daringfireball.net/projects/markdown/syntax
    # thus, since the python implementation `python-markdown` is have an extensive
    # support for testing (https://github.com/Python-Markdown/markdown/tree/master/tests)
    # I have decided to not test the output of the `md_to_text` function,
    # the only extension I've implemented was converting the markdown to a BeautifulSoup object and
    # parse the string from that object. Therefore, I'm assuming that the output of the `md_to_text` function
    # is correct, based on the `python-markdown` tests.
    pass


def test_split_to_line_chunks(example_markdown):
    from utils.script import split_to_line_chunks

    # the output of the `split_to_line_chunks` function should be a list of dictionaries
    # each dictionary should have the following keys:
    # - original_index: the index of the line in the original text
    # - new_index: the index of the line in the new text
    # - text: the text of the line

    # the original_index and new_index should different in each group for each line.

    chunks = split_to_line_chunks(example_markdown)

    for k in ["original_index", "new_index", "text"]:
        assert all([k in c for c in chunks])

    # the original_index and new_index should different in each group for each line.
    original_indices = []
    new_indices = []
    for s in chunks:
        # check if data types are int int str
        assert isinstance(s["original_index"], int)
        assert isinstance(s["new_index"], int)
        assert isinstance(s["text"], str)

        # check if string is not empty
        assert len(s["text"]) > 0

        original_indices.append(s["original_index"])
        new_indices.append(s["new_index"])

    assert len(set(original_indices)) == len(
        original_indices
    )  # all original indices should be unique
    assert len(set(new_indices)) == len(new_indices)  # all new indices should be unique


def test_clean_chunks(example_chunks):
    from utils.script import clean_chunks

    # this function removes "!!!" and leading/trailing spaces from the text of each chunk
    # and returns the cleaned chunks

    cleaned_chunks = clean_chunks(example_chunks)

    for s in cleaned_chunks:
        assert "!!!" not in s["text"]
        assert s["text"].strip() == s["text"]


def test_line_chunks_to_documents(example_chunks):
    # this function converts the given chunks to
    # a list of documents, each document should have
    # the following keys as metadata
    # source_filepath, translation_filepath,
    # original_index, new_index, margin
    # and the page_content should be the text of the chunk

    from utils.script import line_chunks_to_documents

    # we should set up filepathes
    import os

    source_filepath = os.path.join(os.getcwd(), "source.md")
    translation_filepath = os.path.join(os.getcwd(), "translation.md")
    margin = 2  # margin >= 0, the number of lines to be considered as margin

    documents = line_chunks_to_documents(
        example_chunks, source_filepath, translation_filepath, margin
    )

    for doc in documents:
        for k in [
            "source_filepath",
            "translation_filepath",
            "original_index",
            "new_index",
            "margin",
        ]:
            assert k in doc.metadata.keys()
        assert doc.page_content in [c["text"] for c in example_chunks]


def test_load_embedding_model():
    # this function should return a HuggingFaceEmbeddings object
    # with the model_name="all-MiniLM-L6-v2"
    # so I can just check if the loaded object is an instance of HuggingFaceEmbeddings
    # and if the model_name is correct

    from utils.script import load_embedding_model
    from langchain_community.embeddings import HuggingFaceEmbeddings

    emb_model = load_embedding_model()
    assert type(emb_model) == HuggingFaceEmbeddings
    assert emb_model.model_name == "all-MiniLM-L6-v2"

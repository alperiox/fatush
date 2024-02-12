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

    assert (
        process_raw_text(example_raw)
        == """\n# Alternatifler, İlham Kaynakları ve Karşılaştırmalar\n\n**FastAPI**\'ya neler ilham verdi? Diğer alternatiflerle karşılaştırıldığında farkları neler? **FastAPI** diğer alternatiflerinden neler öğrendi?\n\n## Giriş\n<abbr title="Eklenti: Plug-In">eklenti</abbr> ve araç kullanmayı denedim.\n## Daha Önce Geliştirilen Araçlar\n\n### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a>\n!!! check "**FastAPI**\'a nasıl ilham verdi?"\nGereken araçları ve parçaları birleştirip eşleştirmeyi kolaylaştıracak bir mikro framework olmalı.\n\nBasit ve kullanması kolay bir <abbr title="Yönlendirme: Routing">yönlendirme sistemine</abbr> sahip olmalı.\n\n> Requests, tüm zamanların en çok indirilen Python  <abbr title="Paket: Package">paketlerinden</abbr> biridir.\n\n\n`requests.get(...)` ile `@app.get(...)` arasındaki benzerliklere bakın.\n* Cidden etkileyici bir performans.\n* WebSocket desteği.\n!!! check "**FastAPI**\'a nasıl ilham verdi?"\n* Basit ve sezgisel bir API\'ya sahip olmalı.\n* HTTP metot isimlerini (işlemlerini) anlaşılır olacak bir şekilde, direkt kullanmalı.\n* Mantıklı varsayılan değerlere ve buna rağmen güçlü bir özelleştirme desteğine sahip olmalı.\n\n### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a>\n"""
    )


def test_md_to_text(example_markdown):
    from utils.script import md_to_text

    assert (
        md_to_text(example_markdown)
        == """Alternatifler, İlham Kaynakları ve Karşılaştırmalar\nFastAPI\'ya neler ilham verdi? Diğer alternatiflerle karşılaştırıldığında farkları neler? FastAPI diğer alternatiflerinden neler öğrendi?\nGiriş\neklenti ve araç kullanmayı denedim.\nDaha Önce Geliştirilen Araçlar\nDjango\n!!! check "FastAPI\'a nasıl ilham verdi?"\nGereken araçları ve parçaları birleştirip eşleştirmeyi kolaylaştıracak bir mikro framework olmalı.\nBasit ve kullanması kolay bir yönlendirme sistemine sahip olmalı.\n\nRequests, tüm zamanların en çok indirilen Python  paketlerinden biridir.\n\nrequests.get(...) ile @app.get(...) arasındaki benzerliklere bakın.\n* Cidden etkileyici bir performans.\n* WebSocket desteği.\n!!! check "FastAPI\'a nasıl ilham verdi?"\n* Basit ve sezgisel bir API\'ya sahip olmalı.\n* HTTP metot isimlerini (işlemlerini) anlaşılır olacak bir şekilde, direkt kullanmalı.\n* Mantıklı varsayılan değerlere ve buna rağmen güçlü bir özelleştirme desteğine sahip olmalı.\nSwagger / OpenAPI"""
    )


def test_split_to_line_chunks(example_markdown):
    from utils.script import split_to_line_chunks

    answer = [
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

    assert split_to_line_chunks(example_markdown) == answer


def test_clean_chunks(example_chunks):
    from utils.script import clean_chunks

    answer = [
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
            "text": '"FastAPI\'a nasıl ilham verdi?"',
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
            "text": '"FastAPI\'a nasıl ilham verdi?"',
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

    assert clean_chunks(example_chunks) == answer

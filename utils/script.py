from langchain_core.documents import Document
import markdown
from bs4 import BeautifulSoup

from langchain_community.embeddings import HuggingFaceEmbeddings


def load_embedding_model() -> HuggingFaceEmbeddings:
    emb_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return emb_model


def fetch_matched_text(match: Document, fetch_from: str):
    line = match.metadata["new_index"]
    margin = match.metadata["margin"]

    if fetch_from == "source":
        content = read_file(match.metadata["source_filepath"])
    elif fetch_from == "translation":
        content = read_file(match.metadata["translation_filepath"])
    else:
        raise ValueError("fetch_from should be either 'source' or 'translation'")

    chunks = split_to_line_chunks(content)
    chunks = chunks[line - margin : line + margin]

    return "\n".join([chunk["text"] for chunk in chunks])


def line_chunks_to_documents(
    line_chunks, source_filepath, translation_filepath, margin
):
    documents = []
    for chunk in line_chunks:
        metadata = {
            "source_filepath": source_filepath,
            "translation_filepath": translation_filepath,
            "original_index": chunk["original_index"],
            "new_index": chunk["new_index"],
            "margin": margin,
        }

        chunk_doc = Document(page_content=chunk["text"], metadata=metadata)
        documents.append(chunk_doc)

    return documents


def split_to_line_chunks(text_) -> list[str]:
    text = md_to_text(text_)
    splitted_text = text.split("\n")
    # index the lines
    text_indexed = [(idx, line) for idx, line in enumerate(splitted_text)]
    text_filtered = list(filter(lambda x: len(x[1]) > 0, text_indexed))

    # reindex again
    chunks = [
        {"original_index": idx, "new_index": new_idx, "text": line}
        for new_idx, (idx, line) in enumerate(text_filtered)
    ]

    return chunks


def clean_chunks(raw_chunks):
    chunks = []
    for raw_chunk in raw_chunks:
        chunk = raw_chunk.copy()
        # remove the !!! ... tag from the line if it exist
        if chunk["text"].startswith("!!!"):
            chunk["text"] = chunk["text"].replace(
                " ".join(chunk["text"].split(" ")[:2]), ""
            )

        chunk["text"] = chunk["text"].strip()

        chunks.append(chunk)

    return chunks


def md_to_text(md):
    md = process_raw_text(md)

    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text()


def process_raw_text(text):
    lines = list(map(lambda x: x.strip(), text.split("\n")))
    code_block_flag = False
    cleaned_lines = []
    for line in lines:
        if line.startswith("```"):
            code_block_flag = not code_block_flag

        if not (code_block_flag or line.startswith("```")):
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def read_file(filepath):
    with open(filepath, "r") as f:
        return f.read()

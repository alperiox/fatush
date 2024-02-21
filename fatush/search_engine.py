from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


from rich.prompt import Prompt
from rich import print
from datetime import datetime
from fatush.utils.script import fetch_matched_text


class Engine:
    def __init__(
        self,
        embedding: HuggingFaceEmbeddings,
        vector_store: FAISS,
        source_lang: str,
        translation_lang: str,
    ):
        self.embedding = embedding
        self.vector_store = vector_store
        self.source_lang = source_lang
        self.translation_lang = translation_lang
        self.top_k = 3
        self.queries = []

    def run(self):
        print("[bold cyan]Ready![/bold cyan]")
        while True:
            query = Prompt.ask("Enter the query")
            if len(query) == 0:
                break

            results = self.search(query)

            result_string = ""
            for idx, result in enumerate(results, 1):
                result_string += "[bold green]" + "-" * 30 + "[/bold green]\n"
                result_string += (
                    f"[green]Result {idx}, score: {result['score']}[/green]\n"
                )
                result_string += "[cyan]Source match[/cyan]\n"
                result_string += f"{result['source_match']}\n"
                result_string += "[cyan]Translation match[/cyan]\n"
                result_string += f"{result['translation_match']}\n"

            print(result_string)

    def search(self, query):
        # search the vector store with the query vector
        results = self.vector_store.similarity_search_with_score(query, k=self.top_k)
        # fetch the documents from the results
        results = self._parse_results(results)
        self.queries.append(
            {"query": query, "results": results, "timestamp": datetime.now()}
        )

        return results

    def _parse_results(self, results):
        parsed_results = []
        for result in results:
            doc = result[0]
            score = result[1]
            source_match = fetch_matched_text(doc, fetch_from="source")
            translation_match = fetch_matched_text(doc, fetch_from="translation")

            parsed_result = {
                "doc": doc,
                "score": score,
                "source_match": source_match,
                "translation_match": translation_match,
            }
            parsed_results.append(parsed_result)

        return parsed_results

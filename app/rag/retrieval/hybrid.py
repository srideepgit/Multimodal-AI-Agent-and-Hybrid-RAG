# Merge dense + BM25 results into a single ranked list.

class HybridRetriever:
    """
    Merges dense and BM25 search results.

    Both inputs are expected to be lists of normalized dicts:
        {"id": ..., "text": ..., "metadata": {...}, "score": float}

    Chunks found by both retrievers have their scores summed, which
    rewards results that both search strategies agree on.
    """

    def merge(
        self,
        dense_results,
        bm25_results,
        top_k: int = 10,
    ):

        merged = {}

        for result in dense_results:
            chunk_id = result["id"]
            merged[chunk_id] = dict(result)

        for result in bm25_results:
            chunk_id = result["id"]

            if chunk_id in merged:
                merged[chunk_id]["score"] += result["score"]
            else:
                merged[chunk_id] = dict(result)

        ranked = sorted(
            merged.values(),
            key=lambda item: item["score"],
            reverse=True,
        )

        return ranked[:top_k]

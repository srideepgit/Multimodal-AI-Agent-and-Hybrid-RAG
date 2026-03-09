# Metadata = data about the data.

from pathlib import Path

from langchain_core.documents import Document


class MetadataBuilder:
    """
    Builds and enriches metadata for document chunks.
    """

    def build(
        self,
        documents: list[Document],
    ) -> list[Document]:

        total_chunks = len(documents)

        enriched_documents = []

        for index, document in enumerate(documents):

            metadata = dict(document.metadata)

            source = metadata.get("source", "")

            file_path = Path(source)

            metadata.update(
                {
                    "document_name": file_path.name,
                    "file_type": file_path.suffix.lower().replace(".", ""),
                    "chunk_index": index,
                    "total_chunks": total_chunks,
                }
            )

            enriched_documents.append(
                Document(
                    page_content=document.page_content,
                    metadata=metadata,
                )
            )

        return enriched_documents
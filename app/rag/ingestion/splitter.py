# Clean Doc Text -> Split ( default 500 chars, 100 overlap )

from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter

from .schemas import Chunk, ChunkMetadata


class DocumentSplitter:

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split(self, documents):
        chunks = []

        split_docs = self.splitter.split_documents(documents)

        total_chunks = len(split_docs)

        for idx, doc in enumerate(split_docs):

            source = doc.metadata.get("source", "")

            metadata = ChunkMetadata(
                source=source,
                file_name=doc.metadata.get("document_name", source),
                file_type=doc.metadata.get("file_type", ""),
                page=doc.metadata.get("page"),
                section=doc.metadata.get("section"),
                chunk_index=idx,
                total_chunks=total_chunks,
            )

            chunks.append(
                Chunk(
                    id=str(uuid4()),
                    text=doc.page_content,
                    metadata=metadata,
                )
            )

        return chunks

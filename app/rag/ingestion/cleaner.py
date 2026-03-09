# Load Documents -> Clean text

import re

from langchain_core.documents import Document


class DocumentCleaner:
    """
    Cleans raw documents before chunking.
    """

    def clean(self, documents: list[Document]) -> list[Document]:
        cleaned_documents = []

        for document in documents:
            text = document.page_content

            text = self._normalize_newlines(text)
            text = self._remove_tabs(text)
            text = self._remove_extra_spaces(text)
            text = self._remove_extra_blank_lines(text)
            text = self._strip(text)

            cleaned_documents.append(
                Document(
                    page_content=text,
                    metadata=document.metadata,
                )
            )

        return cleaned_documents

    def _normalize_newlines(self, text: str) -> str:
        return text.replace("\r\n", "\n").replace("\r", "\n")

    def _remove_tabs(self, text: str) -> str:
        return text.replace("\t", " ")

    def _remove_extra_spaces(self, text: str) -> str:
        return re.sub(r"[ ]{2,}", " ", text)

    def _remove_extra_blank_lines(self, text: str) -> str:
        return re.sub(r"\n{3,}", "\n\n", text)

    def _strip(self, text: str) -> str:
        return text.strip()
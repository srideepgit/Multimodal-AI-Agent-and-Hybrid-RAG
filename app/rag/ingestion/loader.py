# Documents Load

from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader,
    UnstructuredHTMLLoader,
)


class UnsupportedFileTypeError(Exception):
    """Raised when the file type is not supported."""
    pass


class DocumentLoader:
    """
    Loads enterprise documents into LangChain Document objects.
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".md",
        ".txt",
        ".csv",
        ".html",
        ".htm",
    }

    def load(self, file_path: str | Path) -> list[Document]:
        """
        Detect file type and load a single document.
        """

        # PATH

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

        # EXTENSIONS

        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise UnsupportedFileTypeError(
                f"{extension} is not supported."
            )

        if extension == ".pdf":
            return self._load_pdf(path)

        if extension == ".docx":
            return self._load_docx(path)

        if extension in {".md", ".txt"}:
            return self._load_text(path)

        if extension == ".csv":
            return self._load_csv(path)

        if extension in {".html", ".htm"}:
            return self._load_html(path)

        raise UnsupportedFileTypeError(extension)

    def load_directory(self, directory_path: str | Path) -> list[Document]:
        """
        Load every supported file directly inside `directory_path`
        (non-recursive) and return the combined list of documents.
        """

        directory = Path(directory_path)

        if not directory.is_dir():
            raise NotADirectoryError(f"{directory} is not a directory.")

        documents: list[Document] = []

        for path in sorted(directory.iterdir()):

            if not path.is_file():
                continue

            if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            documents.extend(self.load(path))

        return documents

    # File LOADER

    def _load_pdf(self, path: Path) -> list[Document]:
        loader = PyMuPDFLoader(str(path))
        return loader.load()

    def _load_docx(self, path: Path) -> list[Document]:
        loader = Docx2txtLoader(str(path))
        return loader.load()

    def _load_text(self, path: Path) -> list[Document]:
        loader = TextLoader(
            str(path),
            encoding="utf-8",
        )
        return loader.load()

    def _load_csv(self, path: Path) -> list[Document]:
        loader = CSVLoader(str(path))
        return loader.load()

    def _load_html(self, path: Path) -> list[Document]:
        loader = UnstructuredHTMLLoader(str(path))
        return loader.load()

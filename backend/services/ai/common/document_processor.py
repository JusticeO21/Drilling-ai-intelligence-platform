import tempfile
import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import UnstructuredExcelLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from common.logging import logger


def process_file_to_documents(file_content: bytes, filename: str) -> List[Document]:
    """
    Process uploaded file content into LangChain documents using proper loaders.

    Args:
        file_content: Raw file bytes
        filename: Original filename

    Returns:
        List of Document objects ready for embedding
    """

    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name

    try:
        documents = []

        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            loader = UnstructuredExcelLoader(temp_file_path, mode="elements")
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} elements from Excel file")

        elif filename.endswith('.csv'):
            loader = CSVLoader(temp_file_path)
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} rows from CSV file")

        else:
            raise ValueError(f"Unsupported file type: {filename}")

        return documents

    finally:
        os.unlink(temp_file_path)


def split_documents(documents: List[Document],
                   chunk_size: int = 1000,
                   chunk_overlap: int = 200) -> List[Document]:
    """
    Split documents into smaller chunks using LangChain text splitter.

    Args:
        documents: List of Document objects
        chunk_size: Maximum size of each chunk
        chunk_overlap: Overlap between chunks

    Returns:
        List of chunked Document objects
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    split_docs = text_splitter.split_documents(documents)
    logger.info(f"Split {len(documents)} documents into {len(split_docs)} chunks")

    return split_docs


def process_file_for_rag(file_content: bytes, filename: str) -> List[str]:
    """
    Complete pipeline: file -> documents -> chunks -> text for RAG.

    Args:
        file_content: Raw file bytes
        filename: Original filename

    Returns:
        List of text chunks ready for embedding
    """

    documents = process_file_to_documents(file_content, filename)
    chunked_docs = split_documents(documents)
    text_chunks = [doc.page_content for doc in chunked_docs]

    logger.info(f"Processed {filename}: {len(documents)} docs → {len(text_chunks)} chunks")
    return text_chunks

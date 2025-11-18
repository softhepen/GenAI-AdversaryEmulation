import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import MarkdownTextSplitter
from langchain_chroma import Chroma

from utils.config import DOCUMENT_FOLDER
from utils.logger import get_logger

logger = get_logger()

# Loads Markdown and text documentation from subfolders
def load_tool_docs(base_folder=DOCUMENT_FOLDER):
    tool_docs = {}
    for tool_name in os.listdir(base_folder):
        tool_path = os.path.join(base_folder, tool_name)
        if os.path.isdir(tool_path):
            doc_content = []
            for file_name in os.listdir(tool_path):
                if file_name.endswith(".md"):
                    file_path = os.path.join(tool_path, file_name)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            doc_content.append(f.read().strip())
                    except Exception as e:
                        logger.warning(f"Failed to read {file_path}: {e}")
            if doc_content:
                tool_docs[tool_name.lower()] = "\n\n".join(doc_content)
    return tool_docs

# Splits a document into Markdown chunks
def split_tool_doc(doc_text, chunk_size=500, chunk_overlap=100):
    splitter = MarkdownTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(doc_text)

# Prepares all chunks with metadata for indexing
def prepare_chunks(tool_docs, chunk_size=500, chunk_overlap=100):
    splitter = MarkdownTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_chunks = []
    for tool_name, doc_text in tool_docs.items():
        chunks = splitter.split_text(doc_text)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "tool_name": tool_name,
                "chunk_id": f"{tool_name}_{i}",
                "content": chunk
            })
    return all_chunks

# Builds a Chroma vector store from embedded chunks
def build_vectorstore(chunks, persist_path="chroma_tool_docs", model_name="sentence-transformers/all-MiniLM-L6-v2"):
    embedder = HuggingFaceEmbeddings(model_name=model_name)
    texts = [c["content"] for c in chunks]
    metadatas = [{"tool_name": c["tool_name"], "chunk_id": c["chunk_id"]} for c in chunks]
    vectorstore = Chroma.from_texts(texts, embedder, metadatas=metadatas, persist_directory=persist_path)
    logger.info(f"Vectorstore saved to {persist_path}")
    return vectorstore

# Loads an existing Chroma vector store from disk
def load_vectorstore(persist_path="chroma_tool_docs", model_name="sentence-transformers/all-MiniLM-L6-v2"):
    embedder = HuggingFaceEmbeddings(model_name=model_name)
    return Chroma(persist_directory=persist_path, embedding_function=embedder)

# Performs semantic retrieval filtered by tool name
def retrieve_tool_chunks(vectorstore, attack_text, tool_name, k=5):
    normalized_tool = tool_name.strip().lower()
    try:
        results = vectorstore.similarity_search(
            attack_text,
            k=k,
            filter={"tool_name": normalized_tool}
        )
        return [r.page_content for r in results]
    except Exception as e:
        logger.warning(f"Retrieval failed for tool '{tool_name}': {e}")
        return []

# Returns retrieved chunks or full documentation as fallback
def get_tool_doc_with_fallback(tool_name, attack_text, vectorstore, tool_doc_dict, k=5):
    chunks = retrieve_tool_chunks(vectorstore, attack_text, tool_name, k=k)
    if chunks:
        return "\n\n".join(chunks)
    return tool_doc_dict.get(tool_name.lower(), "")

# rag/retriever.py
# import hashlib
from rag.embedder import get_vectorstore
from rag.loader import build_documents_from_reasoning

def index_reasoning(reasoning_result, collection_name: str):
    """
    Store reasoning output into a specific collection in the vector DB.
    """
    vectorstore = get_vectorstore(collection_name=collection_name)
    # exist_docs = vectorstore.get()['documents']

    try:
        vectorstore.delete_collection()
    except:
        pass

    # Re-initialize vectorstore to ensure the named collection is created fresh
    vectorstore = get_vectorstore(collection_name=collection_name)

    # if exist_docs:
    #     return

    docs = build_documents_from_reasoning(reasoning_result)

    vectorstore.add_texts(docs)
    vectorstore.persist()


def retrieve_context(query: str, collection_name: str, k: int = 4) -> str:
    """
    Retrieve relevant reasoning context from a specific collection.
    """
    vectorstore = get_vectorstore(collection_name=collection_name)
    try:
        results = vectorstore.similarity_search(query, k=k)
    except Exception:
        return ""

    return "\n".join([doc.page_content for doc in results])

# rag/embedder.py
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
# from chromadb.config import Settings
# import os
# import shutil


# embed = None
# vectorstore_ = None

def create_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# def get_vectorstore(persist_dir="vectorstore/chroma_db"):
def get_vectorstore(persist_dir="vectorstore/chroma_db", collection_name="langchain"):

    # global embed, vectorstore_

    # if embed is None:
    #     embed = HuggingFaceEmbeddings(
    #         model_name="sentence-transformers/all-MiniLM-L6-v2"
    #     )

    embed = create_embeddings()

    vectorstore_ = Chroma(
        collection_name=collection_name,
        persist_directory=persist_dir,
        embedding_function=embed,
    )

    # if vectorstore_ is None:

        # vectorstore_ = Chroma(
        #     persist_directory=persist_dir,
        #     embedding_function=embed,
        #     client_settings=Settings(
        #         anonymized_telemetry=False,
        #         is_persistent=True,
        #     ),
        # )

        # try:
        #     vectorstore_ = Chroma(
        #         persist_directory=persist_dir,
        #         embedding_function=embed,
        #         client_settings=Settings(
        #             anonymized_telemetry=False,
        #             is_persistent=True,
        #         ),
        #     )

        # except Exception:
        #     if os.path.exists(persist_dir):
        #         shutil.rmtree(persist_dir)

        #     vectorstore_ = Chroma(
        #         persist_directory=persist_dir,
        #         embedding_function=embed,
        #         client_settings=Settings(
        #             anonymized_telemetry=False,
        #             is_persistent=True,
        #         ),
        #     )

    return vectorstore_

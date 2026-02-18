# from typing import List

# def build_document_from_reasoning(reasoning_result: dict) -> List[dict]:
#     """
#     Build a list of documents from the reasoning result for RAG.

#     Args:
#         reasoning_result (dict): The reasoning result containing insights and recommendations.

#     Returns:
#         List[dict]: A list of documents formatted for RAG.
#     """
#     documents = []

#     insights = reasoning_result.get("insights", [])
#     recommendations = reasoning_result.get("recommendations", [])

#     insight_text = "Dataset Quality Insights:\n" + "\n".join(f"- {insight}" for insight in insights)
#     recommendation_text = "Recommendations:\n" + "\n".join(f"- {rec}" for rec in recommendations)

#     documents.append({
#         "content": insight_text,
#         "metadata": {"type": "insights"}
#     })

#     documents.append({
#         "content": recommendation_text,
#         "metadata": {"type": "recommendations"}
#     })

#     return documents

# rag/loader.py
from typing import List

# untuk membatasi panjang prompt yang bisa digunakan
max_prompt_length = 1024

def prompt_len(text: str) -> str:
    return text[:max_prompt_length]


def build_documents_from_reasoning(reasoning_result) -> List[str]:
    """
    Convert reasoning output into retrievable text documents
    """
    docs = []

    docs.append(
        prompt_len(
            f"Dataset Risk Level: {reasoning_result.risk_levels}"
        )
    )

    for insight in reasoning_result.insights:
        docs.append(f"INSIGHT: {insight}")

    for rec in reasoning_result.recommendations:
        docs.append(f"RECOMMENDATION: {rec}")

    return docs

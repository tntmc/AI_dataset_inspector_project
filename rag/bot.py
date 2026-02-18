from langchain_google_genai import ChatGoogleGenerativeAI
from rag.prompts import build_dataset_quality_prompt
# from rag.retriever import retrieve_context, index_reasoning
from rag.retriever import retrieve_context

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.05,
    max_output_tokens=4096,
)

# def run_chatbot(reasoning_result, user_questions=None):
def run_chatbot(reasoning_result, collection_name: str, user_questions=None):

    # index_reasoning(reasoning_result)
    retrievered_context = retrieve_context(
        query=user_questions or "dataset overview",
        collection_name=collection_name
    )

    # retrievered_context = retrieve_context(user_questions or "dataset overview")
    base_prompt = build_dataset_quality_prompt(reasoning_result, retrieve_context=retrievered_context)

    if user_questions:
      base_prompt += f"\n\nUser Questions:\n{user_questions}"

    response = llm.invoke(base_prompt)
    return response.content

from rag.prompts import PROMPT, build_dataset_quality_prompt

def run_rag_with_reasoning(
  llm,
  reasoning_output: dict,
  user_questions: str
):

  prompt = build_dataset_quality_prompt(reasoning_output)
  full_prompt = prompt.format(user_questions=user_questions)

  response = llm.invoke(
    [
      {"role": "system", "content": PROMPT},
      {"role": "user", "content": full_prompt}
    ]
  )

  return response.content
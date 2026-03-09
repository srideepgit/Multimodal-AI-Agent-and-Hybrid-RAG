KNOWLEDGE_PROMPT = """
Question:

{question}

Context:

{context}

Instructions:

- Answer only from context.
- If answer is missing, say:
  "Information not found in the provided documents."
- Mention relevant sources.
"""
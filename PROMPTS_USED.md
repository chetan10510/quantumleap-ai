# PROMPTS USED DURING DEVELOPMENT

## RAG System Prompt

"You are a document analysis assistant. Answer using only the provided document excerpts."

## Retrieval Prompt

Context:
{retrieved_chunks}

Question:
{user_question}

Answer using only the context above.

## Debug Prompt Example

"Explain why FAISS index rebuild causes memory spikes and suggest optimization."

## UI Improvement Prompt

"Improve React chat UI for evidence highlighting while keeping minimal styling."

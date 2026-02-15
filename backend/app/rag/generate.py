import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
print("GROQ:", os.getenv("GROQ_API_KEY")[:10])
print("GROQ KEY EXISTS:", bool(os.getenv("GROQ_API_KEY")))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


SYSTEM_PROMPT = """
You are Aggroso AI — a professional knowledge workspace assistant.

Behavior:
- Answer conversationally like a helpful AI assistant.
- Use ONLY the provided document context.
- If answer exists, explain clearly and naturally.
- Summarize key ideas when helpful.
- Do NOT hallucinate information.
- If answer is not present, politely say it is not found in uploaded documents.

Formatting:
Use clean markdown with headings and bullet points.
"""


def generate_answer(question, contexts):

    if not contexts:
        return "No relevant information found in uploaded documents."

    context_text = "\n\n".join(contexts)

    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME", "llama-3.1-8b-instant"),
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""
DOCUMENT CONTEXT:
{context_text}

USER QUESTION:
{question}
"""
            },
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content

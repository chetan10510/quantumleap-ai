from fastapi import HTTPException

# Maximum allowed user message length
MAX_MESSAGE_LENGTH = 1200


def validate_user_message(message: str) -> str:
    """
    Basic LLM safety + validation layer.
    Prevents empty prompts, abuse, and injections.
    """

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    message = message.strip()

    if len(message) == 0:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be blank."
        )

    if len(message) > MAX_MESSAGE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail="Message too long. Please shorten your query."
        )

    # Basic prompt-injection patterns
    blocked_patterns = [
        "ignore previous instructions",
        "act as system",
        "reveal system prompt",
        "show hidden prompt",
        "developer message"
    ]

    lower_msg = message.lower()

    for pattern in blocked_patterns:
        if pattern in lower_msg:
            raise HTTPException(
                status_code=400,
                detail="Unsafe instruction detected."
            )

    return message

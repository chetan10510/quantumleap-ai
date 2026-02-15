from fastapi import Request

def get_user_id(request: Request) -> str:
    """
    Returns workspace id from frontend.
    Each browser gets its own storage.
    """
    return request.headers.get("X-User-ID", "anonymous")

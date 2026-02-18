import uuid
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # ---------- CREATE REQUEST ID ----------
        request_id = str(uuid.uuid4())[:8]

        request.state.request_id = request_id

        start_time = time.time()

        print(f"[REQ {request_id}] {request.method} {request.url.path} START")

        # ---------- PROCESS REQUEST ----------
        response = await call_next(request)

        # ---------- ADD HEADER ----------
        response.headers["X-Request-ID"] = request_id

        duration = round((time.time() - start_time) * 1000, 2)

        print(
            f"[REQ {request_id}] COMPLETED {response.status_code} "
            f"in {duration}ms"
        )

        return response

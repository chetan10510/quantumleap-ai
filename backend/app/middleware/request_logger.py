import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logger import get_logger

logger = get_logger("request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every incoming request and response.

    ✔ Method
    ✔ Path
    ✔ Status code
    ✔ Response time
    ✔ Production-safe (no body logging)
    """

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        try:
            response: Response = await call_next(request)

        except Exception as e:
            logger.exception(
                f"Unhandled error during request {request.method} {request.url.path}"
            )
            raise e

        process_time = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"{request.method} {request.url.path} "
            f"-> {response.status_code} "
            f"({process_time} ms)"
        )

        return response

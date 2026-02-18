import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import get_logger

logger = get_logger("api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every API request with:
    ✔ method
    ✔ path
    ✔ status code
    ✔ response time
    """

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        try:
            response = await call_next(request)

            duration = (time.time() - start_time) * 1000

            logger.info(
                f"{request.method} {request.url.path} | "
                f"{response.status_code} | "
                f"{duration:.2f}ms"
            )

            return response

        except Exception as e:
            duration = (time.time() - start_time) * 1000

            logger.exception(
                f"FAILED {request.method} {request.url.path} | "
                f"{duration:.2f}ms"
            )

            raise e

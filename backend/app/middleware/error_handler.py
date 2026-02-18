from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback


class GlobalErrorHandlerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        try:
            response = await call_next(request)
            return response

        except Exception as e:

            # ---------- LOG FULL ERROR ----------
            print("\n===== GLOBAL ERROR =====")
            print("PATH:", request.url.path)
            print("ERROR:", str(e))
            traceback.print_exc()
            print("========================\n")

            # ---------- SAFE RESPONSE ----------
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": {
                        "type": "SERVER_ERROR",
                        "message": "Something went wrong. Please try again."
                    }
                }
            )

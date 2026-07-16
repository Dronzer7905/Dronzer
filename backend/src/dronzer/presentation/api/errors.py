import structlog
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = structlog.get_logger("dronzer.api.errors")


def register_error_handlers(app: FastAPI) -> None:
    """
    Registers global exception handlers mapping internal Python errors to OpenAI-compatible JSON responses.
    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning("Request validation failed", errors=exc.errors())
        # Format explicitly like OpenAI
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "message": "Invalid request parameters",
                    "type": "invalid_request_error",
                    "param": exc.errors()[0].get("loc", [""])[-1] if exc.errors() else None,
                    "code": None,
                    "details": exc.errors(),
                }
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # We catch everything else here
        logger.error("Internal Server Error", error=str(exc), exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "message": "The server had an error processing your request.",
                    "type": "server_error",
                    "param": None,
                    "code": "internal_error",
                }
            },
        )

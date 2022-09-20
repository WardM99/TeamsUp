"""Handlers for the exceptions"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound
from starlette import status

def install_handlers(app: FastAPI): # pragma: no cover
    """Intall all custom exception handlers"""

    @app.exception_handler(NoResultFound)
    def no_result_found(_request: Request, _exception: NoResultFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Not Found"}
        )

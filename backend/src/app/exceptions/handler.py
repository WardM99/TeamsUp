"""Handlers for the exceptions"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound
from jose import ExpiredSignatureError, JWTError
from starlette import status

def install_handlers(app: FastAPI): # pragma: no cover
    """Intall all custom exception handlers"""

    @app.exception_handler(NoResultFound)
    def no_result_found(_request: Request, _exception: NoResultFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Not Found"}
        )


    @app.exception_handler(ExpiredSignatureError)
    def expired_signature_error(_request: Request, _exception: ExpiredSignatureError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Credentials are expired"}
        )


    @app.exception_handler(JWTError)
    def jwt_error(_request: Request, _exception: JWTError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "You are not authorized for this"}
        )

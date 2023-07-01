"""Handlers for the exceptions"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound, IntegrityError
from jose import ExpiredSignatureError, JWTError
from starlette import status

from src.app.exceptions.wrongplayer import WrongPlayerException
from src.app.exceptions.nomorecards import NoMoreCardsException

def install_handlers(app: FastAPI): # pragma: no cover
    """Intall all custom exception handlers"""

    @app.exception_handler(NoResultFound)
    def no_result_found(_request: Request, _exception: NoResultFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Not Found"}
        )


    @app.exception_handler(IntegrityError)
    def integrity_error(_request: Request, _exception: IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Bad Request"}
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

    @app.exception_handler(WrongPlayerException)
    def wrong_player_exception(_request: Request, _exception: WrongPlayerException):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={"message": "It's not your turn"}
        )

    @app.exception_handler(NoMoreCardsException)
    def no_more_cards_exception(_request: Request, _exception: NoMoreCardsException):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={"message": "There are no more cards"}
        )
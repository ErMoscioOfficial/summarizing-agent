from typing import Any, Callable

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from pydantic import ValidationError

from sqlalchemy.exc import SQLAlchemyError

class AppException(Exception):
    pass

class InvalidToken(AppException):
    """Token provided is not valid"""
    pass

class AccessTokenRequired(AppException):
    """No access token provided from user"""
    pass


class InsufficientUserPermission(AppException):
    pass

class UserAlreadyExists(AppException):
    pass

class UserNotExists(AppException):
    pass

class UserWrongPassword(AppException):
    pass

class NoDataFound(AppException):
    pass

def create_exception_handler(
        status_code: int, 
        initial_detail: Any
    ) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: AppException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code = status.HTTP_403_FORBIDDEN,
            initial_detail= {
                'message' : 'Provided token is not valid',
                'error_code':'invalid_token'
            }
        )
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code = status.HTTP_400_BAD_REQUEST,
            initial_detail= {
                'message' : 'Access token not provided',
                'error_code':'missing_token'
            }
        )
    )

    app.add_exception_handler(
        InsufficientUserPermission,
        create_exception_handler(
            status_code = status.HTTP_401_UNAUTHORIZED,
            initial_detail= {
                'message' : 'The user does not have adequate permission',
                'error_code':'invalid_permission'
            }
        )
    )

    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code = status.HTTP_400_BAD_REQUEST,
            initial_detail= {
                'message' : 'A user with the same email already exists',
                'error_code':'account_exists'
            }
        )
    )

    app.add_exception_handler(
        UserNotExists,
        create_exception_handler(
            status_code = status.HTTP_400_BAD_REQUEST,
            initial_detail= {
                'message' : 'The account does not exist',
                'error_code':'account_missing'
            }
        )
    )

    app.add_exception_handler(
        UserWrongPassword,
        create_exception_handler(
            status_code = status.HTTP_400_BAD_REQUEST,
            initial_detail= {
                'message' : 'The provided password is wrong, try again',
                'error_code':'wrong_password'
            }
        )
    )

    app.add_exception_handler(
        NoDataFound,
        create_exception_handler(
            status_code = status.HTTP_404_NOT_FOUND,
            initial_detail= {
                'message' : 'No data present to offload',
                'error_code':'no_data_found'
            }
        )
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                'message':'Fields provided are of the wrong type',
                "error_code": "validation_error",
                "errors": [
                    {"field": err["loc"][-1], "message": err["msg"]} for err in exc.errors()
                ],
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                'message':'Fields provided are of the wrong type',
                "error_code": "validation_error",
                "errors": [
                    {"field": err["loc"][-1], "message": err["msg"]} for err in exc.errors()
                ],
            },
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        errors = [{"field": e["loc"], "message": e["msg"]} for e in exc.errors()]
        return JSONResponse(
            status_code=400,  # 400 Bad Request for internal validation errors
            content={"detail": "Data validation error", "error_code": "validation_error", "errors": errors},
        )

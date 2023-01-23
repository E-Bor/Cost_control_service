from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, Cookie, Response
from passlib.hash import bcrypt
from jose import jwt, JWTError
from pydantic import ValidationError
from starlette import status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from src.database.data_schemes.work_with_db import engine, get_session
from src.settings import jwt_secret, jwt_algoritm, jwt_expiration
from src.apps.cost_controll_app.schemas.schemas import User, Token, UserCreate  #pydantic schema
from src.database.data_schemes.work_with_db import session
from src.database.data_schemes.data_schemas import Users    #orm schema
from fastapi.security import OAuth2PasswordBearer


class AuthService:

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={
                "Authenticate": "Bearer"
            }
        )
        try:
            payload = jwt.decode(token, jwt_secret, algorithms=[jwt_algoritm])
        except JWTError:
            raise exception
        user_data = payload.get("user")
        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception

        return user

    @classmethod
    def create_token(cls, user: Users) -> Token:
        print(user, "user-token-created")
        user_data = User.from_orm(user)
        payload = {
            "iat": datetime.utcnow(),
            "nbf": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=jwt_expiration),
            "sub": str(user_data.user_id),
            "user": user_data.dict()
        }
        token = jwt.encode(payload, jwt_secret, algorithm=jwt_algoritm)
        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: UserCreate, response: Response) -> Token:
        user = Users(
            user_email=user_data.user_email,
            user_name=user_data.user_name,
            user_hashed_pass=self.hash_password(user_data.password)
        )
        self.session.add(user)
        self.session.commit()
        token = self.create_token(user)
        response.set_cookie(key="cookie_token", value=token.access_token)
        return token

    def authenticate_user(self, username: str, password: str,  response: Response) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "Authenticate": "Bearer"
            }
        )
        user = (self.session.query(Users).filter(Users.user_name == username).first())
        if not user:
            raise exception

        if not self.verify_password(password, user.user_hashed_pass):
            raise exception
        token = self.create_token(user)
        response.set_cookie(key="cookie_token", value=token.access_token)
        return token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin", auto_error=False)


def chose_cookie_or_token(cookie_token=Cookie(default=None), token=Depends(oauth2_scheme)):

    if cookie_token:
        return cookie_token
    elif token:
        return token
    else:
        raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )


def get_current_user(token: str = Depends(chose_cookie_or_token)) -> User:
    return AuthService.validate_token(token)



# def get_current_user(token: str = Depends(oauth2_scheme), cookie_token=Cookie(default=None)) -> User:
#     # print(cookie_token, flush=True)
#     # print("!!!!!!!", flush=True)
#     print(cookie_token)
#     if cookie_token:
#         A = AuthService.validate_token(cookie_token)
#         print(A, "bool")
#         return A
#
#     return AuthService.validate_token(token)


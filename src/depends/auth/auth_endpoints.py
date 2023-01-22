from fastapi import APIRouter, Depends, Response, Cookie

from src.apps.cost_controll_app.schemas.schemas import Token, UserCreate, User
from src.depends.auth.auth_service import get_current_user, AuthService
from fastapi.security import OAuth2PasswordRequestForm

auth = APIRouter(prefix="/auth")


@auth.post('/singup', response_model=Token)
def sign_up(response: Response, user_data: UserCreate, service: AuthService = Depends()):
    print(user_data)
    return service.register_new_user(user_data, response=response)


@auth.post('/signin', response_model=Token)
def sign_in(response: Response,
            form_data: OAuth2PasswordRequestForm = Depends(),
            service: AuthService = Depends(),
            ):

    return service.authenticate_user(form_data.username, form_data.password, response=response)

@auth.get('/user', response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user


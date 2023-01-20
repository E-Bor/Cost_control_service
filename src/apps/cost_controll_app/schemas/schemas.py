from datetime import date
from pydantic import BaseModel
from typing import List

class ExpensesModel(BaseModel):
    cost: int
    disc: str
    date: date
    user_id: int


class ExpensesReturnModel(BaseModel):
    status: str = "Ok"


class GetExpenses(BaseModel):
    user_id: int
    pagination_start: int = 0
    pagination_stop: int = 10
    date_start: date
    date_stop: date



class ReturnListExpensisModel(BaseModel):
    summary_cost: int | None
    date: date | List[date]


class BaseUser(BaseModel):
    user_name: str
    user_email: str

class UserCreate(BaseUser):
    password: str

class User(BaseUser):
    user_id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


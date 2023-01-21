from datetime import date
from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from fastapi import Query


class CategoryModel(str, Enum):
    food = "food"
    other = "other"


class ExpensesModel(BaseModel):
    cost: int
    disc: str
    category: CategoryModel
    date: date

class ExpensDBModel(ExpensesModel):
    user_id: int


class ExpensesReturnModel(BaseModel):
    status: str = "Ok"


class GetExpenses(ExpensesModel):
    operation_id: str


class GetExpensesList(BaseModel):
    exp_list: List[GetExpenses]




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


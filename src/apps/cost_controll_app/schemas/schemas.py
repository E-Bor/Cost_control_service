from datetime import date
from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from fastapi import Query


class CategoryModel(str, Enum):
    food = "food"
    other = "other"


# schemas for expensis
class ExpensesModel(BaseModel):
    cost: int
    disc: str
    category: CategoryModel
    date: date

class ExpensDBModel(ExpensesModel):
    user_id: int


class ExpensesReturnModel(BaseModel):
    status: str = "Ok"


class GetExpensesModel(ExpensesModel):
    operation_id: str


class GetExpensesListModel(BaseModel):
    exp_list: List[GetExpensesModel]


# schemas for earnings
class EarningModel(BaseModel):
    earning_value: int
    date: date


class EarningDBModel(EarningModel):
    user_id: int


class GetEarningsModel(EarningModel):
    earning_id: int


class GetEarningsListModel(BaseModel):
    exp_list: List[GetEarningsModel]



# security schemas
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


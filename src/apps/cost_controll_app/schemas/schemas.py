from datetime import date
from pydantic import BaseModel, Field
from typing import List
from enum import Enum

# Pydantic`s schemas set

# Scheme for listing possible categories
class CategoryModel(str, Enum):
    food = "food"
    other = "other"


# Schemas for expensis
class ExpensesModel(BaseModel):
    cost: int
    disc: str
    category: CategoryModel
    date: date


# Scheme for recording expenses in the database
class ExpensDBModel(ExpensesModel):
    user_id: int


# Return schema for expenses in get query
class ExpensesReturnModel(BaseModel):
    status: str = "Ok"


# Scheme for recording expenses in the database with operation id
class GetExpensesModel(ExpensesModel):
    operation_id: str


# schema for get expenses list
class GetExpensesListModel(BaseModel):
    exp_list: List[GetExpensesModel]


# Eq. schemas for earnings
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


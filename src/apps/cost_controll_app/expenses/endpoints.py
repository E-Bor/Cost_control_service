from fastapi import APIRouter

from src import database
from src.apps.cost_controll_app.schemas.schemas import ExpensesModel, ExpensesReturnModel, GetExpenses
from src.database.data_schemes.work_with_db import engine, session
from src.database.data_schemes.data_schemas import Expenses
from datetime import date, datetime


cost_control_router = APIRouter()


@cost_control_router.post("/expenses", response_model=ExpensesReturnModel)
async def add_expenses(expenses: ExpensesModel):
    exp = Expenses(**dict(expenses))
    session.add(exp)
    session.commit()
    return {"status" : "Record added to database"}

@cost_control_router.get("/expenses")
async def get_expenses(got_expenses:  GetExpenses):
    q = session.query(Expenses).where(
        Expenses.user_id == got_expenses.user_id and
        got_expenses.date_start < Expenses.date < got_expenses.date_stop
    )[got_expenses.pagination_start:got_expenses.pagination_stop]
    for i in q:
        print(q)



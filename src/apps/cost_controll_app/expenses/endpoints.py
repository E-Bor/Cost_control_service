from datetime import datetime, date, timedelta

from fastapi import APIRouter, Depends, Query
from src.depends.auth.auth_service import get_current_user
from datetime import date
from src.apps.cost_controll_app.schemas.schemas import ExpensesModel, ExpensesReturnModel, GetExpensesModel, User, \
    ExpensDBModel, GetExpensesListModel, GetExpensesModel
from src.database.data_schemes.work_with_db import engine, get_session
from src.database.data_schemes.data_schemas import Expenses
from sqlalchemy.orm import Session


cost_control_router = APIRouter()


@cost_control_router.post("/expenses", response_model=ExpensesReturnModel)
async def add_expenses(expenses: ExpensesModel, current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session),
                       ):
    expens_to_db = ExpensDBModel(**dict(expenses), user_id=current_user.user_id)
    exp = Expenses(**dict(expens_to_db))
    session.add(exp)
    session.commit()
    return {"status" : "Record added to database"}


@cost_control_router.get("/expenses", response_model=GetExpensesListModel)
async def get_expenses(pagination_start: int = Query(ge=0, default=0),
                       pagination_step: int = Query(ge=10, lt=100, default=10), current_user = Depends(get_current_user),
                       time_delta_days: int = Query(gt=0, default=30), session: Session = Depends(get_session)):
    q = session.query(Expenses.cost, Expenses.date, Expenses.disc, Expenses.category, Expenses.operation_id).where(
        Expenses.user_id == current_user.user_id and datetime.today() - timedelta(days=time_delta_days)
        <= datetime.date(Expenses.date) <= datetime.today()
    ).all()
    session.close()
    expenses = list()
    for i in q:
        expenses.append({"cost": i[0], "date": i[1], "disc": i[2], "category": i[3], "operation_id": i[4]})
    return {"exp_list": expenses}


@cost_control_router.put("/expenses", response_model=GetExpensesModel)
async def change_expense(
        expense: GetExpensesModel,
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session)
):

    upd_expense = ExpensDBModel(**dict(expense), user_id=current_user.user_id)
    q = session.query(Expenses).where(Expenses.user_id == current_user.user_id)\
        .where(Expenses.operation_id == expense.operation_id).update(dict(upd_expense))
    session.commit()
    session.close()
    return expense


@cost_control_router.delete("/expenses", response_model=ExpensesReturnModel)
async def delete_expense(
        operation_id: str,
        current_user = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    q = session.query(Expenses).where(Expenses.user_id == current_user.user_id)\
        .where(Expenses.operation_id == operation_id).delete()
    session.commit()
    session.close()
    return {"status" : "Record deleted from database"}






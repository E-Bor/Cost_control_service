from fastapi import APIRouter, Depends, Query
from datetime import datetime, date, timedelta

from src.database.data_schemes.data_schemas import Earnings
from src.depends.auth.auth_service import get_current_user
from src.apps.cost_controll_app.schemas.schemas import EarningModel, EarningDBModel, GetEarningsListModel, \
    GetEarningsModel, User
from src.database.data_schemes.work_with_db import get_session
# from src.database.data_schemes.data_schemas import Expenses
from sqlalchemy.orm import Session


earnings_control_router = APIRouter()


@earnings_control_router.get('/earnings', response_model=GetEarningsListModel)
async def get_earnings(pagination_start: int = Query(ge=0, default=0),
                       pagination_step: int = Query(ge=10, lt=100, default=10),
                       current_user: User = Depends(get_current_user),
                       time_delta_days: int = Query(gt=0, default=30), session: Session = Depends(get_session)):
    q = session.query(Earnings.earning_value, Earnings.date, Earnings.earning_id).where(
        Earnings.user_id == current_user.user_id and datetime.today() - timedelta(days=time_delta_days)
        <= datetime.date(Earnings.date) <= datetime.today()
    )[pagination_start:pagination_start+pagination_step]
    session.close()
    expenses = list()
    for i in q:
        expenses.append({"earning_value": i[0], "date": i[1], "earning_id": i[2]})

    return {"exp_list": expenses}


@earnings_control_router.post("/earnings")
async def add_earnings(earning: EarningModel,
                       current_user: User =Depends(get_current_user),
                       session: Session = Depends(get_session)):
    earning = EarningDBModel(**dict(earning), user_id=current_user.user_id)
    earning_to_db = Earnings(**dict(earning))
    session.add(earning_to_db)
    session.commit()
    session.close()
    return {"status": "Record added to database"}


@earnings_control_router.put('/earnings')
async def edit_earnings(
        earning: GetEarningsModel,
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session)
):

    upd_earning = EarningDBModel(**dict(earning), user_id=current_user.user_id)
    q = session.query(Earnings).where(Earnings.user_id == current_user.user_id)\
        .where(Earnings.earning_id == earning.earning_id).update(dict(upd_earning))
    session.commit()
    session.close()
    return earning


@earnings_control_router.delete("/earnings")
async def delete_earning(
        earning_id: str,
        current_user=Depends(get_current_user),
        session: Session = Depends(get_session)
):
    q = session.query(Earnings).where(Earnings.user_id == current_user.user_id)\
        .where(Earnings.earning_id == earning_id).delete()
    session.commit()
    session.close()
    return {"status" : "Record deleted from database"}


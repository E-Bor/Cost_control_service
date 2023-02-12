from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import datetime, timedelta

from src.database.data_schemes.data_schemas import Earnings
from src.depends.auth.auth_service import get_current_user
from src.apps.cost_controll_app.schemas.schemas import EarningModel, EarningDBModel, GetEarningsListModel, \
    GetEarningsModel, User
from src.database.data_schemes.work_with_db import get_session

from sqlalchemy.orm import Session

# router for user operations in category earnings
earnings_control_router = APIRouter()


# getting info about earnings in time interval
@earnings_control_router.get('/earnings', response_model=GetEarningsListModel, tags=["Earnings"])
async def get_earnings(pagination_start: int = Query(ge=0, default=0),
                       pagination_step: int = Query(ge=10, lt=100, default=10),
                       current_user: User = Depends(get_current_user),
                       time_delta_days: int = Query(gt=0, default=30), session: Session = Depends(get_session)):
    q = session.query(Earnings.earning_value, Earnings.date, Earnings.earning_id).where(
        Earnings.user_id == current_user.user_id and datetime.today() - timedelta(days=time_delta_days)
        <= datetime.date(Earnings.date) <= datetime.today()
    )[pagination_start:pagination_start+pagination_step]
    session.close()
    earnings = list()
    for i in q:
        earnings.append({"earning_value": i[0], "date": i[1], "earning_id": i[2]})

    return {"exp_list": earnings}


# add earning with info to database
@earnings_control_router.post("/earnings", tags=["Earnings"])
async def add_earnings(earning: EarningModel,
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    earning = EarningDBModel(**dict(earning), user_id=current_user.user_id)
    earning_to_db = Earnings(**dict(earning))
    session.add(earning_to_db)
    session.commit()
    session.close()
    return {"status": "Record added to database"}


# edit earning note
@earnings_control_router.put('/earnings', tags=["Earnings"])
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
    if not q:
        raise HTTPException(status_code=404, detail="Earning note not found")
    return earning


# deleting earning note from database
@earnings_control_router.delete("/earnings", tags=["Earnings"])
async def delete_earning(
        earning_id: str,
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    q = session.query(Earnings).where(Earnings.user_id == current_user.user_id)\
        .where(Earnings.earning_id == earning_id).delete()
    session.commit()
    session.close()
    return {"status": "Record deleted from database"}

from fastapi import APIRouter, Depends, Query
from datetime import datetime, date, timedelta
from src.depends.auth.auth_service import get_current_user
# from src.apps.cost_controll_app.schemas.schemas import
from src.database.data_schemes.work_with_db import get_session
# from src.database.data_schemes.data_schemas import Expenses
from sqlalchemy.orm import Session


earnings_control_router = APIRouter()


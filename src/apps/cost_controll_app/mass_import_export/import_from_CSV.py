from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .services import MassOperations
from src.apps.cost_controll_app.schemas.schemas import User
from src.database.data_schemes.work_with_db import get_session
from src.depends.auth.auth_service import get_current_user


mass_import_router = APIRouter()


@mass_import_router.get("/massimport", tags=["Import CSV"])
def load_info_from_zip(current_user: User = Depends(get_current_user),
                       srvs: MassOperations = Depends(MassOperations)):

    pass
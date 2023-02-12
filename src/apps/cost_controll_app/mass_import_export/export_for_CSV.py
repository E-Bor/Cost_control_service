from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .services import MassOperations
from src.apps.cost_controll_app.schemas.schemas import User
from src.database.data_schemes.work_with_db import get_session
from src.depends.auth.auth_service import get_current_user
from fastapi.responses import FileResponse

mass_export_router = APIRouter()


@mass_export_router.get("/massexport", tags=["Export CSV"])
def get_csv_with_data(current_user: User = Depends(get_current_user),
                      srvs: MassOperations = Depends(MassOperations)):

    read_data = srvs.read_database(current_user.user_id)
    paths = srvs.create_zip_with_csv(read_data, current_user.user_id)
    return FileResponse(paths.get("path"), filename=paths.get("filename"), media_type="zip")

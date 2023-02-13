import shutil

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from .services import MassOperations
from src.apps.cost_controll_app.schemas.schemas import User
from src.database.data_schemes.work_with_db import get_session
from src.depends.auth.auth_service import get_current_user
import os


mass_import_router = APIRouter()


@mass_import_router.post("/massimport", tags=["Import CSV"])
def load_info_from_zip(file: UploadFile,
                       current_user: User = Depends(get_current_user),
                       srvs: MassOperations = Depends(MassOperations)
                       ):
    with open(os.path.dirname(__file__) + "/uploaded_files/" + file.filename, "wb") as new_file:
        shutil.copyfileobj(file.file, new_file)
    # csv_list = srvs.unpack_zip(file.filename)
    srvs.extract_data_to_db(file.filename, current_user)
    file.file.close()

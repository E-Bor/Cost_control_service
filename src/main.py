from fastapi import FastAPI
from .apps.cost_controll_app.expenses.endpoints import cost_control_router
from .depends.auth.auth_endpoints import auth

app = FastAPI()
app.include_router(cost_control_router)
app.include_router(auth)
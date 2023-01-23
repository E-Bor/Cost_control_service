from fastapi import FastAPI
from .apps.cost_controll_app.expenses.expenses import cost_control_router
from .apps.cost_controll_app.earnings.earnings import earnings_control_router
from .depends.auth.auth_endpoints import auth

app = FastAPI()
app.include_router(cost_control_router)
app.include_router(earnings_control_router)
app.include_router(auth)

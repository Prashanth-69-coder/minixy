from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from src.controllers.auth_controller import router as auth_router

app = FastAPI()

app.include_router(auth_router)

templates = Jinja2Templates(directory="templates")
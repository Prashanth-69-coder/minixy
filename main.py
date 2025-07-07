from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.controllers.auth_controller import router as auth_router
from src.controllers.profile_controller import router as profile_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(profile_router)
templates = Jinja2Templates(directory="templates")
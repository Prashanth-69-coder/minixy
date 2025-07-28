from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.controllers.auth_controller import router as auth_router
from src.controllers.profile_controller import router as profile_router
from src.controllers.alumini_controller import router as alumini_router
from src.controllers.student_controller import router as student_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(alumini_router)
app.include_router(student_router)
templates = Jinja2Templates(directory="templates")

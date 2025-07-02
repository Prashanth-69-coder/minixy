from fastapi import FastAPI,APIRouter,Form,Request
from fastapi.responses import HTMLResponse
from supabase import create_client
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get('/login')
def get_login(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})

@router.get('/signup')
def get_signup(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})

@router.post('/api/login')
def make_login(request:Request,email:str =Form(...) ,password:str = Form(...)):

    print(email)
    print(password)
    return {"message":"recieved"}
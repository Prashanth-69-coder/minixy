from typing import Self
from fastapi import FastAPI,APIRouter,Form,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi import status
from fastapi.templating import Jinja2Templates
from ..services.auth_services import AuthService
from ..repositories.auth_repository import AuthRepository
from ..services.profile_services import ProfileService



router = APIRouter()

templates = Jinja2Templates(directory="templates")

def logged_user(request:Request):
    session_token = request.cookies.get('user_session')
    user_service = AuthService()
    user = user_service.current_user(session_token)
    if user:
        return user
    else:
        return None



@router.get('/')
def get_home(request:Request):
    user = logged_user(request)
    if user:
        return RedirectResponse(
            url="/api/profile",
            status_code=status.HTTP_303_SEE_OTHER
        )
    return templates.TemplateResponse("homepage.html",{"request":request})

@router.get('/login')
def get_login(request: Request):
    user = logged_user(request)
    if user:
        return RedirectResponse(
            url="/api/profile",
            status_code=status.HTTP_303_SEE_OTHER
            
        )
    return templates.TemplateResponse("login.html",{"request":request})

@router.get('/signup')
def get_signup(request:Request):
    user = logged_user(request)
    if user:
        return RedirectResponse(
            url="/api/profile",
            status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("signup.html",{"request":request})

@router.post('/api/signup')
def make_signup(request:Request,email:str =Form(...),password:str = Form(...)):
    try:
        user_service = AuthService()
        res = user_service.signup_user(email,password)
        if res:
            return templates.TemplateResponse("registration.html",{"request":request})
        else:
            return templates.TemplateResponse("login.html",{"request":request})
    except Exception as e:
        return templates.TemplateResponse("login.html",{"request":request})


@router.post('/api/create_profile')
def create_profile(request: Request,
                  user_name: str = Form(...),
                  first_name: str = Form(...),
                  last_name: str = Form(...),
                  role: str = Form(...),
                  bio: str = Form(...),
                  skills: str = Form(...),
                  experience: str = Form(...),
                  profile_picture: str = Form(None)):
    try:
        user_id = request.session.get('user_id')
        skills_list = [s.strip() for s in skills.split(',') if s.strip()]
        user_service = ProfileService()
        res = user_service.create_user_profile(user_id, user_name, first_name, last_name, role, bio, skills_list, experience, profile_picture)
        if res:
            return templates.TemplateResponse("signup.html", {"request": request, "success": True})
        else:
            return templates.TemplateResponse("registration.html", {"request": request})
    except Exception as e:
        return templates.TemplateResponse("login.html", {"request": request})

@router.get('/api/profile')
def get_profile(request:Request):
    try:
        user_id = request.session.get('user_id')
        user_service = ProfileService()
        res = user_service.get_user_profile(user_id)
        if res:
            return templates.TemplateResponse("profile.html",{"request":request,"user":res})
        else:
            return templates.TemplateResponse("login.html",{"request":request})
    except Exception as e:
        return templates.TemplateResponse("login.html",{"request":request})

            
@router.post('/api/login')
def make_login(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        user_service = AuthService()
        res = user_service.login_user(email, password)

        if res and res.session and res.session.access_token:
            response = RedirectResponse(
                url="/api/profile",
                status_code=status.HTTP_303_SEE_OTHER
            )
            response.set_cookie(
                key="user_session",
                value=res.session.access_token,
                httponly=True,
                secure=True,  # only use secure=True if you're serving over HTTPS
                samesite='lax',
                max_age=3600
            )
            return response
        else:
            # optionally you can add error message to context
            return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    except Exception as e:
        # logging the error would be helpful in production
        return templates.TemplateResponse("login.html", {"request": request, "error": "Something went wrong. Try again."})







from typing import Self
from fastapi import FastAPI,APIRouter,Form,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi import status
from fastapi.templating import Jinja2Templates
from ..services.auth_services import AuthService
from ..repositories.auth_repository import AuthRepository
from ..services.profile_services import ProfileService
import pprint

templates = Jinja2Templates(directory="templates")
router = APIRouter()

def get_loggedin_user(request: Request):
    session_token = request.cookies.get('user_session')
    auth_service = AuthService()
    user = auth_service.current_user(session_token)
    if user:
        return user
    else:
        return None


@router.get('/registration')
def registration_page(request: Request):
    user = get_loggedin_user(request)
    if user:
        return templates.TemplateResponse('registration.html', {"request": request})
    else:
        return RedirectResponse('/login')

# Removed the /dashboard route to avoid conflict with auth_controller.py

@router.post('/api/create/profile')
def update_profile(request: Request, first_name: str = Form(...), last_name: str = Form(...), role: str = Form(...)):
    profile_service = ProfileService()
    user = get_loggedin_user(request)
    if user:
        profile = {
            "id": user.user.id,
            "first_name": first_name,
            "last_name": last_name,
            "role": role
        }
        result = profile_service.create_user_profile(profile)
        if result:
            # After profile creation, redirect to the correct dashboard based on role
            if role == 'admin':
                return RedirectResponse(url="/admindashboard", status_code=status.HTTP_303_SEE_OTHER)
            elif role == 'student':
                return RedirectResponse(url="/studentdashboard", status_code=status.HTTP_303_SEE_OTHER)
            elif role == 'alumni':
                return RedirectResponse(url="/alumnidashboard", status_code=status.HTTP_303_SEE_OTHER)
            else:
                return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse(url="/registration", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse('/login')
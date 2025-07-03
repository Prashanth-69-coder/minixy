from fastapi import FastAPI,APIRouter,Form,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from httpx import request
from supabase import create_client
from fastapi.templating import Jinja2Templates
import supabase
from ..services.profile_services import ProfileService
from ..services.auth_services import AuthService

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.post('/api/create_profile')
def create_profile(request: Request,
                  email: str = Form(...),
                  user_name: str = Form(...),
                  first_name: str = Form(...),
                  last_name: str = Form(...),
                  role: str = Form(...),
                  bio: str = Form(...),
                  skills: str = Form(...),
                  experience: str = Form(...),
                  profile_picture: str = Form(None)):
    try:
        print('Create profile attempt:')
        print('email:', email)
        print('user_name:', user_name)
        print('first_name:', first_name)
        print('last_name:', last_name)
        print('role:', role)
        print('bio:', bio)
        print('skills:', skills)
        print('experience:', experience)
        print('profile_picture:', profile_picture)
        # Lookup user_id by email
        auth_service = AuthService()
        user_id = auth_service.get_user_by_email(email)
        print('Resolved user_id:', user_id)
        skills_list = [s.strip() for s in skills.split(',') if s.strip()]
        user_service = ProfileService()
        res = user_service.create_user_profile(user_id, user_name, first_name, last_name, role, bio, skills_list, experience, profile_picture)
        print('Insert result:', res)
        if res:
            print('Profile creation successful, redirecting to /api/profile')
            return RedirectResponse(url="/api/profile", status_code=303)
        else:
            print('Profile creation failed, rendering registration.html')
            return templates.TemplateResponse("registration.html", {"request": request})
    except Exception as e:
        print('Profile creation exception:', e)
        return templates.TemplateResponse("login.html", {"request": request })

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
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
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER
        )
    return templates.TemplateResponse("homepage.html",{"request":request})

@router.get('/login')
def get_login(request: Request):
    user = logged_user(request)
    print('user from logged_user:', user)
    if user:
        return RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER
            
        )
    return templates.TemplateResponse("login.html",{"request":request})

@router.get('/signup')
def get_signup(request:Request):
    user = logged_user(request)
    if user:
        return RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("signup.html",{"request":request})

@router.post('/api/signup')
def make_signup(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        print('Signup attempt: email=', email, 'password=', password)
        user_service = AuthService()
        res = user_service.signup_user(email, password)
        print('Signup result:', res)
        if res:
            # Auto-login after signup
            login_res = user_service.login_user(email, password)
            print('Auto-login result:', login_res)
            # Safely extract access_token
            session = getattr(login_res, 'session', None) or (login_res.get('session') if isinstance(login_res, dict) else None)
            access_token = getattr(session, 'access_token', None) if session and not isinstance(session, dict) else (session.get('access_token') if session else None)
            if access_token:
                response = RedirectResponse(url="/registration", status_code=303)
                response.set_cookie(
                    key="user_session",
                    value=access_token,
                    httponly=True,
                    secure=True,  # only use secure=True if you're serving over HTTPS
                    samesite='lax',
                    max_age=3600
                )
                print('Signup and auto-login successful, redirecting to /registration')
                return response
            else:
                print('Auto-login failed after signup: No access_token')
                return templates.TemplateResponse("login.html", {"request": request, "error": "Auto-login failed after signup."})
        else:
            print('Signup failed: No result returned')
            return templates.TemplateResponse("login.html", {"request": request, "error": "Signup failed."})
    except Exception as e:
        print('Signup exception:', e)
        return templates.TemplateResponse("login.html", {"request": request, "error": "Signup failed."})


            
@router.post('/api/login')
def make_login(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        print('Login attempt: email=', email, 'password=', password)
        user_service = AuthService()
        res = user_service.login_user(email, password)
        print('Login result:', res)
        if res and res.session and res.session.access_token:
            response = RedirectResponse(
                url="/dashboard",
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
            print('Login successful, redirecting to /dashboard')
            return response
        else:
            print('Login failed: Invalid credentials')
            return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    except Exception as e:
        print('Login exception:', e)
        return templates.TemplateResponse("login.html", {"request": request, "error": "Something went wrong. Try again."})


@router.get('/dashboard')
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get('/details')
def get_details(request: Request):
    return templates.TemplateResponse("details.html", {"request": request})

@router.post('/api/details')
def post_details(request: Request, first_name: str = Form(...), last_name: str = Form(...)):
    # Here you would save the details to the user profile in the database
    # For now, just redirect to dashboard
    print(f"Received details: {first_name} {last_name}")
    return RedirectResponse(url="/dashboard", status_code=303)







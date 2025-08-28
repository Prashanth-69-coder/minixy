from fastapi import APIRouter, Request, Form, status, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from ..services.auth_services import AuthService
from ..services.profile_services import ProfileService
from ..auth_utils import get_current_user, protected_route, create_session_cookies, clear_session_cookies
from ..validators import AuthValidator, SecurityHelper
from typing import Optional



router = APIRouter()

templates = Jinja2Templates(directory="templates")



@router.get('/')
async def get_home(request: Request):
    user = await get_current_user(request)
    if user:
        return RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER
        )
    return templates.TemplateResponse("homepage.html", {"request": request})

@router.get('/login')
async def get_login(
    request: Request, 
    registration_complete: str = "",
    email: str = "",
    role: str = ""
):
    user = await get_current_user(request)
    if user:
        return RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    success_message = None
    
    if registration_complete == "true" and email:
        if role:
            dashboard_names = {
                'admin': 'Admin Dashboard',
                'student': 'Student Dashboard', 
                'alumni': 'Alumni Dashboard'
            }
            dashboard_name = dashboard_names.get(role, 'Dashboard')
            success_message = f"Registration completed successfully! Please sign in to access your {dashboard_name}."
        else:
            success_message = f"Registration completed successfully! Please sign in with your email ({email}) to continue."
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "success": success_message,
        "prefill_email": email if registration_complete == "true" else ""
    })

@router.get('/signup')
async def get_signup(request:Request):
    user = await get_current_user(request)
    if user:
        return RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("signup.html",{"request":request})

@router.post('/api/signup')
async def make_signup(request: Request, response: Response, email: str = Form(...), password: str = Form(...)):
    try:
        email = AuthValidator.sanitize_input(email)
        password = AuthValidator.sanitize_input(password)
        
        email_valid, email_error = AuthValidator.validate_email(email)
        if not email_valid:
            return templates.TemplateResponse("signup.html", {
                "request": request, 
                "error": email_error
            })
        
        password_valid, password_errors = AuthValidator.validate_password(password)
        if not password_valid:
            error_message = "Password requirements not met: " + "; ".join(password_errors)
            return templates.TemplateResponse("signup.html", {
                "request": request, 
                "error": error_message
            })
        
        # Create user account
        user_service = AuthService()
        signup_result = user_service.signup_user(email, password)
        
        if signup_result:
            # Immediately log in the user after successful signup
            login_result = user_service.login_user(email, password)
            
            if login_result and login_result.session and login_result.session.access_token:
                # User successfully created and logged in
                access_token = login_result.session.access_token
                refresh_token = getattr(login_result.session, 'refresh_token', None)
                
                # Create redirect response to registration page
                redirect_response = RedirectResponse(
                    url="/registration",
                    status_code=status.HTTP_303_SEE_OTHER
                )
                
                # Set session cookies for auto-login
                create_session_cookies(redirect_response, access_token, refresh_token)
                
                return redirect_response
            else:
                # Account created but auto-login failed, redirect to login
                return RedirectResponse(
                    url=f"/login?email={email}&signup_success=true",
                    status_code=status.HTTP_303_SEE_OTHER
                )
        else:
            return templates.TemplateResponse("signup.html", {
                "request": request, 
                "error": "Signup failed. Email may already be in use or there was a server error."
            })
            
    except Exception as e:
        return templates.TemplateResponse("signup.html", {
            "request": request, 
            "error": "Signup failed. Please try again."
        })




            
@router.post('/api/login')
async def make_login(request: Request, response: Response, email: str = Form(...), password: str = Form(...)):
    try:
        email = AuthValidator.sanitize_input(email)
        password = AuthValidator.sanitize_input(password)
        
        email_valid, email_error = AuthValidator.validate_email(email)
        if not email_valid:
            return templates.TemplateResponse("login.html", {
                "request": request, 
                "error": "Invalid email format"
            })
        
        user_service = AuthService()
        res = user_service.login_user(email, password)

        if res and res.session and res.session.access_token and res.user and res.user.id:

            
            if not SecurityHelper.is_secure_session_token(res.session.access_token):
                return templates.TemplateResponse("login.html", {
                    "request": request, 
                    "error": "Invalid session token received"
                })
            
            user_id = res.user.id
            role_service = ProfileService()
            role = role_service.get_role(user_id)
            user_role = None
            
            if role and isinstance(role, list) and len(role) > 0 and 'role' in role[0]:
                user_role = role[0]['role']
                
            if user_role:
                role_valid, role_error = SecurityHelper.validate_role(user_role)
                if not role_valid:
                    return templates.TemplateResponse("login.html", {
                        "request": request, 
                        "error": "Invalid user role detected"
                    })
            
            access_token = res.session.access_token
            refresh_token = getattr(res.session, 'refresh_token', None)
            
            if user_role == 'admin':
                redirect_response = RedirectResponse(
                    url="/admindashboard",
                    status_code=status.HTTP_303_SEE_OTHER
                )
                create_session_cookies(redirect_response, access_token, refresh_token, user_role)
                return redirect_response
            elif user_role == 'student':
                redirect_response = RedirectResponse(
                    url="/studentdashboard",
                    status_code=status.HTTP_303_SEE_OTHER
                )
                create_session_cookies(redirect_response, access_token, refresh_token, user_role)
                return redirect_response
            elif user_role == 'alumni':
                redirect_response = RedirectResponse(
                    url="/alumnidashboard",
                    status_code=status.HTTP_303_SEE_OTHER
                )
                create_session_cookies(redirect_response, access_token, refresh_token, user_role)
                return redirect_response
            else:
                redirect_response = RedirectResponse(
                    url="/registration",
                    status_code=status.HTTP_303_SEE_OTHER
                )
                create_session_cookies(redirect_response, access_token, refresh_token)
                return redirect_response
        else:
            return templates.TemplateResponse("login.html", {
                "request": request, 
                "error": "Invalid email or password"
            })
    except Exception as e:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Login failed. Please try again."
        })


@router.get("/dashboard")
async def dashboard_redirect(request: Request):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    role = request.state.user_role
    role_redirects = {
        "admin": "/admindashboard",
        "student": "/studentdashboard",
        "alumni": "/alumnidashboard",
    }

    return RedirectResponse(
        url=role_redirects.get(role, "/login"),
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get('/admindashboard')
@protected_route(["admin"])
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("admindashboard.html", {"request": request})



@router.get('/details')
async def get_details(request: Request):
    return templates.TemplateResponse("details.html", {"request": request})

@router.post('/api/details')
async def post_details(request: Request, first_name: str = Form(...), last_name: str = Form(...)):
    return RedirectResponse(url="/dashboard", status_code=303)


@router.post('/api/logout')
async def logout(request: Request, response: Response):
    session_token = request.cookies.get('user_session')
    

    if session_token:
        try:
            auth_service = AuthService()
            auth_service.logout_user()
        except Exception as e:
            pass
    
    redirect_response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    clear_session_cookies(redirect_response)
    return redirect_response

@router.get('/logout')
async def logout_get(request: Request, response: Response):
    session_token = request.cookies.get('user_session')
    

    if session_token:
        try:
            auth_service = AuthService()
            auth_service.logout_user()
        except Exception as e:
            pass
    
    redirect_response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    clear_session_cookies(redirect_response)
    return redirect_response

@router.get('/forgot-password')
async def forgot_password_page(request: Request):
    user = await get_current_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@router.get('/reset-password')
async def reset_password_page(request: Request, token: str = ""):
    user = await get_current_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("reset_password.html", {"request": request, "token": token})

@router.post('/api/forgot-password')
async def forgot_password_submit(request: Request, email: str = Form(...)):
    try:
        email = AuthValidator.sanitize_input(email)
        email_valid, email_error = AuthValidator.validate_email(email)
        
        if not email_valid:
            return templates.TemplateResponse("forgot_password.html", {
                "request": request, 
                "error": email_error
            })
        
        auth_service = AuthService()
        result = auth_service.reset_password(email)
        
        if result:
            return templates.TemplateResponse("forgot_password.html", {
                "request": request, 
                "success": "Password reset instructions have been sent to your email address."
            })
        else:
            return templates.TemplateResponse("forgot_password.html", {
                "request": request, 
                "error": "Failed to send password reset email. Please check if the email address is registered."
            })
    except Exception as e:
        return templates.TemplateResponse("forgot_password.html", {
            "request": request, 
            "error": "An error occurred. Please try again later."
        })

@router.post('/api/reset-password')
async def reset_password_submit(request: Request, token: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    try:
        token = AuthValidator.sanitize_input(token)
        password = AuthValidator.sanitize_input(password)
        confirm_password = AuthValidator.sanitize_input(confirm_password)
        
        if password != confirm_password:
            return templates.TemplateResponse("reset_password.html", {
                "request": request, 
                "token": token,
                "error": "Passwords do not match"
            })
        
        password_valid, password_errors = AuthValidator.validate_password(password)
        if not password_valid:
            error_message = "Password requirements not met: " + "; ".join(password_errors)
            return templates.TemplateResponse("reset_password.html", {
                "request": request, 
                "token": token,
                "error": error_message
            })
        
        auth_service = AuthService()
        result = auth_service.update_password(token, password)
        
        if result:
            return templates.TemplateResponse("login.html", {
                "request": request, 
                "success": "Password updated successfully. Please sign in with your new password."
            })
        else:
            return templates.TemplateResponse("reset_password.html", {
                "request": request, 
                "token": token,
                "error": "Failed to update password. The reset link may have expired."
            })
    except Exception as e:
        return templates.TemplateResponse("reset_password.html", {
            "request": request, 
            "token": token,
            "error": "An error occurred. Please try again later."
        })

@router.post('/api/refresh-token')
async def refresh_token_endpoint(request: Request, response: Response):
    try:
        refresh_token = request.cookies.get('refresh_token')
        
        if not refresh_token:
            return {"success": False, "error": "No refresh token found"}
        
        auth_service = AuthService()
        result = auth_service.refresh_token(refresh_token)
        
        if result and hasattr(result, 'session') and result.session:
            new_access_token = result.session.access_token
            new_refresh_token = getattr(result.session, 'refresh_token', refresh_token)
            
            if SecurityHelper.is_secure_session_token(new_access_token):
                # Get user role for appropriate session duration
                user = auth_service.current_user(new_access_token)
                user_role = None
                
                if user:
                    profile_service = ProfileService()
                    role_data = profile_service.get_role(user.user.id)
                    if role_data and isinstance(role_data, list) and len(role_data) > 0 and 'role' in role_data[0]:
                        user_role = role_data[0]['role']
                
                # Update cookies with new tokens
                create_session_cookies(response, new_access_token, new_refresh_token, user_role)
                
                return {"success": True, "message": "Session refreshed successfully"}
        
        return {"success": False, "error": "Failed to refresh session"}
        
    except Exception as e:
        return {"success": False, "error": "An error occurred while refreshing session"}






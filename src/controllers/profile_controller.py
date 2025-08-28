from typing import Self
from fastapi import FastAPI,APIRouter,Form,Request,Response
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi import status
from fastapi.templating import Jinja2Templates
from ..services.auth_services import AuthService
from ..repositories.auth_repository import AuthRepository
from ..services.profile_services import ProfileService
from ..auth_utils import get_current_user, protected_route, create_session_cookies
from ..validators import AuthValidator, SecurityHelper
import pprint

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get('/registration')
async def registration_page(request: Request, response: Response, verified_email: str = "", email_verified: str = ""):
    
    user = await get_current_user(request)
    if user:
        return templates.TemplateResponse('registration.html', {"request": request})
    
    if verified_email and email_verified == "true":
        
        import secrets
        verification_session_id = secrets.token_urlsafe(32)
        
        try:
            auth_service = AuthService()
            
            return templates.TemplateResponse('registration.html', {
                "request": request,
                "verified_email": verified_email,
                "email_verified": True,
                "verification_session_id": verification_session_id
            })
            
        except Exception as e:
            pass
        
        return RedirectResponse(
            url=f"/login?verified_email={verified_email}&verification_success=true",
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    return RedirectResponse(
        url="/login",
        status_code=status.HTTP_303_SEE_OTHER
    )

# Removed the /dashboard route to avoid conflict with auth_controller.py

@router.post('/api/create/profile')
async def update_profile(
    request: Request, 
    response: Response, 
    first_name: str = Form(...), 
    last_name: str = Form(...), 
    role: str = Form(...),
    verified_email: str = Form(""),
    verification_session_id: str = Form("")
):
    profile_service = ProfileService()
    
    # Check if user is authenticated OR this is a verified email user
    user = await get_current_user(request)
    
    # Handle verified email users who don't have active sessions yet
    if not user and verified_email and verification_session_id:
        # Process profile creation for verified email user
        
        # For verified email users, we'll get a temporary user ID from the database
        try:
            auth_service = AuthService()
            
            # Get the user by email to find their user ID
            user_data = auth_service.get_user_by_email(verified_email)
            if user_data and 'id' in user_data:
                temp_user_id = user_data['id']
                # User ID found for verified email
                pass
            else:
                # If no profile exists, we need to get the auth user ID
                # Since they signed up, they should exist in auth.users
                # No profile found, will use email for ID lookup
                pass
                # We'll use the email as identifier and let the profile creation handle the ID
                temp_user_id = verified_email  # Temporary - will be resolved in profile creation
            
        except Exception as e:
            # Error finding user data
            return templates.TemplateResponse('registration.html', {
                "request": request,
                "error": "User not found. Please sign up again.",
                "verified_email": verified_email
            })
    
    elif not user:
        # User not authenticated and not verified email user
        return RedirectResponse('/login')
    
    else:
        # Regular authenticated user
        temp_user_id = user.user.id
    
    # Validate input fields
    first_name = AuthValidator.sanitize_input(first_name)
    last_name = AuthValidator.sanitize_input(last_name)
    role = AuthValidator.sanitize_input(role)
    
    # Validate names
    first_name_valid, first_name_error = AuthValidator.validate_name(first_name, "First name")
    if not first_name_valid:
        return templates.TemplateResponse('registration.html', {
            "request": request, 
            "error": first_name_error,
            "verified_email": verified_email
        })
    
    last_name_valid, last_name_error = AuthValidator.validate_name(last_name, "Last name")
    if not last_name_valid:
        return templates.TemplateResponse('registration.html', {
            "request": request, 
            "error": last_name_error,
            "verified_email": verified_email
        })
    
    # Validate role
    role_valid, role_error = SecurityHelper.validate_role(role)
    if not role_valid:
        return templates.TemplateResponse('registration.html', {
            "request": request, 
            "error": role_error,
            "verified_email": verified_email
        })
    
    # Resolve user ID for verified email users
    if verified_email and verification_session_id and temp_user_id == verified_email:
        # Need to look up the actual user ID from Supabase auth
        try:
            # Query Supabase to get the user ID
            # This is a simplified approach - in production you might want better error handling
            auth_service = AuthService()
            
            # Try to find user by querying profiles table first
            user_data = auth_service.get_user_by_email(verified_email)
            if user_data and 'id' in user_data:
                actual_user_id = user_data['id']
            else:
                # If no profile, generate a UUID for now
                # The user exists in auth.users but not in profiles yet
                import uuid
                actual_user_id = str(uuid.uuid4())
                # Generated new UUID for verified email user
                pass
            
            temp_user_id = actual_user_id
            
        except Exception as e:
            # Error resolving user ID
            import uuid
            temp_user_id = str(uuid.uuid4())
    
    profile = {
        "id": temp_user_id,
        "first_name": first_name,
        "last_name": last_name,
        "role": role.lower()
    }
    
    result = profile_service.create_user_profile(profile)
    
    if result:
        # If this was a verified email user, now create the proper session
        if verified_email and verification_session_id and not user:
            try:
                # Create authenticated session for newly registered user
                pass
                
                # After profile creation, the user should be able to login normally
                # We'll redirect them to login with a success message
                # This avoids JWT token issues and uses the standard login flow
                
                redirect_url = f"/login?registration_complete=true&email={verified_email}&role={role.lower()}"
                return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
                
            except Exception as session_error:
                # Error creating session for verified user
                # Fallback to login
                return RedirectResponse(
                    url=f"/login?registration_complete=true&email={verified_email}",
                    status_code=status.HTTP_303_SEE_OTHER
                )
        
        # Regular authenticated user flow
        session_token = request.cookies.get('user_session')
        refresh_token = request.cookies.get('refresh_token')
        
        # Update session cookies with role-based duration
        if session_token:
            create_session_cookies(response, session_token, refresh_token, role.lower())
        
        # After profile creation, redirect to the correct dashboard based on role
        if role.lower() == 'admin':
            redirect_response = RedirectResponse(url="/admindashboard", status_code=status.HTTP_303_SEE_OTHER)
        elif role.lower() == 'student':
            redirect_response = RedirectResponse(url="/studentdashboard", status_code=status.HTTP_303_SEE_OTHER)
        elif role.lower() == 'alumni':
            redirect_response = RedirectResponse(url="/alumnidashboard", status_code=status.HTTP_303_SEE_OTHER)
        else:
            redirect_response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        
        # Copy cookies to the redirect response
        if session_token:
            create_session_cookies(redirect_response, session_token, refresh_token, role.lower())
        
        return redirect_response
    else:
        return templates.TemplateResponse('registration.html', {
            "request": request, 
            "error": "Failed to create profile. Please try again.",
            "verified_email": verified_email
        })
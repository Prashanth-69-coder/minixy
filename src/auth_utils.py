from functools import wraps
from fastapi import Request, status, Response
from fastapi.responses import RedirectResponse
from .services.auth_services import AuthService
from .services.profile_services import ProfileService
from .validators import SecurityHelper
from typing import Optional
import time

async def get_current_user(request: Request, response: Optional[Response] = None):
    session_token = request.cookies.get('user_session')
    refresh_token = request.cookies.get('refresh_token')
    
    if not session_token:
        return None
    
    try:

        if not SecurityHelper.is_secure_session_token(session_token):
            return None
        
        auth_service = AuthService()
        user = auth_service.current_user(session_token)
        

        if not user and refresh_token:
            try:

                refresh_result = auth_service.refresh_token(refresh_token)
                
                if refresh_result and hasattr(refresh_result, 'session') and refresh_result.session:
                    new_access_token = refresh_result.session.access_token
                    new_refresh_token = refresh_result.session.refresh_token
                    

                    if SecurityHelper.is_secure_session_token(new_access_token):

                        user = auth_service.current_user(new_access_token)
                        
                        if user and response:

                            response.set_cookie(
                                key="user_session",
                                value=new_access_token,
                                httponly=True,
                                secure=True,
                                samesite='lax',
                                max_age=3600  # 1 hour
                            )
                            response.set_cookie(
                                key="refresh_token",
                                value=new_refresh_token,
                                httponly=True,
                                secure=True,
                                samesite='lax',
                                max_age=604800  # 7 days
                            )
            except Exception as refresh_error:
                return None
        
        if user:

            profile_service = ProfileService()
            role_data = profile_service.get_role(user.user.id)
            user_role = None
            
            if role_data and isinstance(role_data, list) and len(role_data) > 0 and 'role' in role_data[0]:
                user_role = role_data[0]['role']
            

            request.state.user = user
            request.state.user_role = user_role
            request.state.session_refreshed = hasattr(request.state, 'session_refreshed') and request.state.session_refreshed
            
            return user
        
        return None
    except Exception as e:
        return None

def protected_route(allowed_roles=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            from fastapi import Response
            

            response = Response()
            

            user = await get_current_user(request, response)
            
            if not user:
                return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
            

            if allowed_roles:
                user_role = getattr(request.state, 'user_role', None)
                if user_role not in allowed_roles:
                    return RedirectResponse(url="/login", status_code=status.HTTP_403_FORBIDDEN)
            

            result = await func(request, *args, **kwargs)
            

            if hasattr(request.state, 'session_refreshed') and request.state.session_refreshed:

                pass
            
            return result
        return wrapper
    return decorator

def protected_api_route(allowed_roles=None):
    """API-specific protected route decorator that returns JSON responses"""
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            from fastapi import Response, HTTPException
            
            response = Response()
            user = await get_current_user(request, response)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            if allowed_roles:
                user_role = getattr(request.state, 'user_role', None)
                if user_role not in allowed_roles:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Access denied. Required roles: {allowed_roles}, User role: {user_role}"
                    )
            
            result = await func(request, *args, **kwargs)
            return result
        return wrapper
    return decorator

def create_session_cookies(response: Response, access_token: str, refresh_token: Optional[str] = None, role: Optional[str] = None):

    session_max_age = 604800 if role == 'admin' else 3600  # 7 days for admin, 1 hour for others
    refresh_max_age = 2592000  # 30 days for refresh token
    
    response.set_cookie(
        key="user_session",
        value=access_token,
        httponly=True,
        secure=True,
        samesite='lax',
        max_age=session_max_age
    )
    
    if refresh_token:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='lax',
            max_age=refresh_max_age
        )

def clear_session_cookies(response: Response):
    response.delete_cookie(key="user_session")
    response.delete_cookie(key="refresh_token")

def is_session_expired(request: Request) -> bool:
    try:
        session_token = request.cookies.get('user_session')
        if not session_token:
            return True
        

        return False
    except Exception:
        return True
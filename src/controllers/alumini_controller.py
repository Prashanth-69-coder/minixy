
from typing import Optional
from fastapi import APIRouter, Form, Request, UploadFile, Body, HTTPException, status, File
from ..services.post_services import PostServices
from ..services.auth_services import AuthService
from ..services.profile_services import ProfileService
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from ..services.conversations_services import ConversationsService
from ..services.messages_services import MessagesService
from ..services.mentorship_services import MentorshipService
from ..services.reactions_services import ReactionsService
from ..services.comments_services import CommentsService
from ..services.notifications_services import NotificationsService
from ..auth_utils import get_current_user, protected_route, protected_api_route
from pydantic import BaseModel


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get('/alumnidashboard', name='alumni_dashboard')
@protected_route(["alumni"])
async def alumni_dashboard(request: Request, filter_type: str = "newest", search: str = "", role_filter: str = ""):

    user = request.state.user
    
    profile_info = ProfileService()
    profile_details = profile_info.get_profile(user.user.id)
    
    posts_service = PostServices()
    
    # Apply filters in order of priority
    if search.strip():
        posts = posts_service.search_posts(search) or []
    elif role_filter and role_filter in ['student', 'alumni']:
        posts = posts_service.reterive_posts_by_role(role_filter) or []
    else:
        posts = posts_service.reterive_posts_by_filter(filter_type) or []
    

    profile_service = ProfileService()
    reactions_service = ReactionsService()
    comments_service = CommentsService()
    

    user_ids = list(set(post['user_id'] for post in posts))
    post_ids = [post['id'] for post in posts]
    
    if user_ids:

        profiles_dict = profile_service.get_profiles_batch(user_ids)
        
        # Get user's reactions for all posts
        user_reactions = reactions_service.get_user_reactions_for_posts(user.user.id, post_ids)
        

        for post in posts:
            profile = profiles_dict.get(post['user_id'])
            if profile:
                post['author_first_name'] = profile.get('first_name', 'Unknown')
                post['author_last_name'] = profile.get('last_name', '')
                post['author_role'] = profile.get('role', 'Alumni')
            else:
                post['author_first_name'] = 'Unknown'
                post['author_last_name'] = ''
                post['author_role'] = 'Alumni'
            
            # Add user's reaction status for this post
            post['user_liked'] = user_reactions.get(post['id']) == 'like'
            
            # Add ownership information
            post['is_owner'] = post['user_id'] == user.user.id
    
    if profile_details and len(profile_details) > 0:
        profile_dict = profile_details[0]
        context = {
            "request": request, 
            "profile": profile_dict, 
            "posts": posts, 
            "current_filter": filter_type,
            "current_search": search,
            "current_role_filter": role_filter
        }
        return templates.TemplateResponse("alumnidashboard.html", context)
    

    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@router.post('/alumnidashboard', name='alumni_dashboard_post')
@protected_route(["alumni"])
async def alumni_dashboard_post(request: Request, title: str = Form(...), description: str = Form(...), image: Optional[UploadFile] = File(None)):
    user = request.state.user
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    post_service = PostServices()
    post_data = {
        "user_id": user.user.id,
        "title": title,
        "description": description
    }
    
    if image is not None and getattr(image, 'filename', None):
        try:
            image_urls = post_service.post_repo.upload_file([image], user.user.id)
            if image_urls:
                post_data["image"] = image_urls[0]
        except Exception as e:

            pass
    
    try:
        post_service.create_post(post_data)
    except Exception as e:

        pass
    
    return RedirectResponse(url="/alumnidashboard", status_code=status.HTTP_303_SEE_OTHER)

@router.get('/alumni_mentorhub', name='alumni_mentorship')
@protected_route(["alumni"])
async def alumni_mentorhub(request: Request, response_class=HTMLResponse):
    user = request.state.user
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    profile_service = ProfileService()

    alumni_list = profile_service.get_all_alumni(user.user.id)
    
    profile_details = profile_service.get_profile(user.user.id)
    if profile_details and len(profile_details) > 0:
        profile = profile_details[0]
    else:

        profile = {
            'id': user.user.id,
            'first_name': 'Alumni',
            'last_name': '',
            'headline': 'Alumni',
            'email': user.user.email if hasattr(user.user, 'email') else '',
            'role': 'alumni'
        }
    
    return templates.TemplateResponse(
        "alumni_mentorhub.html",
        {"request": request, "alumni_list": alumni_list, "profile": profile}
    )

@router.get('/alumni_profile', name='alumni_profile')
@protected_route(["alumni"])
async def alumni_profile(request: Request, response_class=HTMLResponse):
    user = request.state.user
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    profile_service = ProfileService()
    profile_details = profile_service.get_profile(user.user.id)
    
    if profile_details and len(profile_details) > 0:
        profile = profile_details[0]
    else:

        profile = {
            'id': user.user.id,
            'first_name': 'Alumni',
            'last_name': '',
            'headline': 'Alumni',
            'email': user.user.email if hasattr(user.user, 'email') else '',
            'role': 'alumni'
        }
    
    return templates.TemplateResponse("alumini_profile.html", {"request": request, "profile": profile})

@router.get('/alumni_jobs', name='alumni_jobs')
@protected_route(["alumni"])
async def alumni_jobs(request: Request, response_class=HTMLResponse):
    user = request.state.user
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    profile_service = ProfileService()
    profile_details = profile_service.get_profile(user.user.id)
    
    if profile_details and len(profile_details) > 0:
        profile = profile_details[0]
    else:

        profile = {
            'id': user.user.id,
            'first_name': 'Alumni',
            'last_name': '',
            'headline': 'Alumni',
            'email': user.user.email if hasattr(user.user, 'email') else '',
            'role': 'alumni'
        }
    
    return templates.TemplateResponse("alumni_jobs.html", {"request": request, "profile": profile})

@router.get('/alumni_messages', name='alumni_messages')
@protected_route(["alumni"])
async def alumni_messages(request: Request):
    user = request.state.user
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    profile_service = ProfileService()
    profile_details = profile_service.get_profile(user.user.id)
    
    if profile_details and len(profile_details) > 0:
        profile = profile_details[0]
    else:

        profile = {
            'id': user.user.id,
            'first_name': 'Alumni',
            'last_name': '',
            'headline': 'Alumni',
            'email': user.user.email if hasattr(user.user, 'email') else '',
            'role': 'alumni'
        }
    
    return templates.TemplateResponse("alumni_messages.html", {"request": request, "profile": profile})

@router.get('/api/alumni/conversations')
@protected_api_route(["alumni"])
async def get_user_conversations(request: Request):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        conv_service = ConversationsService()
        profile_service = ProfileService()
        conversations = conv_service.get_user_conversations(user.user.id)
        
        enriched = []
        for conv in conversations:
            other_id = conv['sender_id'] if conv['receiver_id'] == user.user.id else conv['receiver_id']
            other_profile = profile_service.get_profile(other_id)
            
            if other_profile and len(other_profile) > 0:
                other_name = f"{other_profile[0].get('first_name', '')} {other_profile[0].get('last_name', '')}".strip()
                other_email = other_profile[0].get('email', '')
            else:
                other_name = other_email = ''
            
            conv['other_user_name'] = other_name
            conv['other_user_email'] = other_email
            enriched.append(conv)
        
        return {"conversations": enriched}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch conversations")

@router.get('/api/alumni/messages/{conversation_id}')
@protected_api_route(["alumni"])
async def get_conversation_messages(request: Request, conversation_id: str):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        
    try:
        messages_service = MessagesService()
        messages = messages_service.get_messages(conversation_id)
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch messages")

class AlumniMessageBody(BaseModel):
    content: str

@router.post('/api/alumni/messages/{conversation_id}')
@protected_api_route(["alumni"])
async def send_message(request: Request, conversation_id: str, body: AlumniMessageBody):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        messages_service = MessagesService()
        message = messages_service.create_message(conversation_id, user.user.id, body.content)
        return {"success": True, "message": message}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send message")

@router.post('/api/mentor-request-message')
@protected_api_route(["alumni", "student"])
async def mentor_request_message(request: Request, requester_id: str = Body(...), receiver_id: str = Body(...), description: str = Body(...)):
    try:
        conv_service = ConversationsService()
        messages_service = MessagesService()
        mentor_service = MentorshipService()
        
        conversation_id = conv_service.get_or_create_conversation(requester_id, receiver_id)
        message = messages_service.create_message(conversation_id, requester_id, description)
        mentor_request = mentor_service.create_mentor_request(requester_id, receiver_id, description)
        
        return {"success": True, "conversation_id": conversation_id, "message": message, "mentorship_request": mentor_request}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create mentor request")

# Mentorship Request Management APIs
@router.get('/api/mentorship/requests')
@protected_api_route(["alumni"])
async def get_mentor_requests(request: Request):
    """Get all mentorship requests for the logged-in alumni"""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        mentor_service = MentorshipService()
        requests = mentor_service.get_mentor_requests_for_alumni(user.user.id)
        return {"success": True, "requests": requests}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch mentor requests")

@router.post('/api/mentorship/requests/{request_id}/accept')
@protected_api_route(["alumni"])
async def accept_mentor_request(request: Request, request_id: str):
    """Accept a mentorship request"""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        mentor_service = MentorshipService()
        result = mentor_service.accept_mentor_request(request_id, user.user.id)
        
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result['error'])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to accept mentor request")

@router.post('/api/mentorship/requests/{request_id}/reject')
@protected_api_route(["alumni"])
async def reject_mentor_request(request: Request, request_id: str):
    """Reject a mentorship request"""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        mentor_service = MentorshipService()
        result = mentor_service.reject_mentor_request(request_id, user.user.id)
        
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result['error'])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to reject mentor request")

@router.post('/api/mentorship/availability')
@protected_api_route(["alumni"])
async def toggle_mentor_availability(request: Request, available: bool = Body(...)):
    """Toggle mentor availability status"""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        mentor_service = MentorshipService()
        result = mentor_service.set_mentor_availability(user.user.id, available)
        
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result['error'])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update availability")

@router.get('/api/mentorship/statistics')
@protected_api_route(["alumni"])
async def get_mentorship_statistics(request: Request):
    """Get mentorship statistics for the logged-in alumni"""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        mentor_service = MentorshipService()
        stats = mentor_service.get_mentorship_statistics(user.user.id)
        return {"success": True, "statistics": stats}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch statistics")

@router.get('/api/mentorship/available-mentors')
@protected_api_route(["alumni"])
async def get_available_mentors(request: Request, expertise: Optional[str] = None, search: Optional[str] = None):
    """Get list of available mentors with optional filtering"""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        mentor_service = MentorshipService()
        mentors = mentor_service.get_available_mentors(expertise, search)
        return {"success": True, "mentors": mentors}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch available mentors")

@router.post('/api/jobs')
@protected_api_route(["alumni"])
async def create_job(request: Request, title: str = Form(...), description: str = Form(...), company: str = Form(...), location: str = Form(...), type: str = Form("Full-time"), visible: Optional[str] = Form(None)):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        from ..repositories.alumini_jobs_repository import AluminiJobsRepository
        
        # Validate required fields
        if not title or not description or not company or not location:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required")
        
        visible_bool = str(visible).lower() in ['true', '1', 'on', 'yes'] if visible is not None else True
        
        job_data = {
            "title": title,
            "description": description,
            "company": company,
            "location": location,
            "visible": visible_bool,
            "posted_by": user.user.id
        }
        
        jobs_repo = AluminiJobsRepository()
        result = jobs_repo.create_job(job_data)
        
        return {"success": True, "job": result}
    except HTTPException:
        raise
    except Exception as e:
        # Log the actual error for debugging
        import logging
        logging.error(f"Error creating job: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create job: {str(e)}")

@router.get('/api/jobs')
@protected_api_route(["alumni"])
async def list_jobs(request: Request, search: Optional[str] = None, location: Optional[str] = None):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        from ..repositories.alumini_jobs_repository import AluminiJobsRepository
        
        jobs_repo = AluminiJobsRepository()

        # Get all visible jobs first
        jobs = jobs_repo.list_visible_jobs(user.user.id)
        
        # Apply filters if provided
        if search:
            search_lower = search.lower()
            jobs = [job for job in jobs if 
                   search_lower in (job.get('title', '').lower() if job.get('title') else '') or
                   search_lower in (job.get('company', '').lower() if job.get('company') else '') or
                   search_lower in (job.get('description', '').lower() if job.get('description') else '')]
        
        if location:
            location_lower = location.lower()
            jobs = [job for job in jobs if 
                   location_lower in (job.get('location', '').lower() if job.get('location') else '')]
        
        profile_service = ProfileService()
        enriched = []
        
        for job in jobs:
            try:
                poster_profile = profile_service.get_profile(job['posted_by'])
                if poster_profile and len(poster_profile) > 0:
                    poster = poster_profile[0]
                    job['poster_name'] = f"{poster.get('first_name', '')} {poster.get('last_name', '')}".strip()
                    job['poster_email'] = poster.get('email', '')
                else:
                    job['poster_name'] = job['poster_email'] = ''
            except Exception as e:
                # Log the error but don't fail the entire request
                import logging
                logging.error(f"Error getting profile for job {job.get('id')}: {str(e)}")
                job['poster_name'] = job['poster_email'] = ''
            enriched.append(job)
        
        return {"jobs": enriched}
    except Exception as e:
        # Log the actual error for debugging
        import logging
        logging.error(f"Error fetching jobs: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch jobs: {str(e)}")

@router.get('/api/my-jobs')
@protected_api_route(["alumni"])
async def list_my_jobs(request: Request):
    """Get jobs posted by the current user"""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        from ..repositories.alumini_jobs_repository import AluminiJobsRepository
        
        jobs_repo = AluminiJobsRepository()
        jobs = jobs_repo.get_jobs_by_user(user.user.id)
        
        return {"jobs": jobs}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch your jobs")

@router.post('/api/jobs/{job_id}/visibility')
@protected_api_route(["alumni"])
async def update_job_visibility(request: Request, job_id: str, body: dict = Body(...)):
    """Update the visibility of a job posting"""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        from ..repositories.alumini_jobs_repository import AluminiJobsRepository
        
        # Extract visibility from request body
        visible = body.get('visible')
        if visible is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Visibility parameter is required")
        
        jobs_repo = AluminiJobsRepository()
        
        # First verify the job belongs to this user
        job = jobs_repo.get_job(job_id)
        if not job or job['posted_by'] != user.user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this job")
        
        # Update visibility
        updated_job = jobs_repo.update_job_visibility(job_id, visible)
        
        return {"success": True, "job": updated_job}
    except HTTPException:
        raise
    except Exception as e:
        # Log the actual error for debugging
        import logging
        logging.error(f"Error updating job visibility: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update job visibility: {str(e)}")

@router.post('/api/jobs/{job_id}/apply')
@protected_api_route(["alumni"])
async def apply_job(request: Request, job_id: str, message: str = Body(...)):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        from ..repositories.alumini_jobs_repository import AluminiJobsRepository
        
        jobs_repo = AluminiJobsRepository()
        job = jobs_repo.get_job(job_id)
        
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        
        alumni_id = job['posted_by']
        conv_service = ConversationsService()
        messages_service = MessagesService()
        
        conversation_id = conv_service.get_or_create_conversation(user.user.id, alumni_id)
        job_info = f"Job Application for: {job.get('title', 'N/A')} at {job.get('company', 'N/A')} ({job.get('location', 'N/A')})\n\n{message}"
        
        message_obj = messages_service.create_message(conversation_id, user.user.id, job_info)
        
        return {"success": True, "conversation_id": conversation_id, "message": message_obj, "job": job}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to apply to job")

@router.post('/api/profile/update')
@protected_api_route(["alumni"])
async def update_profile(request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    headline: str = Form(None),
    bio: str = Form(None),
    skills: str = Form(None),
    experience: str = Form(None),
    college: str = Form(None),
    graduation_year: Optional[int] = Form(None),
):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        profile_service = ProfileService()

        current_profile = profile_service.get_profile(user.user.id)
        role = current_profile[0].get("role") if current_profile and len(current_profile) > 0 else "alumni"
        
        # Process skills properly
        skills_list = None
        if skills:
            # Split by comma and strip whitespace from each skill
            skills_list = [s.strip() for s in skills.split(',') if s.strip()]
        
        profile_data = {
            "id": user.user.id,
            "first_name": first_name,
            "last_name": last_name,
            "headline": headline,
            "bio": bio,
            "skills": skills_list,  # Use the processed skills list
            "experience": experience,
            "college": college,
            "graduation_year": graduation_year,
            "role": role,
        }
        
        # Use update_profile method for consistency
        result = profile_service.update_profile(profile_data)
        return {"success": bool(result), "profile": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update profile")
     
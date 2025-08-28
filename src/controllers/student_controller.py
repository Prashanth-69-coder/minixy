from typing import Optional
from fastapi import APIRouter, Form, Request, UploadFile, Body, File, HTTPException, status
from ..services.post_services import PostServices
from ..services.auth_services import AuthService
from ..services.profile_services import ProfileService
from ..services.student_services import StudentService
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



@router.get('/studentdashboard')
@protected_route(["student"])
async def student_dashboard(request: Request, filter_type: str = "newest", search: str = "", role_filter: str = ""):
    """Optimized student dashboard with lazy loading for better performance"""
    user = request.state.user
    
    # Get minimal profile info first (fastest query)
    profile_info = ProfileService()
    profile_details = profile_info.get_profile(user.user.id)
    
    # Prepare profile data
    if profile_details and len(profile_details) > 0:
        profile_dict = profile_details[0]
    else:
        # Create minimal default profile for immediate display
        profile_dict = {
            'id': user.user.id,
            'first_name': 'Student',
            'last_name': '',
            'headline': 'Student', 
            'email': user.user.email if hasattr(user.user, 'email') else '',
            'role': 'student'
        }
    
    # Return page immediately with loading state - posts will be loaded via AJAX
    context = {
        "request": request, 
        "profile": profile_dict, 
        "posts": [],  # Empty initially - loaded via AJAX
        "current_filter": filter_type,
        "current_search": search,
        "current_role_filter": role_filter,
        "lazy_load": True  # Flag to enable AJAX loading
    }
    return templates.TemplateResponse("studentdashboard.html", context)

# Optimized API endpoint for lazy loading posts
@router.get('/api/student/posts')
@protected_api_route(["student"])
async def get_student_posts(request: Request, filter_type: str = "newest", search: str = "", role_filter: str = "", limit: int = 10):
    """Optimized endpoint for loading posts with minimal database queries"""
    user = request.state.user
    if not user:
        return {"success": False, "error": "User not authenticated"}
    
    try:
        posts_service = PostServices()
        
        # Apply filters in order of priority
        if search.strip():
            posts = posts_service.search_posts(search, limit) or []
        elif role_filter and role_filter in ['student', 'alumni']:
            posts = posts_service.reterive_posts_by_role(role_filter, limit) or []
        else:
            posts = posts_service.reterive_posts_by_filter(filter_type, limit) or []
        
        if not posts:
            return {"success": True, "posts": []}
        
        # Batch all data fetching for optimal performance
        profile_service = ProfileService()
        reactions_service = ReactionsService()
        
        user_ids = list(set(post['user_id'] for post in posts))
        post_ids = [post['id'] for post in posts]
        
        # Parallel data fetching
        profiles_dict = profile_service.get_profiles_batch(user_ids)
        user_reactions = reactions_service.get_user_reactions_for_posts(user.user.id, post_ids)
        
        # Enrich posts with profile and reaction data
        for post in posts:
            profile = profiles_dict.get(post['user_id'])
            if profile:
                post['author_first_name'] = profile.get('first_name', 'Unknown')
                post['author_last_name'] = profile.get('last_name', '')
                post['author_role'] = profile.get('role', 'User')
            else:
                post['author_first_name'] = 'Unknown'
                post['author_last_name'] = ''
                post['author_role'] = 'User'
            
            # Add user interaction data
            post['user_liked'] = user_reactions.get(post['id']) == 'like'
            post['is_owner'] = post['user_id'] == user.user.id
        
        return {"success": True, "posts": posts}
        
    except Exception as e:
        print(f"Error loading posts: {e}")
        return {"success": False, "error": "Failed to load posts"}

@router.post('/studentdashboard')
@protected_route(["student"])
async def student_dashboard_post(request: Request, title: str = Form(...), description: str = Form(...), image: Optional[UploadFile] = File(None)):
    user = request.state.user
    if not user:
        return RedirectResponse(url="/login")
    
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
    
    return RedirectResponse(url="/studentdashboard", status_code=303)

@router.post('/api/posts/{post_id}/like')
@protected_api_route(["student", "alumni"])
async def toggle_like(request: Request, post_id: str):
    user = request.state.user
    if not user:
        return {"success": False, "error": "User not authenticated"}
    
    reactions_service = ReactionsService()
    notifications_service = NotificationsService()
    
    result = reactions_service.toggle_like(user.user.id, post_id)
    
    # Create notification if post was liked (not unliked)
    if result['success'] and result.get('liked'):
        notifications_service.create_like_notification(post_id, user.user.id)
    
    return result

@router.post('/api/posts/{post_id}/comment')
@protected_api_route(["student", "alumni"])
async def add_comment(request: Request, post_id: str, content: str = Form(...)):
    user = request.state.user
    if not user:
        return {"success": False, "error": "User not authenticated"}
    
    comments_service = CommentsService()
    notifications_service = NotificationsService()
    
    result = comments_service.create_comment(user.user.id, post_id, content)
    
    if result['success']:
        # Create notification for the post owner
        notifications_service.create_comment_notification(post_id, user.user.id)
        
        # Get updated comments count
        comments_count = comments_service.get_post_comments_count(post_id)
        result['comments_count'] = comments_count
    
    return result

@router.get('/api/posts/{post_id}/comments')
@protected_api_route(["student", "alumni"])
async def get_comments(request: Request, post_id: str):
    user = request.state.user
    if not user:
        return {"success": False, "error": "User not authenticated"}
    
    comments_service = CommentsService()
    comments = comments_service.get_post_comments_with_profiles(post_id)
    
    return {"success": True, "comments": comments}

@router.get('/api/posts/{post_id}')
@protected_api_route(["student", "alumni"])
async def get_post(request: Request, post_id: str):
    user = request.state.user
    if not user:
        return {"success": False, "error": "User not authenticated"}
    
    posts_service = PostServices()
    post = posts_service.get_post_by_id(post_id)
    
    if not post:
        return {"success": False, "error": "Post not found"}
    
    # Check if user owns this post
    post['is_owner'] = posts_service.check_post_ownership(post_id, user.user.id)
    
    return {"success": True, "post": post}

@router.put('/api/posts/{post_id}')
@protected_api_route(["student", "alumni"])
async def update_post(request: Request, post_id: str, title: str = Form(...), description: str = Form(...)):
    user = request.state.user
    if not user:
        return {"success": False, "error": "User not authenticated"}
    
    posts_service = PostServices()
    result = posts_service.update_post_content(post_id, user.user.id, title, description)
    
    return result

@router.delete('/api/posts/{post_id}')
@protected_api_route(["student", "alumni"])
async def delete_post(request: Request, post_id: str):
    user = request.state.user
    if not user:
        return {"success": False, "error": "User not authenticated"}
    
    posts_service = PostServices()
    result = posts_service.delete_post(post_id, user.user.id)
    
    return result

@router.get('/api/notifications')
@protected_api_route(["student", "alumni"])
async def get_notifications(request: Request):
    user = request.state.user
    if not user:
        return {"success": False, "error": "User not authenticated"}
    
    notifications_service = NotificationsService()
    result = notifications_service.get_user_notifications(user.user.id)
    
    return result

@router.get('/api/notifications/count')
@protected_api_route(["student", "alumni"])
async def get_notifications_count(request: Request):
    user = request.state.user
    if not user:
        return {"success": False, "error": "User not authenticated"}
    
    notifications_service = NotificationsService()
    result = notifications_service.get_unread_count(user.user.id)
    
    return result

@router.post('/api/notifications/{notification_id}/read')
@protected_api_route(["student", "alumni"])
async def mark_notification_read(request: Request, notification_id: str):
    user = request.state.user
    if not user:
        return {"success": False, "error": "User not authenticated"}
    
    notifications_service = NotificationsService()
    result = notifications_service.mark_notification_as_read(notification_id, user.user.id)
    
    return result

@router.post('/api/notifications/mark-all-read')
@protected_api_route(["student", "alumni"])
async def mark_all_notifications_read(request: Request):
    user = request.state.user
    if not user:
        return {"success": False, "error": "User not authenticated"}
    
    notifications_service = NotificationsService()
    result = notifications_service.mark_all_as_read(user.user.id)
    
    return result

@router.get('/student_mentorhub')
@protected_route()
async def student_mentorhub(request: Request, response_class=HTMLResponse):
    user = request.state.user
    if not user:
        return RedirectResponse(url="/login")
    
    profile_service = ProfileService()
    alumni_list = profile_service.get_all_alumni(user.user.id)
    

    profile_details = profile_service.get_profile(user.user.id)
    

    if profile_details and len(profile_details) > 0:
        profile = profile_details[0]
    else:

        profile = {
            'id': user.user.id,
            'first_name': 'Student',
            'last_name': '',
            'headline': 'Student',
            'email': user.user.email if hasattr(user.user, 'email') else '',
            'role': 'student'
        }
    
    return templates.TemplateResponse(
        "studentmentor.html",
        {"request": request, "alumni_list": alumni_list, "profile": profile}
    )

@router.get('/student_jobs')
@protected_route()
async def student_jobs(request: Request, response_class=HTMLResponse):
    user = request.state.user
    if not user:
        return RedirectResponse(url="/login")
    
    profile_service = ProfileService()
    

    profile_details = profile_service.get_profile(user.user.id)
    

    if profile_details and len(profile_details) > 0:
        profile = profile_details[0]
    else:

        profile = {
            'id': user.user.id,
            'first_name': 'Student',
            'last_name': '',
            'headline': 'Student',
            'email': user.user.email if hasattr(user.user, 'email') else '',
            'role': 'student'
        }
    
    return templates.TemplateResponse(
        "student_job.html",
        {"request": request, "profile": profile}
    )

@router.get('/student_messages')
@protected_route(["student"])
async def student_messages(request: Request):
    user = request.state.user
    if not user:
        return RedirectResponse(url="/login")
    
    profile_service = ProfileService()
    

    profile_details = profile_service.get_profile(user.user.id)
    

    if profile_details and len(profile_details) > 0:
        profile = profile_details[0]
    else:

        profile = {
            'id': user.user.id,
            'first_name': 'Student',
            'last_name': '',
            'headline': 'Student',
            'email': user.user.email if hasattr(user.user, 'email') else '',
            'role': 'student'
        }
    
    return templates.TemplateResponse(
        "student_messages.html",
        {"request": request, "profile": profile}
    )

@router.get('/student_profile')
@protected_route(["student"])
async def student_profile(request: Request, response_class=HTMLResponse):
    user = request.state.user
    if not user:
        return RedirectResponse(url="/login")
    
    profile_service = ProfileService()
    

    profile_details = profile_service.get_profile(user.user.id)
    

    if profile_details and len(profile_details) > 0:
        profile = profile_details[0]
    else:

        profile = {
            'id': user.user.id,
            'first_name': 'Student',
            'last_name': '',
            'headline': 'Student',
            'email': user.user.email if hasattr(user.user, 'email') else '',
            'role': 'student'
        }
    
    return templates.TemplateResponse(
        "student_profile.html",
        {"request": request, "profile": profile}
    )



@router.get('/api/student/conversations')
@protected_api_route(["student"])
async def get_student_conversations(request: Request):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        conv_service = ConversationsService()
        conversations = conv_service.get_user_conversations(user.user.id)
        
        profile_service = ProfileService()
        enriched_conversations = []
        
        for conv in conversations:
            other_user_id = conv['receiver_id'] if conv['sender_id'] == user.user.id else conv['sender_id']
            other_user_profile = profile_service.get_profile(other_user_id)
            
            if other_user_profile and len(other_user_profile) > 0:
                other_profile = other_user_profile[0]
                conv['other_user_name'] = f"{other_profile.get('first_name', '')} {other_profile.get('last_name', '')}".strip()
                conv['other_user_email'] = other_profile.get('email', '')
            else:
                conv['other_user_name'] = 'Unknown User'
                conv['other_user_email'] = ''
            
            enriched_conversations.append(conv)
        
        return {"conversations": enriched_conversations}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch conversations")

class StudentMessageBody(BaseModel):
    content: str

@router.get('/api/student/messages/{conversation_id}')
@protected_api_route(["student"])
async def get_student_conversation_messages(request: Request, conversation_id: str):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        messages_service = MessagesService()
        messages = messages_service.get_messages(conversation_id)
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch messages")

@router.post('/api/student/messages/{conversation_id}')
@protected_api_route(["student"])
async def send_student_message(request: Request, conversation_id: str, body: StudentMessageBody):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        messages_service = MessagesService()
        message = messages_service.create_message(conversation_id, user.user.id, body.content)
        return {"success": True, "message": message}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send message")

@router.post('/api/student/mentor-request-message')
@protected_api_route(["student"])
async def student_mentor_request_message(request: Request, requester_id: str = Body(...), receiver_id: str = Body(...), description: str = Body(...)):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        
    try:
        conv_service = ConversationsService()
        messages_service = MessagesService()
        mentorship_service = MentorshipService()
        
        conversation_id = conv_service.get_or_create_conversation(requester_id, receiver_id)
        message = messages_service.create_message(conversation_id, requester_id, description)
        mentorship_request = mentorship_service.create_mentor_request(requester_id, receiver_id, description)
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "message": message,
            "mentorship_request": mentorship_request
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create mentor request")

@router.get('/api/student/jobs')
@protected_api_route(["student"])
async def list_student_jobs(request: Request):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        student_service = StudentService()
        # Get all visible jobs except those posted by the current user
        jobs = student_service.list_visible_jobs(user.user.id)
        
        # Enrich jobs with poster info
        profile_service = ProfileService()
        enriched_jobs = []
        
        for job in jobs:
            poster_profile = profile_service.get_profile(job['posted_by'])
            if poster_profile and len(poster_profile) > 0:
                poster = poster_profile[0]
                job['poster_name'] = f"{poster.get('first_name', '')} {poster.get('last_name', '')}".strip()
                job['poster_email'] = poster.get('email', '')
            else:
                job['poster_name'] = 'Unknown'
                job['poster_email'] = ''
            
            enriched_jobs.append(job)
        
        return {"success": True, "jobs": enriched_jobs}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch jobs")

class JobApplicationBody(BaseModel):
    message: str

@router.post('/api/student/jobs/{job_id}/apply')
@protected_api_route(["student"])
async def student_apply_job(request: Request, job_id: str, body: JobApplicationBody):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        student_service = StudentService()
        job = student_service.get_job(job_id)
        
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        
        # Create conversation and send application message
        conv_service = ConversationsService()
        messages_service = MessagesService()
        
        conversation_id = conv_service.get_or_create_conversation(user.user.id, job['posted_by'])
        
        # Compose application message with job details
        application_message = f"Job Application for {job['title']} at {job['company']}\n\n{body.message}"
        
        message_obj = messages_service.create_message(conversation_id, user.user.id, application_message)
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "message": message_obj,
            "job": job
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to apply for job")

@router.post('/api/student/profile/update')
@protected_api_route(["student"])
async def update_student_profile(request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    headline: str = Form(None),
    bio: str = Form(None),
    skills: str = Form(None),
    experience: str = Form(None),
    projects: str = Form(None),
    college: str = Form(None),
    graduation_year: Optional[int] = Form(None)
):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        profile_service = ProfileService()
        current_profile = profile_service.get_profile(user.user.id)
        
        if not current_profile or len(current_profile) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        
        current_profile_data = current_profile[0]
        
        # Process skills and projects properly
        skills_list = None
        if skills:
            # Split by comma and strip whitespace from each skill
            skills_list = [s.strip() for s in skills.split(',') if s.strip()]
        
        projects_list = None
        if projects:
            # Split by comma and strip whitespace from each project
            projects_list = [p.strip() for p in projects.split(',') if p.strip()]
        
        profile_data = {
            "id": user.user.id,
            "first_name": first_name,
            "last_name": last_name,
            "headline": headline,
            "bio": bio,
            "skills": skills_list,
            "experience": experience,
            "projects": projects_list,
            "college": college,
            "graduation_year": graduation_year,
            "role": current_profile_data.get('role', 'student')  # Keep existing role
        }
        
        # Use update_profile method for consistency
        updated_profile = profile_service.update_profile(profile_data)
        return {"success": bool(updated_profile), "profile": updated_profile}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update profile")

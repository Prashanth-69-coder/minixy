from typing import Optional
from fastapi import APIRouter, Form, Request, UploadFile, Body
from ..services.post_services import PostServices
from ..services.auth_services import AuthService
from ..services.profile_services import ProfileService
from ..services.student_services import StudentServices
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from ..services.conversations_services import ConversationsService
from ..services.messages_services import MessagesService
from ..services.mentorship_services import MentorshipService
from pydantic import BaseModel

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def logged_user(request: Request):
    session_token = request.cookies.get('user_session')
    user_service = AuthService()
    user = user_service.current_user(session_token)
    if user:
        return user
    else:
        return None

@router.get('/studentdashboard')
def student_dashboard(request: Request):
    user = logged_user(request)
    if not user:
        return RedirectResponse(url="/login")
    
    profile_info = ProfileService()
    profile_details = profile_info.get_profile(user.user.id)
    
    # Use the exact same posts retrieval as alumni controller
    posts_service = PostServices()
    posts = posts_service.reterive_posts() or []
    
    profile_service = ProfileService()
    
    # Enrich all posts with author information
    for post in posts:
        user_profile = profile_service.get_profile(post['user_id'])
        if user_profile and len(user_profile) > 0:
            profile = user_profile[0]
            post['author_first_name'] = profile.get('first_name', 'Unknown')
            post['author_last_name'] = profile.get('last_name', '')
            post['author_role'] = profile.get('role', 'User')
        else:
            post['author_first_name'] = 'Unknown'
            post['author_last_name'] = ''
            post['author_role'] = 'User'
    
    # Create profile data - use existing profile or create default
    if profile_details and len(profile_details) > 0:
        profile_dict = profile_details[0]
    else:
        # Create a default profile for students who don't have one yet
        profile_dict = {
            'id': user.user.id,
            'first_name': 'Student',
            'last_name': '',
            'headline': 'Student',
            'email': user.user.email if hasattr(user.user, 'email') else '',
            'role': 'student'
        }
    
    context = {"request": request, "profile": profile_dict, "posts": posts}
    return templates.TemplateResponse("studentdashboard.html", context)

@router.post('/studentdashboard')
def student_dashboard_post(request: Request, title: str = Form(...), description: str = Form(...), image: UploadFile = None):
    user = logged_user(request)
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

@router.get('/student_mentorhub')
def student_mentorhub(request: Request, response_class=HTMLResponse):
    user = logged_user(request)
    if not user:
        return RedirectResponse(url="/login")
    
    profile_service = ProfileService()
    alumni_list = profile_service.get_all_alumni()
    
    # Get user profile
    profile_details = profile_service.get_profile(user.user.id)
    
    # Ensure we have profile data or provide defaults
    if profile_details and len(profile_details) > 0:
        profile = profile_details[0]
    else:
        # Create a default profile if none exists
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
def student_jobs(request: Request, response_class=HTMLResponse):
    user = logged_user(request)
    if not user:
        return RedirectResponse(url="/login")
    
    profile_service = ProfileService()
    
    # Get user profile
    profile_details = profile_service.get_profile(user.user.id)
    
    # Ensure we have profile data or provide defaults
    if profile_details and len(profile_details) > 0:
        profile = profile_details[0]
    else:
        # Create a default profile if none exists
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
def student_messages(request: Request):
    user = logged_user(request)
    if not user:
        return RedirectResponse(url="/login")
    
    profile_service = ProfileService()
    
    # Get user profile
    profile_details = profile_service.get_profile(user.user.id)
    
    # Ensure we have profile data or provide defaults
    if profile_details and len(profile_details) > 0:
        profile = profile_details[0]
    else:
        # Create a default profile if none exists
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
def student_profile(request: Request, response_class=HTMLResponse):
    user = logged_user(request)
    if not user:
        return RedirectResponse(url="/login")
    
    profile_service = ProfileService()
    
    # Get user profile
    profile_details = profile_service.get_profile(user.user.id)
    
    # Ensure we have profile data or provide defaults
    if profile_details and len(profile_details) > 0:
        profile = profile_details[0]
    else:
        # Create a default profile if none exists
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

# API Endpoints for student features

@router.get('/api/student/conversations')
def get_student_conversations(request: Request):
    user = logged_user(request)
    if not user:
        return {"error": "Not authenticated"}
    
    conv_service = ConversationsService()
    conversations = conv_service.get_user_conversations(user.user.id)
    
    # Enrich conversations with other user info
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

@router.get('/api/student/messages/{conversation_id}')
def get_student_conversation_messages(conversation_id: str):
    messages_service = MessagesService()
    messages = messages_service.get_messages(conversation_id)
    return {"messages": messages}

class StudentMessageBody(BaseModel):
    content: str

@router.post('/api/student/messages/{conversation_id}')
def send_student_message(request: Request, conversation_id: str, body: StudentMessageBody):
    user = logged_user(request)
    if not user:
        return {"error": "Not authenticated"}
    
    messages_service = MessagesService()
    message = messages_service.create_message(conversation_id, user.user.id, body.content)
    return {"message": message}

@router.post('/api/student/mentor-request-message')
def student_mentor_request_message(request: Request, requester_id: str = Body(...), receiver_id: str = Body(...), description: str = Body(...)):
    conv_service = ConversationsService()
    messages_service = MessagesService()
    mentorship_service = MentorshipService()
    
    # Create or get conversation
    conversation_id = conv_service.get_or_create_conversation(requester_id, receiver_id)
    
    # Create message
    message = messages_service.create_message(conversation_id, requester_id, description)
    
    # Create mentorship request
    mentorship_request = mentorship_service.create_mentor_request(requester_id, receiver_id, description)
    
    return {
        "conversation_id": conversation_id,
        "message": message,
        "mentorship_request": mentorship_request
    }

@router.get('/api/student/jobs')
def list_student_jobs(request: Request):
    user = logged_user(request)
    if not user:
        return {"error": "Not authenticated"}
    
    student_service = StudentServices()
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
    
    return {"jobs": enriched_jobs}

class JobApplicationBody(BaseModel):
    message: str

@router.post('/api/student/jobs/{job_id}/apply')
def student_apply_job(request: Request, job_id: str, body: JobApplicationBody):
    user = logged_user(request)
    if not user:
        return {"error": "Not authenticated"}
    
    student_service = StudentServices()
    job = student_service.get_job(job_id)
    
    if not job:
        return {"error": "Job not found"}
    
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

@router.post('/api/student/profile/update')
def update_student_profile(request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    headline: str = Form(None),
    bio: str = Form(None),
    skills: str = Form(None),
    experience: str = Form(None),
    projects: str = Form(None)
):
    user = logged_user(request)
    if not user:
        return {"error": "Not authenticated"}
    
    profile_service = ProfileService()
    current_profile = profile_service.get_profile(user.user.id)
    
    if not current_profile or len(current_profile) == 0:
        return {"error": "Profile not found"}
    
    current_profile_data = current_profile[0]
    
    # Process skills and projects
    skills_list = None
    if skills:
        skills_list = [s.strip() for s in skills.split(',')]
    
    projects_list = None
    if projects:
        projects_list = [p.strip() for p in projects.split(',')]
    
    profile_data = {
        "id": user.user.id,
        "first_name": first_name,
        "last_name": last_name,
        "headline": headline,
        "bio": bio,
        "skills": skills_list,
        "experience": experience,
        "projects": projects_list,
        "role": current_profile_data.get('role', 'student')  # Keep existing role
    }
    
    try:
        updated_profile = profile_service.update_profile(profile_data)
        return {"success": True, "profile": updated_profile}
    except Exception as e:
        return {"error": str(e)} 
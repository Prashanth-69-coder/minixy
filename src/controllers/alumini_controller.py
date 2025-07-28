
from typing import Self, Optional
from fastapi import FastAPI,APIRouter,Form,Request,UploadFile,Body
from ..services.post_services import PostServices
from ..services.auth_services import AuthService
from ..services.profile_services import ProfileService
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from ..services.conversations_services import ConversationsService
from ..services.messages_services import MessagesService
from ..services.mentorship_services import MentorshipService
from pydantic import BaseModel


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



@router.get('/alumnidashboard')
def alumni_dashboard(request: Request):
    user = logged_user(request)
    if not user:
        return RedirectResponse(url="/login")
    profile_info = ProfileService()
    profile_details = profile_info.get_profile(user.user.id)
    posts_service = PostServices()
    posts = posts_service.reterive_posts() or []
    profile_service = ProfileService()
    for post in posts:
        user_profile = profile_service.get_profile(post['user_id'])
        if user_profile and len(user_profile) > 0:
            profile = user_profile[0]
            post['author_first_name'] = profile.get('first_name', 'Unknown')
            post['author_last_name'] = profile.get('last_name', '')
            post['author_role'] = profile.get('role', 'Alumni')
        else:
            post['author_first_name'] = 'Unknown'
            post['author_last_name'] = ''
            post['author_role'] = 'Alumni'
    if profile_details:
        profile_dict = profile_details[0]
        context = {"request": request, "profile": profile_dict, "posts": posts}
        return templates.TemplateResponse("alumnidashboard.html", context)
    return RedirectResponse(url="/login")

@router.post('/alumnidashboard')
def alumni_dashboard_post(request: Request, title: str = Form(...), description: str = Form(...), image: UploadFile = None):
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
    return RedirectResponse(url="/alumnidashboard", status_code=303)

@router.get('/alumni_mentorhub', name='alumni_mentorship')
def alumni_mentorhub(request:Request,response_class=HTMLResponse):
    user = logged_user(request)
    profile_service = ProfileService()
    # Get all alumni except the current user
    alumni_list = profile_service.get_all_alumni(user.user.id if user else None)
    profile = None
    if user:
        profile_details = profile_service.get_profile(user.user.id)
        if profile_details:
            profile = profile_details[0]
    if not profile:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(
        "alumni_mentorhub.html",
        {"request": request, "alumni_list": alumni_list, "profile": profile}
    )


@router.get('/alumni_profile')
def alumni_profile(request:Request,response_class=HTMLResponse):
    user = logged_user(request)
    profile = None
    if user:
        profile_service = ProfileService()
        profile_details = profile_service.get_profile(user.user.id)
        if profile_details:
            profile = profile_details[0]
    if not profile:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("alumini_profile.html",{"request":request, "profile": profile})

@router.get('/alumni_jobs')
def alumni_jobs(request: Request, response_class=HTMLResponse):
    user = logged_user(request)
    profile = None
    if user:
        profile_service = ProfileService()
        profile_details = profile_service.get_profile(user.user.id)
        if profile_details:
            profile = profile_details[0]
    if not profile:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("alumni_jobs.html", {"request": request, "profile": profile})

@router.get('/alumni_messages', name='alumni_messages')
def alumni_messeages(request: Request):
    user = logged_user(request)
    profile = None
    if user:
        profile_service = ProfileService()
        profile_details = profile_service.get_profile(user.user.id)
        if profile_details:
            profile = profile_details[0]
    if not profile:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("alumni_messeages.html", {"request": request, "profile": profile})

@router.get('/api/conversations')
def get_user_conversations(request: Request):
    user = logged_user(request)
    if not user:
        return []
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
    return enriched

@router.get('/api/messages/{conversation_id}')
def get_conversation_messages(conversation_id: str):

    messages_service = MessagesService()
    messages = messages_service.get_messages(conversation_id)
    return messages

class MessageBody(BaseModel):
    content: str

@router.post('/api/messages/{conversation_id}')
def send_message(request: Request, conversation_id: str, body: MessageBody):
    user = logged_user(request)
    if not user:
        return {"error": "Not authenticated"}
    from ..services.messages_services import MessagesService
    messages_service = MessagesService()
    messages_service.create_message(conversation_id, user.user.id, body.content)
    return {"success": True}

@router.post('/api/mentor-request-message')
def mentor_request_message(request: Request, requester_id: str = Body(...), receiver_id: str = Body(...), description: str = Body(...)):
    conv_service = ConversationsService()
    messages_service = MessagesService()
    mentor_service = MentorshipService()
    conversation_id = conv_service.get_or_create_conversation(requester_id, receiver_id)
    messages_service.create_message(conversation_id, requester_id, description)
    mentor_service.create_mentor_request(requester_id, receiver_id, description)
    return {"success": True, "conversation_id": conversation_id}

@router.post('/api/jobs')
def create_job(request: Request, title: str = Form(...), description: str = Form(...), company: str = Form(...), location: str = Form(...), visible: Optional[str] = Form(None)):
    user = logged_user(request)
    if not user:
        return {"error": "Not authenticated"}
    from ..services.profile_services import ProfileService
    profile_service = ProfileService()
    from ..repositories.alumini_jobs_repository import AluminiJobsRepository
    jobs_repo = AluminiJobsRepository()
    # Convert visible to boolean, default to False if not present
    visible_bool = str(visible).lower() in ['true', '1', 'on', 'yes'] if visible is not None else False
    job_data = {
        "title": title,
        "description": description,
        "company": company,
        "location": location,
        "visible": visible_bool,
        "posted_by": user.user.id
    }
    jobs_repo.create_job(job_data)
    return {"success": True}

@router.get('/api/jobs')
def list_jobs(request: Request):
    user = logged_user(request)
    from ..repositories.alumini_jobs_repository import AluminiJobsRepository
    jobs_repo = AluminiJobsRepository()
    # Get all visible jobs except those posted by the current user
    jobs = jobs_repo.list_visible_jobs(user.user.id if user else None)
    from ..services.profile_services import ProfileService
    profile_service = ProfileService()
    enriched = []
    for job in jobs:
        poster_profile = profile_service.get_profile(job['posted_by'])
        if poster_profile and len(poster_profile) > 0:
            poster = poster_profile[0]
            job['poster_name'] = f"{poster.get('first_name', '')} {poster.get('last_name', '')}".strip()
            job['poster_email'] = poster.get('email', '')
        else:
            job['poster_name'] = job['poster_email'] = ''
        enriched.append(job)
    return enriched

@router.post('/api/jobs/{job_id}/apply')
def apply_job(request: Request, job_id: str, message: str = Body(...)):
    user = logged_user(request)
    if not user:
        return {"error": "Not authenticated"}
    from ..repositories.alumini_jobs_repository import AluminiJobsRepository
    jobs_repo = AluminiJobsRepository()
    job = jobs_repo.get_job(job_id)
    if not job:
        return {"error": "Job not found"}
    alumni_id = job['posted_by']
    conv_service = ConversationsService()
    messages_service = MessagesService()
    conversation_id = conv_service.get_or_create_conversation(user.user.id, alumni_id)
    job_info = f"Job Application for: {job.get('title', 'N/A')} at {job.get('company', 'N/A')} ({job.get('location', 'N/A')})\n\n{message}"
    messages_service.create_message(conversation_id, user.user.id, job_info)
    return {"success": True, "conversation_id": conversation_id}

@router.post('/api/profile/update')
def update_profile(request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    headline: str = Form(None),
    bio: str = Form(None),
    skills: str = Form(None),
    experience: str = Form(None),
):
    user = logged_user(request)
    if not user:
        return {"error": "Not authenticated"}
    profile_service = ProfileService()
    # Fetch the current profile to get the role
    current_profile = profile_service.get_profile(user.user.id)
    role = current_profile[0].get("role") if current_profile and len(current_profile) > 0 else "alumni"
    profile_data = {
        "id": user.user.id,
        "first_name": first_name,
        "last_name": last_name,
        "headline": headline,
        "bio": bio,
        "skills": [s.strip() for s in skills.split(',')] if skills else [],
        "experience": experience,
        "role": role,
    }
    result = profile_service.create_user_profile(profile_data)
    return {"success": bool(result)}
     
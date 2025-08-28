# Student System Documentation

This document provides comprehensive documentation for the student system in the Minixy platform. The student system enables students to connect with alumni through mentorship, job opportunities, and community interactions.

## Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [System Architecture](#system-architecture)
4. [Components](#components)
   - [Student Dashboard](#student-dashboard)
   - [Mentorship Hub](#mentorship-hub)
   - [Job Opportunities](#job-opportunities)
   - [Messaging System](#messaging-system)
   - [Profile Management](#profile-management)
5. [JavaScript Components](#javascript-components)
6. [API Endpoints](#api-endpoints)
7. [Security Features](#security-features)
8. [UI/UX Design](#uiux-design)

## Overview

The student system is designed to provide students with tools to connect with alumni, find mentorship opportunities, explore job listings, and build their professional network. It follows a modern web architecture with a responsive frontend and RESTful backend API.

## Key Features

### 1. Community Feed
- View posts from alumni and other students
- Like and comment on posts
- Create and share own posts
- Search and filter content

### 2. Mentorship Hub
- Search for available mentors
- View mentor profiles
- Send mentorship requests
- Manage mentorship relationships

### 3. Job Opportunities
- Browse job listings posted by alumni
- Apply to positions with cover letters
- View job details and requirements

### 4. Messaging System
- Communicate with mentors and alumni
- Real-time messaging interface
- Conversation history management

### 5. Profile Management
- Personal information management
- Skill and project showcasing
- Profile customization

## System Architecture

The student system follows a layered architecture pattern:

```
┌─────────────────┐
│   Frontend      │ (HTML Templates, JavaScript, TailwindCSS)
├─────────────────┤
│   Controllers   │ (Request/Response Handling)
├─────────────────┤
│   Services      │ (Business Logic)
├─────────────────┤
│  Repositories   │ (Data Access Layer)
├─────────────────┤
│   Database      │ (Supabase PostgreSQL)
└─────────────────┘
```

### Technology Stack
- **Frontend**: HTML, TailwindCSS, JavaScript (ES6+), Font Awesome
- **Backend**: Python FastAPI
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth with JWT
- **Templating**: Jinja2

## Components

### Student Dashboard

The student dashboard serves as the central hub for community interactions.

#### Features
- Social feed displaying posts from alumni and other students
- Ability to create new posts
- Like and comment functionality
- Search and filtering capabilities
- Responsive design for all device sizes

#### JavaScript Functionality
```javascript
// Post creation with image upload
const postForm = document.getElementById('post-form');
postForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(postForm);
    
    try {
        const response = await fetch('/api/student/posts', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            location.reload(); // Refresh to show new post
        } else {
            alert(result.error || 'Failed to create post');
        }
    } catch (error) {
        console.error('Error creating post:', error);
        alert('Failed to create post');
    }
});

// Like functionality with immediate UI feedback
document.querySelectorAll('.like-btn').forEach(btn => {
    btn.addEventListener('click', async function() {
        const postId = this.dataset.postId;
        const isLiked = this.classList.contains('liked');
        
        try {
            const response = await fetch(`/api/student/posts/${postId}/like`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ liked: !isLiked })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Update UI immediately
                this.classList.toggle('liked', !isLiked);
                const countSpan = this.querySelector('.likes-count');
                countSpan.textContent = `(${result.likes_count})`;
            } else {
                alert(result.error || 'Failed to update like');
            }
        } catch (error) {
            console.error('Error updating like:', error);
            alert('Failed to update like');
        }
    });
});
```

### Mentorship Hub

The mentorship hub connects students with alumni mentors.

#### Features
- Search for mentors by expertise and skills
- View detailed mentor profiles
- Send mentorship requests with personalized messages
- Manage mentorship relationships

#### JavaScript Functionality
```javascript
// Mentor request modal
const modal = document.getElementById('request-modal');
const requestForm = document.getElementById('request-form');

requestForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(requestForm);
    const data = {
        requester_id: "{{ profile.id }}",
        receiver_id: formData.get('receiver_id'),
        description: formData.get('description'),
    };

    try {
        const response = await fetch('/api/student/mentor-request-message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        successMessage.classList.remove('hidden');
        setTimeout(closeModal, 2000);

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to send request. Please try again.');
    }
});

// Profile modal for viewing mentor details
const profileModal = document.getElementById('profile-modal');
const profileRequestBtn = document.getElementById('profile-request-btn');

const openProfileModal = (mentorId, mentorName, mentorHeadline, mentorBio, mentorSkills) => {
    // Update profile modal content
    document.getElementById('profile-modal-name').textContent = mentorName;
    document.getElementById('profile-modal-headline').textContent = mentorHeadline;
    document.getElementById('profile-modal-bio').textContent = mentorBio;
    
    // Update avatar with initials
    const nameParts = mentorName.split(' ');
    const initials = nameParts[0][0] + (nameParts[1] ? nameParts[1][0] : '');
    document.getElementById('profile-modal-avatar').src = `https://placehold.co/96x96/7c3aed/ffffff?text=${initials}`;
    
    // Update skills
    const skillsContainer = document.getElementById('profile-modal-skills');
    skillsContainer.innerHTML = '';
    
    if (mentorSkills) {
        const skills = mentorSkills.split(',').filter(skill => skill.trim() !== '');
        skills.forEach(skill => {
            const skillElement = document.createElement('span');
            skillElement.className = 'expertise-tag text-xs font-semibold px-3 py-1 rounded-full';
            skillElement.textContent = skill.trim();
            skillsContainer.appendChild(skillElement);
        });
    }
    
    // Set mentor ID for request button
    profileRequestBtn.onclick = () => {
        closeProfileModal();
        openModal(mentorId, mentorName);
    };
    
    profileModal.classList.add('active');
};
```

### Job Opportunities

The job opportunities section allows students to browse and apply to positions posted by alumni.

#### Features
- Browse job listings with details
- Apply to positions with cover letters
- View job requirements and descriptions
- Search and filter job listings

#### JavaScript Functionality
```javascript
// Load jobs dynamically
async function loadJobs() {
    try {
        const response = await fetch('/api/student/jobs');
        const data = await response.json();
        
        const jobsContainer = document.getElementById('jobs-container');
        
        if (data.jobs && data.jobs.length > 0) {
            jobsContainer.innerHTML = data.jobs.map(job => `
                <div class="job-card bg-white p-6 rounded-xl shadow-sm flex flex-col" data-job-id="${job.id}">
                    <div class="flex items-start justify-between mb-4">
                        <div>
                            <h3 class="font-bold text-gray-900 text-lg">${job.title}</h3>
                            <p class="text-sm text-gray-600">${job.company}</p>
                        </div>
                        <span class="company-tag text-xs font-semibold px-3 py-1 rounded-full">${job.location}</span>
                    </div>
                    <p class="text-sm text-gray-600 leading-relaxed flex-grow mb-4">${job.description}</p>
                    <div class="flex items-center justify-between pt-4 border-t border-gray-100">
                        <div class="text-sm text-gray-500">
                            <i class="fas fa-dollar-sign mr-1"></i>
                            ${job.salary || 'Salary not specified'}
                        </div>
                        <button class="apply-btn btn-primary text-white font-semibold py-2 px-4 rounded-lg text-sm" 
                                data-job-id="${job.id}" 
                                data-job-title="${job.title}" 
                                data-job-company="${job.company}">
                            Apply Now
                        </button>
                    </div>
                </div>
            `).join('');
        } else {
            jobsContainer.innerHTML = `
                <div class="text-center py-12 col-span-full">
                    <i class="fas fa-briefcase text-4xl text-gray-300 mb-4"></i>
                    <h3 class="text-lg font-semibold text-gray-600 mb-2">No jobs available</h3>
                    <p class="text-gray-500">Check back later for new opportunities!</p>
                </div>
            `;
        }
        
        // Add event listeners to apply buttons
        document.querySelectorAll('.apply-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                const jobId = e.target.dataset.jobId;
                const jobTitle = e.target.dataset.jobTitle;
                const jobCompany = e.target.dataset.jobCompany;
                openApplyModal(jobId, jobTitle, jobCompany);
            });
        });
        
    } catch (error) {
        console.error('Error loading jobs:', error);
        document.getElementById('jobs-container').innerHTML = `
            <div class="text-center py-12 col-span-full">
                <i class="fas fa-exclamation-triangle text-4xl text-red-300 mb-4"></i>
                <h3 class="text-lg font-semibold text-gray-600 mb-2">Error loading jobs</h3>
                <p class="text-gray-500">Please try refreshing the page</p>
            </div>
        `;
    }
}

// Apply modal functionality
const applyModal = document.getElementById('apply-modal');
const applyForm = document.getElementById('apply-form');

applyForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(applyForm);
    const jobId = formData.get('job_id');
    const message = formData.get('message');

    try {
        const response = await fetch(`/api/student/jobs/${jobId}/apply`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        applySuccessMessage.classList.remove('hidden');
        setTimeout(closeApplyModal, 2000);

    } catch (error) {
        console.error('Error applying for job:', error);
        alert('Failed to send application. Please try again.');
    }
});
```

### Messaging System

The messaging system enables real-time communication between students and alumni.

#### Features
- Private conversations with mentors and alumni
- Real-time message sending and receiving
- Conversation history management
- Online status indicators

#### JavaScript Functionality
```javascript
// Fetch conversations
async function fetchConversations() {
    try {
        const response = await fetch('/api/student/conversations');
        if (!response.ok) {
            throw new Error('Failed to fetch conversations');
        }
        const data = await response.json();
        const conversations = data.conversations || [];

        conversationsList.innerHTML = '';
        
        if (conversations.length === 0) {
            conversationsList.innerHTML = `
                <div class="text-center py-8">
                    <i class="fas fa-comments text-gray-300 text-2xl mb-2"></i>
                    <p class="text-gray-500">No conversations yet</p>
                    <p class="text-gray-400 text-sm">Start a conversation by requesting mentorship</p>
                </div>
            `;
            return;
        }

        conversations.forEach(conv => {
            const otherUserName = conv.other_user_name || 'Unknown User';
            const nameParts = otherUserName.split(' ');
            const initials = (nameParts[0]?.[0] || '') + (nameParts[1]?.[0] || '');

            const item = document.createElement('div');
            item.className = 'conversation-item flex items-center p-4 cursor-pointer hover:bg-gray-100 transition-colors';
            item.innerHTML = `
                <div class="relative flex-shrink-0">
                    <img src="https://placehold.co/48x48/7c3aed/ffffff?text=${initials}" alt="User Avatar" class="w-12 h-12 rounded-full">
                    <span class="absolute bottom-0 right-0 block h-3 w-3 rounded-full bg-green-500 border-2 border-white"></span>
                </div>
                <div class="ml-4 flex-1 overflow-hidden">
                    <div class="flex justify-between items-baseline">
                        <h4 class="font-semibold text-sm text-gray-800 truncate">${otherUserName}</h4>
                        <p class="text-xs text-gray-400 flex-shrink-0 ml-2">${conv.other_user_email || ''}</p>
                    </div>
                    <p class="text-xs text-gray-500 truncate mt-1">Click to view messages</p>
                </div>
            `;

            item.onclick = () => loadMessages(conv.id, otherUserName, initials, conv.other_user_email);
            conversationsList.appendChild(item);
        });
    } catch (error) {
        console.error('Error fetching conversations:', error);
        conversationsList.innerHTML = `
            <div class="text-center py-8">
                <i class="fas fa-exclamation-triangle text-red-300 text-2xl mb-2"></i>
                <p class="text-gray-500">Error loading conversations</p>
                <p class="text-gray-400 text-sm">Please try refreshing the page</p>
            </div>
        `;
    }
}

// Load messages for a conversation
async function loadMessages(conversationId, otherUserName, initials, otherUserEmail) {
    try {
        chatWelcomeView.classList.add('hidden');
        chatView.classList.remove('hidden');
        chatView.classList.add('flex');
        currentConversationId = conversationId;
        chatHeader.textContent = otherUserName;
        chatStatus.textContent = otherUserEmail || 'Online';
        chatAvatar.src = `https://placehold.co/40x40/7c3aed/ffffff?text=${initials}`;

        // Update active conversation
        document.querySelectorAll('.conversation-item.active').forEach(el => el.classList.remove('active'));
        const allConvs = Array.from(conversationsList.children);
        const activeConvIndex = allConvs.findIndex(child => child.onclick.toString().includes(`'${conversationId}'`));
        if (activeConvIndex > -1) {
            allConvs[activeConvIndex].classList.add('active');
        }

        // Fetch messages
        const response = await fetch(`/api/student/messages/${conversationId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch messages');
        }
        const data = await response.json();
        const messages = data.messages || [];

        messagesList.innerHTML = '';
        messages.forEach(msg => {
            appendMessage(msg.content, msg.sender_id === currentUserId ? 'sent' : 'received');
        });
        messagesList.scrollTop = messagesList.scrollHeight;
    } catch (error) {
        console.error('Error loading messages:', error);
        messagesList.innerHTML = `
            <div class="text-center py-8">
                <i class="fas fa-exclamation-triangle text-red-300 text-2xl mb-2"></i>
                <p class="text-gray-500">Error loading messages</p>
            </div>
        `;
    }
}

// Send message
sendMessageForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const content = messageInput.value.trim();
    if (!content || !currentConversationId) return;

    try {
        const response = await fetch(`/api/student/messages/${currentConversationId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: content })
        });

        if (!response.ok) {
            throw new Error('Failed to send message');
        }

        const data = await response.json();
        appendMessage(content, 'sent');
        messagesList.scrollTop = messagesList.scrollHeight;
        messageInput.value = '';
    } catch (error) {
        console.error('Error sending message:', error);
        alert('Failed to send message. Please try again.');
    }
});
```

### Profile Management

The profile management system allows students to showcase their skills and projects.

#### Features
- Personal information management
- Bio and headline customization
- Skills and project showcasing
- Profile picture management

#### JavaScript Functionality
```javascript
// Edit profile modal
const editProfileModal = document.getElementById('editProfileModal');
const editProfileForm = document.getElementById('editProfileForm');

editProfileForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(editProfileForm);

    try {
        const response = await fetch('/api/student/profile/update', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to update profile');
        }

        const result = await response.json();
        
        if (result.success) {
            alert('Profile updated successfully!');
            closeModal();
            // Reload the page to show updated data
            location.reload();
        } else {
            alert('Error updating profile: ' + (result.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error updating profile:', error);
        alert('Failed to update profile. Please try again.');
    }
});
```

## JavaScript Components

The student system uses JavaScript extensively to create a dynamic, responsive user experience:

### DOM Manipulation
- Dynamic content loading without page refreshes
- Real-time UI updates for user interactions
- Form validation and submission handling

### API Integration
- RESTful API calls using fetch API
- Async/await for handling asynchronous operations
- Error handling and user feedback

### UI Components
- Modal dialogs for forms and information display
- Dynamic search and filtering
- Real-time messaging interface
- Interactive elements with visual feedback

### Event Handling
- Event delegation for efficient event management
- Keyboard navigation support
- Responsive design adjustments

## API Endpoints

The student system interacts with the following API endpoints:

### Authentication
- `POST /api/student/login` - Student login
- `POST /api/student/logout` - Student logout

### Posts
- `GET /api/student/posts` - Get community posts
- `POST /api/student/posts` - Create new post
- `POST /api/student/posts/{id}/like` - Like/unlike a post
- `POST /api/student/posts/{id}/comment` - Add comment to post

### Mentorship
- `GET /api/student/mentors` - Get available mentors
- `POST /api/student/mentor-request-message` - Send mentorship request

### Jobs
- `GET /api/student/jobs` - Get job listings
- `POST /api/student/jobs/{id}/apply` - Apply to job

### Messaging
- `GET /api/student/conversations` - Get user conversations
- `GET /api/student/messages/{conversation_id}` - Get conversation messages
- `POST /api/student/messages/{conversation_id}` - Send message

### Profile
- `GET /api/student/profile` - Get student profile
- `POST /api/student/profile/update` - Update student profile

## Security Features

### Authentication
- JWT-based session management
- Role-based access control (Student role)
- Protected routes and API endpoints

### Data Protection
- Input validation and sanitization
- Secure API communication
- Proper error handling without exposing sensitive information

### Authorization
- Students can only edit their own profile
- Students can only delete their own posts
- Access control to mentorship features

## UI/UX Design

### Responsive Design
- Mobile-first approach
- Flexible grid layouts
- Touch-friendly interface elements
- Adaptive components for different screen sizes

### Visual Design
- Consistent color scheme and typography
- Smooth animations and transitions
- Clear visual hierarchy
- Intuitive navigation patterns

### Accessibility
- Semantic HTML structure
- Keyboard navigation support
- Proper contrast ratios
- Screen reader compatibility

### Performance Optimization
- Lazy loading for content
- Efficient event handling
- Minimal DOM manipulation
- Optimized asset loading

## Conclusion

The student system provides a comprehensive platform for students to connect with alumni, find mentorship opportunities, explore job listings, and build their professional network. With its modern architecture, responsive design, and rich feature set, it offers an engaging and productive experience for student users.
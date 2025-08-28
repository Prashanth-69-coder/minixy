# Alumni System JavaScript Components Documentation

This document provides a comprehensive overview of all JavaScript components used in the alumni system. The JavaScript code enhances user experience by providing dynamic interactions, real-time updates, and seamless navigation without page reloads.

## Table of Contents
1. [Overview](#overview)
2. [Alumni Dashboard JavaScript](#alumni-dashboard-javascript)
   - [Post Management](#post-management)
   - [Social Interactions](#social-interactions)
   - [Search and Filtering](#search-and-filtering)
   - [Post Editing and Deletion](#post-editing-and-deletion)
3. [Mentorship Hub JavaScript](#mentorship-hub-javascript)
   - [Mentor Request Management](#mentor-request-management)
   - [Mentor Search and Discovery](#mentor-search-and-discovery)
   - [Profile Viewing](#profile-viewing)
4. [Job Referrals JavaScript](#job-referrals-javascript)
   - [Job Posting](#job-posting)
   - [Job Visibility Management](#job-visibility-management)
   - [Job Application](#job-application)
5. [Messaging System JavaScript](#messaging-system-javascript)
   - [Conversation Management](#conversation-management)
   - [Real-time Messaging](#real-time-messaging)
6. [Profile Management JavaScript](#profile-management-javascript)
7. [Common JavaScript Patterns](#common-javascript-patterns)
   - [Modal Management](#modal-management)
   - [API Integration](#api-integration)
   - [Error Handling](#error-handling)
8. [UI/UX Enhancements](#uiux-enhancements)

## Overview

The alumni system uses JavaScript extensively to create a dynamic, responsive user experience. All JavaScript code follows modern best practices including:

- Asynchronous operations using `async/await`
- Event delegation for efficient event handling
- DOM manipulation for dynamic content updates
- RESTful API integration
- Responsive design considerations
- Loading states and user feedback

## Alumni Dashboard JavaScript

### Post Management

The dashboard allows alumni to create and manage posts with rich interactions:

```javascript
// Create new post with image upload
const postForm = document.getElementById('post-form');
postForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(postForm);
    
    try {
        const response = await fetch('/api/posts', {
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
```

### Social Interactions

Users can like posts and add comments with real-time updates:

```javascript
// Like functionality with immediate UI feedback
document.querySelectorAll('.like-btn').forEach(btn => {
    btn.addEventListener('click', async function() {
        const postId = this.dataset.postId;
        const isLiked = this.classList.contains('liked');
        
        try {
            const response = await fetch(`/api/posts/${postId}/like`, {
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

// Comment functionality with dynamic loading
document.querySelectorAll('.comment-form').forEach(form => {
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const postId = this.dataset.postId;
        const formData = new FormData(this);
        
        try {
            const response = await fetch(`/api/posts/${postId}/comment`, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Clear form and update comments
                this.reset();
                const commentBtn = document.querySelector(`[data-post-id="${postId}"].comment-btn`);
                const countSpan = commentBtn.querySelector('.comments-count');
                countSpan.textContent = `(${result.comments_count})`;
                
                // Reload comments
                loadComments(postId);
            } else {
                alert(result.error || 'Failed to add comment');
            }
        } catch (error) {
            console.error('Error adding comment:', error);
            alert('Failed to add comment');
        }
    });
});
```

### Search and Filtering

Dynamic search and filtering capabilities:

```javascript
// Search functionality
const searchInput = document.getElementById('search-input');
const roleFilter = document.getElementById('role-filter');

searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        performSearch();
    }
});

roleFilter.addEventListener('change', function() {
    performSearch();
});

function performSearch() {
    const searchTerm = searchInput.value.trim();
    const roleValue = roleFilter.value;
    const currentUrl = new URL(window.location);
    
    if (searchTerm) {
        currentUrl.searchParams.set('search', searchTerm);
    } else {
        currentUrl.searchParams.delete('search');
    }
    
    if (roleValue) {
        currentUrl.searchParams.set('role_filter', roleValue);
    } else {
        currentUrl.searchParams.delete('role_filter');
    }
    
    window.location.href = currentUrl.toString();
}
```

### Post Editing and Deletion

Users can edit or delete their own posts:

```javascript
// Post editing functionality
const editModal = document.getElementById('edit-modal');
const editForm = document.getElementById('edit-post-form');

document.querySelectorAll('.edit-post-btn').forEach(btn => {
    btn.addEventListener('click', async function() {
        const postId = this.dataset.postId;
        
        try {
            const response = await fetch(`/api/posts/${postId}`);
            const result = await response.json();
            
            if (result.success && result.post.is_owner) {
                editPostId.value = postId;
                editTitle.value = result.post.title;
                editDescription.value = result.post.description;
                editModal.classList.remove('hidden');
            } else {
                alert('You can only edit your own posts');
            }
        } catch (error) {
            console.error('Error loading post:', error);
            alert('Failed to load post');
        }
    });
});

// Post deletion functionality
document.querySelectorAll('.delete-post-btn').forEach(btn => {
    btn.addEventListener('click', async function() {
        const postId = this.dataset.postId;
        
        if (confirm('Are you sure you want to delete this post?')) {
            try {
                const response = await fetch(`/api/posts/${postId}`, {
                    method: 'DELETE'
                });
                
                const result = await response.json();
                
                if (result.success) {
                    location.reload(); // Refresh to remove deleted post
                } else {
                    alert(result.error || 'Failed to delete post');
                }
            } catch (error) {
                console.error('Error deleting post:', error);
                alert('Failed to delete post');
            }
        }
    });
});
```

## Mentorship Hub JavaScript

### Mentor Request Management

Alumni can manage mentorship requests they receive:

```javascript
// Accept mentor request
async function acceptRequest(requestId) {
    try {
        const response = await fetch(`/api/mentorship/requests/${requestId}/accept`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Update UI to reflect acceptance
            const requestElement = document.querySelector(`[data-request-id="${requestId}"]`);
            requestElement.innerHTML = `
                <div class="flex items-center justify-between p-4 bg-green-50 rounded-lg">
                    <div class="flex items-center">
                        <i class="fas fa-check-circle text-green-500 mr-3"></i>
                        <span>Request accepted</span>
                    </div>
                </div>
            `;
            loadStatistics(); // Refresh statistics
        } else {
            showNotification('Failed to accept request', 'error');
        }
    } catch (error) {
        console.error('Error accepting request:', error);
        showNotification('Failed to accept request', 'error');
    }
}

// Decline mentor request
async function declineRequest(requestId) {
    if (!confirm('Are you sure you want to decline this request?')) return;
    
    try {
        const response = await fetch(`/api/mentorship/requests/${requestId}/decline`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Remove request from list
            const requestElement = document.querySelector(`[data-request-id="${requestId}"]`);
            requestElement.remove();
            loadStatistics(); // Refresh statistics
        } else {
            showNotification('Failed to decline request', 'error');
        }
    } catch (error) {
        console.error('Error rejecting request:', error);
        showNotification('Failed to decline request', 'error');
    }
}
```

### Mentor Search and Discovery

Dynamic mentor search with filtering capabilities:

```javascript
// Search functionality
const searchBtn = document.getElementById('search-btn');
const searchInput = document.getElementById('search-input');
const expertiseSelect = document.getElementById('expertise-select');

searchBtn.addEventListener('click', performSearch);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') performSearch();
});

async function performSearch() {
    const searchQuery = searchInput.value.trim();
    const expertise = expertiseSelect.value === 'All Expertise' ? null : expertiseSelect.value;
    
    try {
        const params = new URLSearchParams();
        if (searchQuery) params.append('search', searchQuery);
        if (expertise) params.append('expertise', expertise);
        
        const response = await fetch(`/api/mentorship/available-mentors?${params}`);
        if (response.ok) {
            const data = await response.json();
            displaySearchResults(data.mentors);
        }
    } catch (error) {
        console.error('Error searching mentors:', error);
    }
}

function displaySearchResults(mentors) {
    if (mentors.length === 0) {
        mentorsGrid.innerHTML = `
            <div class="col-span-full text-center py-12">
                <i class="fas fa-search text-4xl text-gray-300 mb-4"></i>
                <h3 class="text-lg font-semibold text-gray-600 mb-2">No mentors found</h3>
                <p class="text-gray-500">Try adjusting your search criteria.</p>
            </div>`;
        return;
    }

    mentorsGrid.innerHTML = mentors.map(mentor => `
        <div class="mentor-card bg-white p-6 rounded-xl shadow-sm flex flex-col" 
             data-mentor-id="${mentor.user_id}" 
             data-mentor-name="${mentor.first_name} ${mentor.last_name}">
            <div class="flex items-center mb-4">
                <img src="https://placehold.co/56x56/7c3aed/ffffff?text=${mentor.first_name[0]}${mentor.last_name[0] || ''}" 
                     alt="Avatar" class="w-14 h-14 rounded-full flex-shrink-0">
                <div class="ml-4">
                    <h3 class="font-bold text-gray-900">${mentor.first_name} ${mentor.last_name}</h3>
                    <p class="text-sm text-gray-600">${mentor.headline || 'Alumni'}</p>
                </div>
            </div>
            <p class="text-sm text-gray-600 leading-relaxed flex-grow">
                ${mentor.bio ? (mentor.bio.length > 120 ? mentor.bio.substring(0, 120) + '...' : mentor.bio) : 'No bio available.'}
            </p>
            <div class="flex flex-wrap gap-2 my-4">
                ${(mentor.skills || []).slice(0, 3).map(skill => 
                    `<span class="expertise-tag text-xs font-semibold px-3 py-1 rounded-full">${skill}</span>`
                ).join('')}
            </div>
            <div class="flex space-x-3 mt-auto pt-4 border-t border-gray-100">
                <button class="view-profile-btn w-full text-sm font-semibold text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition py-2">View Profile</button>
                <button class="request-btn w-full btn-primary text-white font-semibold py-2 rounded-lg text-sm">Request</button>
            </div>
        </div>
    `).join('');
    
    // Re-attach event listeners for new elements
    document.querySelectorAll('.request-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const card = e.target.closest('.mentor-card');
            const mentorId = card.dataset.mentorId;
            const mentorName = card.dataset.mentorName;
            openModal(mentorId, mentorName);
        });
    });
}
```

### Profile Viewing

Modal-based profile viewing for mentors:

```javascript
// Profile modal functions
const profileModal = document.getElementById('profile-modal');
const closeProfileModalBtn = document.getElementById('close-profile-modal-btn');
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

const closeProfileModal = () => {
    profileModal.classList.remove('active');
};
```

## Job Referrals JavaScript

### Job Posting

Form handling for job creation:

```javascript
// Modal functionality
const jobModal = document.getElementById('jobModal');
const postJobBtn = document.getElementById('postJobBtn');
const closeModalBtn = document.getElementById('closeModalBtn');
const cancelModalBtn = document.getElementById('cancelModalBtn');
const postJobForm = document.getElementById('post-job-form');

const openModal = () => jobModal.classList.add('active');
const closeModal = () => {
    jobModal.classList.remove('active');
    postJobForm.reset();
};

postJobBtn.addEventListener('click', openModal);
closeModalBtn.addEventListener('click', closeModal);
cancelModalBtn.addEventListener('click', closeModal);

// Handle form submission
postJobForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(postJobForm);
    
    // Show loading state
    const submitButton = postJobForm.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Posting...';
    submitButton.disabled = true;
    
    fetch('/api/jobs', {
        method: 'POST',
        body: formData
    }).then(res => {
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
    }).then(data => {
        if (data.success) {
            closeModal();
            // Refresh the current view
            if (myJobsContainer.classList.contains('hidden')) {
                loadJobs();
            } else {
                loadMyJobs();
            }
            // Show success message
            alert('Job posted successfully!');
        } else {
            alert('Failed to post job: ' + (data.detail || 'Unknown error'));
        }
    }).catch(err => {
        console.error('Error posting job:', err);
        alert('Failed to post job. Please try again.');
    }).finally(() => {
        // Restore button state
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
    });
});
```

### Job Visibility Management

Toggle job visibility for alumni:

```javascript
// Toggle job visibility
function toggleJobVisibility(jobId, visible) {
    // Show a loading indicator
    const buttons = document.querySelectorAll(`.toggle-visibility-btn[data-job-id="${jobId}"]`);
    if (buttons.length > 0) {
        const originalHTML = buttons[0].innerHTML;
        buttons[0].innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        buttons[0].disabled = true;
    }
    
    fetch(`/api/jobs/${jobId}/visibility`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ visible: visible })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(data => {
                throw new Error(data.detail || `Error ${res.status}: Failed to update job visibility`);
            });
        }
        return res.json();
    })
    .then(data => {
        if (data.success) {
            // Reload my jobs to reflect the change
            loadMyJobs();
        } else {
            alert('Failed to update job visibility: ' + (data.detail || 'Unknown error'));
        }
    })
    .catch(err => {
        console.error('Error updating job visibility:', err);
        alert(`Failed to update job visibility: ${err.message}`);
        // Restore buttons
        loadMyJobs();
    });
}
```

### Job Application

Apply for jobs with modal form:

```javascript
// Job application modal
let currentApplyJobId = null;
const applyJobModal = document.getElementById('applyJobModal');
const closeApplyModalBtn = document.getElementById('closeApplyModalBtn');
const cancelApplyModalBtn = document.getElementById('cancelApplyModalBtn');
const applyJobForm = document.getElementById('apply-job-form');
const applySuccessMessage = document.getElementById('apply-success-message');
const applyMessageInput = document.getElementById('apply-message');

function openApplyModal(jobId) {
    currentApplyJobId = jobId;
    applyJobModal.classList.add('active');
    applyJobForm.reset();
    applySuccessMessage.classList.add('hidden');
}

function closeApplyModal() {
    applyJobModal.classList.remove('active');
    applyJobForm.reset();
    applySuccessMessage.classList.add('hidden');
}

applyJobForm.addEventListener('submit', function(e) {
    e.preventDefault();
    if (!currentApplyJobId) return;
    const message = applyMessageInput.value.trim();
    if (!message) return;
    fetch(`/api/jobs/${currentApplyJobId}/apply`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({message: message})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            applySuccessMessage.classList.remove('hidden');
            setTimeout(closeApplyModal, 2000);
        } else {
            alert('Failed to send application.');
        }
    })
    .catch(err => {
        console.error('Error applying for job:', err);
        alert('Failed to send application.');
    });
});
```

## Messaging System JavaScript

### Conversation Management

Load and display conversations:

```javascript
async function fetchConversations() {
    try {
        const response = await fetch('/api/alumni/conversations');
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
            showWelcomeView();
            return;
        }

        conversations.forEach(conv => {
            const otherUserName = conv.other_user_name || conv.other_user_email || 'Unknown User';
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
        showWelcomeView();
    }
}
```

### Real-time Messaging

Send and display messages in real-time:

```javascript
async function loadMessages(conversationId, otherUserName, initials, otherUserEmail) {
    // Immediately show the chat view when a conversation is selected
    showChatView();
    
    // Update conversation state
    currentConversationId = conversationId;
    chatHeader.textContent = otherUserName;
    chatAvatar.src = `https://placehold.co/40x40/7c3aed/ffffff?text=${initials}`;
    
    try {
        // Show loading state
        messagesList.innerHTML = `
            <div class="text-center py-8">
                <i class="fas fa-spinner fa-spin text-gray-400 text-xl"></i>
                <p class="text-gray-500 mt-2">Loading messages...</p>
            </div>
        `;

        // Fetch messages
        const response = await fetch(`/api/alumni/messages/${conversationId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch messages');
        }
        const data = await response.json();
        const messages = data.messages || [];

        // Display messages
        messagesList.innerHTML = '';
        messages.forEach(msg => {
            appendMessage(msg.content, msg.sender_id.toString() === currentUserId.toString() ? 'sent' : 'received');
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

sendMessageForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const content = messageInput.value.trim();
    if (!content || !currentConversationId) return;

    try {
        // Immediately show the message in the UI
        appendMessage(content, 'sent');
        messagesList.scrollTop = messagesList.scrollHeight;
        messageInput.value = '';

        const response = await fetch(`/api/alumni/messages/${currentConversationId}`, {
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
    } catch (error) {
        console.error('Error sending message:', error);
        alert('Failed to send message. Please try again.');
    }
});
```

## Profile Management JavaScript

Edit profile information with modal form:

```javascript
document.addEventListener('DOMContentLoaded', () => {
    const editProfileModal = document.getElementById('editProfileModal');
    const editProfileBtn = document.getElementById('editProfileBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const cancelModalBtn = document.getElementById('cancelModalBtn');
    const editProfileForm = document.getElementById('editProfileForm');

    const openModal = () => {
        // Pre-fill form with current profile data
        document.getElementById('modal-first-name').value = `{{ first_name }}`;
        document.getElementById('modal-last-name').value = `{{ last_name }}`;
        document.getElementById('modal-headline').value = `{{ headline }}`;
        document.getElementById('modal-bio').value = `{{ bio }}`;
        document.getElementById('modal-experience').value = `{{ experience }}`;
        document.getElementById('modal-skills').value = `{{ skills_str }}`;
        document.getElementById('modal-college').value = `{{ college }}`;
        document.getElementById('modal-graduation-year').value = `{{ graduation_year }}`;
        editProfileModal.classList.add('active');
    };

    const closeModal = () => editProfileModal.classList.remove('active');

    // Event listeners for modal
    editProfileBtn.addEventListener('click', openModal);
    closeModalBtn.addEventListener('click', closeModal);
    cancelModalBtn.addEventListener('click', closeModal);
    editProfileModal.addEventListener('click', (e) => {
        if (e.target === editProfileModal) closeModal();
    });

    // Handle form submission
    editProfileForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(editProfileForm);
        fetch('/api/profile/update', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Refresh to show updated profile
            } else {
                alert('Failed to update profile.');
            }
        })
        .catch(error => {
            console.error('Error updating profile:', error);
            alert('An error occurred. Please try again.');
        });
    });
});
```

## Common JavaScript Patterns

### Modal Management

Consistent modal handling across all alumni features:

```javascript
// Generic modal functions
const openModal = (modalElement) => {
    modalElement.classList.add('active');
};

const closeModal = (modalElement) => {
    modalElement.classList.remove('active');
};

// Event delegation for modal closing
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay') && e.target.classList.contains('active')) {
        closeModal(e.target);
    }
});

// Escape key to close modals
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const activeModal = document.querySelector('.modal-overlay.active');
        if (activeModal) {
            closeModal(activeModal);
        }
    }
});
```

### API Integration

Standardized API request handling:

```javascript
// Generic API request function
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`API Error (${url}):`, error);
        throw error;
    }
}

// Usage example
async function loadJobs() {
    try {
        const data = await apiRequest('/api/jobs');
        renderJobs(jobListContainer, data.jobs, false);
    } catch (error) {
        jobListContainer.innerHTML = `
            <div class="text-center py-12">
                <i class="fas fa-exclamation-triangle text-4xl text-red-300 mb-4"></i>
                <h3 class="text-lg font-medium text-gray-900 mb-1">Error loading jobs</h3>
                <p class="text-gray-500">Please try again later.</p>
            </div>
        `;
    }
}
```

### Error Handling

Comprehensive error handling with user feedback:

```javascript
// Notification system for user feedback
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg text-white ${type === 'success' ? 'bg-green-600' : type === 'error' ? 'bg-red-600' : 'bg-blue-600'}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// Error boundary for async operations
async function safeAsyncOperation(operation, successCallback, errorCallback) {
    try {
        const result = await operation();
        if (successCallback) successCallback(result);
        return result;
    } catch (error) {
        console.error('Operation failed:', error);
        if (errorCallback) {
            errorCallback(error);
        } else {
            showNotification('An error occurred. Please try again.', 'error');
        }
        throw error;
    }
}
```

## UI/UX Enhancements

### Loading States

Visual feedback during async operations:

```javascript
// Show loading indicator
function showLoading(element) {
    element.innerHTML = `
        <div class="text-center py-4">
            <i class="fas fa-spinner fa-spin text-gray-400"></i>
            <span class="text-gray-500 ml-2">Loading...</span>
        </div>
    `;
}

// Button loading states
function setButtonLoading(button, loading = true) {
    if (loading) {
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + button.textContent;
    } else {
        button.disabled = false;
        // Restore original text (would need to store it)
    }
}
```

### Responsive Design

JavaScript enhancements for responsive behavior:

```javascript
// Handle responsive navigation
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    mobileMenu.classList.toggle('hidden');
}

// Adjust UI based on screen size
function handleResize() {
    const isMobile = window.innerWidth < 768;
    if (isMobile) {
        // Adjust for mobile
        document.body.classList.add('mobile-view');
    } else {
        // Adjust for desktop
        document.body.classList.remove('mobile-view');
    }
}

window.addEventListener('resize', handleResize);
document.addEventListener('DOMContentLoaded', handleResize);
```

## Conclusion

The alumni system's JavaScript components provide a rich, interactive experience that enhances user engagement and productivity. The code follows modern best practices with:

1. **Modular Design**: Each feature has its own JavaScript components
2. **Asynchronous Operations**: All API calls use async/await for better error handling
3. **User Feedback**: Loading states, success/error messages, and visual indicators
4. **Responsive UI**: Adapts to different screen sizes and devices
5. **Accessibility**: Proper event handling and keyboard navigation support
6. **Performance**: Efficient DOM manipulation and event delegation

This JavaScript implementation ensures a smooth, responsive user experience while maintaining clean, maintainable code.
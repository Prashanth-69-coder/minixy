# Minixy Alumni System

## Overview

The Minixy Alumni System is a comprehensive platform that enables alumni to connect with students, share opportunities, and provide mentorship. This system provides a rich set of features including a social feed, mentorship hub, job referrals, messaging, and profile management.

## Key Features

1. **Alumni Dashboard** - Social feed for sharing updates and connecting with the community
2. **Mentorship Hub** - Connect with students and manage mentorship requests
3. **Job Referrals** - Post job opportunities and apply to positions
4. **Messaging System** - Communicate with other users through private messages
5. **Profile Management** - Maintain and update professional information

## System Architecture

The alumni system follows a layered architecture pattern:

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Templates     │    │   Controllers    │    │    Services      │
│ (HTML templates)│◄──►│(alumini_controller)│◄──►│ (various services)│
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                │                         │
                                ▼                         ▼
                        ┌──────────────────┐    ┌──────────────────┐
                        │  Repositories    │    │   Supabase DB    │
                        │(various repos)   │◄──►│  (Data Storage)  │
                        └──────────────────┘    └──────────────────┘
```

## Component Breakdown

### 1. Alumni Controller (`src/controllers/alumini_controller.py`)

The main controller handling all alumni-related routes and business logic:

- **Dashboard Management**
  - `/alumnidashboard` - Display alumni feed with posts
  - Post creation functionality
  - Post filtering (newest, trending, by role)
  
- **Mentorship Hub**
  - `/alumni_mentorhub` - Access to mentorship features
  - Mentorship request management
  - Mentor discovery and availability toggling
  
- **Job Referrals**
  - `/alumni_jobs` - Job posting and application system
  - Job visibility management
  - Job search and filtering
  
- **Messaging System**
  - `/alumni_messages` - Private messaging interface
  - Conversation management
  - Message sending and retrieval
  
- **Profile Management**
  - `/alumni_profile` - View and edit profile information
  - Profile update functionality

### 2. Services Layer

Multiple services handle specific business logic:

- **Mentorship Service** (`src/services/mentorship_services.py`)
  - Mentorship request creation and management
  - Request acceptance/rejection workflows
  - Mentor availability management
  - Mentorship statistics generation

- **Conversations Service** (`src/services/conversations_services.py`)
  - Conversation creation and retrieval
  - User conversation listing

- **Messages Service** (`src/services/messages_services.py`)
  - Message creation and retrieval

- **Profile Service** (`src/services/profile_services.py`)
  - Profile creation and updates
  - Profile information retrieval

- **Post Service** (`src/services/post_services.py`)
  - Post creation and retrieval
  - Post filtering and search

### 3. Repositories Layer

Data access layer communicating with Supabase:

- **Mentorship Repository** (`src/repositories/mentorship_repository.py`)
  - Mentorship request data operations
  - Mentor availability management
  - Mentorship statistics queries

- **Conversations Repository** (`src/repositories/conversations_repository.py`)
  - Conversation data operations

- **Messages Repository** (`src/repositories/messages_repository.py`)
  - Message data operations

- **Profile Repository** (`src/repositories/profile_repository.py`)
  - Profile data operations

- **Jobs Repository** (`src/repositories/alumini_jobs_repository.py`)
  - Job posting and retrieval
  - Job visibility management

## Detailed Feature Descriptions

### 1. Alumni Dashboard

The alumni dashboard serves as the central hub for social interaction:

**Features:**
- Timeline feed displaying posts from alumni and students
- Post creation with title, description, and image upload
- Post filtering by newest or trending
- Search functionality to find specific posts
- Role-based filtering (students only, alumni only)
- Engagement features (likes, comments)
- Post management (edit/delete for own posts)

**Technical Implementation:**
- Uses PostServices for post retrieval and creation
- Implements filtering logic in the controller
- Supports image uploads through file handling
- Integrates reactions and comments services

### 2. Mentorship Hub

The mentorship hub facilitates connections between alumni and students:

**Features:**
- Mentorship request management (accept/reject)
- Mentor availability toggling
- Mentor discovery with search and filtering
- Mentorship statistics dashboard
- Profile viewing for potential mentors
- Request messaging system

**Technical Implementation:**
- Mentorship requests stored in `mentor_requests` table
- Availability status managed in user profiles
- Advanced search with expertise and name filtering
- Real-time statistics generation
- Integration with notification system

### 3. Job Referrals

The job referral system enables alumni to share opportunities:

**Features:**
- Job posting with title, company, location, and description
- Job visibility control (public/private)
- Job search and filtering by title, company, or location
- Job application through messaging system
- My Jobs section for managing posted positions

**Technical Implementation:**
- Jobs stored in `jobs` table
- Visibility controlled through boolean field
- Advanced search with multiple criteria
- Integration with conversation system for applications

### 4. Messaging System

The messaging system enables private communication:

**Features:**
- Conversation listing with user information
- Real-time message sending and receiving
- Online status indicators
- Conversation history retention

**Technical Implementation:**
- Conversations stored in `conversations` table
- Messages stored in `messages` table
- Automatic conversation creation when first message is sent
- Real-time message retrieval

### 5. Profile Management

Profile management allows alumni to maintain their information:

**Features:**
- Professional information display
- Editable fields (name, headline, bio, experience, skills)
- Profile picture management
- College and graduation year tracking

**Technical Implementation:**
- Profile data stored in `profiles` table
- Skills stored as array field
- Image handling for profile pictures
- Form validation and sanitization

## Authentication and Security

The alumni system implements robust security measures:

- **Role-Based Access Control**: All routes are protected and restricted to alumni users
- **Input Validation**: All form inputs are validated and sanitized
- **Secure Sessions**: Authentication handled through secure JWT tokens
- **Data Protection**: Sensitive data protected through Supabase security rules

## API Endpoints

### Mentorship APIs
- `GET /api/mentorship/requests` - Get mentorship requests for logged-in alumni
- `POST /api/mentorship/requests/{request_id}/accept` - Accept a mentorship request
- `POST /api/mentorship/requests/{request_id}/reject` - Reject a mentorship request
- `POST /api/mentorship/availability` - Toggle mentor availability status
- `GET /api/mentorship/statistics` - Get mentorship statistics
- `GET /api/mentorship/available-mentors` - Get list of available mentors

### Messaging APIs
- `GET /api/alumni/conversations` - Get user conversations
- `GET /api/alumni/messages/{conversation_id}` - Get conversation messages
- `POST /api/alumni/messages/{conversation_id}` - Send a message

### Job APIs
- `POST /api/jobs` - Create a new job posting
- `GET /api/jobs` - List visible jobs with filtering
- `GET /api/my-jobs` - Get jobs posted by current user
- `POST /api/jobs/{job_id}/visibility` - Update job visibility
- `POST /api/jobs/{job_id}/apply` - Apply to a job

### Profile APIs
- `POST /api/profile/update` - Update user profile

## Frontend Implementation

### Technologies Used
- **HTML/TailwindCSS** - For responsive UI design
- **JavaScript** - For interactive components and dynamic content
- **Font Awesome** - For icons and visual elements
- **Jinja2 Templates** - For server-side rendering

### Key UI Components
- **Navigation Sidebar** - Consistent navigation across all alumni pages
- **Modals** - For forms and detailed views (job posting, profile editing, etc.)
- **Cards** - For content display (posts, jobs, mentors)
- **Tabs** - For organizing related content (mentorship requests, discover mentors)
- **Forms** - For data input with validation

## Data Models

### Key Tables in Supabase

1. **profiles** - User profile information
   - id (UUID)
   - first_name (string)
   - last_name (string)
   - headline (string)
   - bio (text)
   - skills (array)
   - experience (text)
   - role (string: alumni/student/admin)
   - mentor_available (boolean)

2. **posts** - Social feed posts
   - id (UUID)
   - user_id (UUID)
   - title (string)
   - description (text)
   - image (string)
   - created_at (timestamp)

3. **mentor_requests** - Mentorship requests
   - id (UUID)
   - requester_id (UUID)
   - receiver_id (UUID)
   - description (text)
   - status (string: pending/accepted/rejected)
   - created_at (timestamp)

4. **jobs** - Job postings
   - id (UUID)
   - title (string)
   - description (text)
   - company (string)
   - location (string)
   - visible (boolean)
   - posted_by (UUID)
   - created_at (timestamp)

5. **conversations** - Message conversations
   - id (UUID)
   - sender_id (UUID)
   - receiver_id (UUID)
   - is_group (boolean)
   - created_at (timestamp)

6. **messages** - Individual messages
   - id (UUID)
   - conversation_id (UUID)
   - sender_id (UUID)
   - content (text)
   - created_at (timestamp)

## Error Handling

The system implements comprehensive error handling:

- **Input Validation**: Client and server-side validation
- **API Error Responses**: Proper HTTP status codes and error messages
- **User Feedback**: Clear error messages for end users
- **Logging**: Error logging for debugging and monitoring

## Performance Considerations

- **Caching**: Comments and other frequently accessed data are cached
- **Pagination**: Large data sets are paginated
- **Efficient Queries**: Database queries optimized with proper indexing
- **Lazy Loading**: Content loaded as needed

## Future Enhancements

Potential areas for future development:

1. **Advanced Analytics**: Detailed usage statistics and insights
2. **Mobile Responsiveness**: Enhanced mobile experience
3. **Search Improvements**: More sophisticated search algorithms
4. **Notification System**: Real-time notifications for various events
5. **File Sharing**: Enhanced file sharing capabilities in messages
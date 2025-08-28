# Minixy Platform Documentation

Welcome to the Minixy platform documentation. This comprehensive guide covers all aspects of the system architecture, components, and how different parts of the system connect to enable meaningful interactions between alumni and students.

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Core Components](#core-components)
4. [User Systems](#user-systems)
5. [Connection Points](#connection-points)
6. [Authentication System](#authentication-system)
7. [Technical Documentation](#technical-documentation)

## Project Overview

Minixy is a comprehensive platform designed to foster connections between alumni and students through mentorship, job opportunities, and communication. The platform provides role-specific experiences while enabling meaningful interactions across user types.

## System Architecture

### High-Level Architecture
![Architecture Diagram](ARCHITECTURE_DIAGRAM.md)

The Minixy platform follows a layered architecture pattern with clear separation of concerns:

- **Client Layer**: Web browsers accessing the application
- **Application Layer**: FastAPI server handling requests
- **Service Layer**: Business logic implementation
- **Data Layer**: Supabase database for data persistence

### Detailed Architecture Documentation
- [Full Architecture Overview](PROJECT_ARCHITECTURE.md)
- [Visual Architecture Diagram](ARCHITECTURE_DIAGRAM.md)
- [System Connections](SYSTEM_CONNECTIONS.md)

## Core Components

### Authentication System
Manages user authentication, session handling, and role-based access control.

Key files:
- [auth_utils.py](src/auth_utils.py) - Core authentication utilities
- [auth_controller.py](src/controllers/auth_controller.py) - Authentication routes
- [auth_services.py](src/services/auth_services.py) - Authentication business logic

### Profile Management
Handles user profile creation, updates, and retrieval.

Key files:
- [profile_controller.py](src/controllers/profile_controller.py) - Profile routes
- [profile_services.py](src/services/profile_services.py) - Profile business logic
- [profile_repository.py](src/repositories/profile_repository.py) - Profile data access

## User Systems

### Alumni System
Provides features specifically for alumni users including mentorship management, job posting, and networking.

Documentation:
- [Alumni README](ALUMNI_README.md)
- [Alumni Architecture](ALUMNI_ARCHITECTURE.md)
- [Alumni JavaScript Usage](ALUMNI_JAVASCRIPT.md)

### Student System
Provides features specifically for student users including mentorship requests, job applications, and learning resources.

Documentation:
- [Student README](STUDENT_README.md)
- [Student Architecture](STUDENT_ARCHITECTURE.md)
- [Student JavaScript Usage](STUDENT_JAVASCRIPT.md)

## Connection Points

The platform enables connections between alumni and students through three primary channels:

### 1. Mentorship System
Enables students to request mentorship from alumni and for alumni to accept or reject these requests.

Detailed documentation:
- [Mentorship Connection Details](SYSTEM_CONNECTIONS.md#2-mentorship-connection-system)

### 2. Job Opportunities
Allows alumni to post job opportunities that students can browse and apply for.

Detailed documentation:
- [Job Connection Details](SYSTEM_CONNECTIONS.md#3-job-opportunity-connection-system)

### 3. Messaging System
Provides real-time messaging capabilities between all users regardless of role.

Detailed documentation:
- [Messaging Connection Details](SYSTEM_CONNECTIONS.md#4-messaging-connection-system)

## Authentication System

The authentication system provides secure user registration, login, and password management:

### Core Features
- User registration with email verification
- Secure login with session management
- Password reset functionality
- Role-based access control (admin, student, alumni)
- JWT token management with automatic refresh

### Password Reset Feature
The platform includes a complete forgot password functionality:
- Users can request password reset via email
- Secure token-based password reset process
- Password strength validation requirements
- Comprehensive error handling

Detailed documentation:
- [Forgot Password Feature Implementation](FORGOT_PASSWORD_FEATURE.md)

## Technical Documentation

### API Endpoints
All API endpoints are protected and role-specific:

1. **Authentication Routes**
   - `/login`, `/signup` - Public authentication endpoints
   - `/dashboard` - Role-specific dashboards
   - `/forgot-password`, `/reset-password` - Password reset endpoints

2. **Profile Routes**
   - `/registration` - Profile creation
   - `/profile` - Profile management

3. **Alumni Routes**
   - `/alumnidashboard` - Alumni social feed
   - `/alumni_mentorhub` - Mentorship management
   - `/alumni_jobs` - Job posting
   - `/alumni_messages` - Messaging

4. **Student Routes**
   - `/studentdashboard` - Student social feed
   - `/studentmentor` - Mentorship requests
   - `/student_job` - Job applications
   - `/student_messages` - Messaging

### Database Schema
The platform uses Supabase with the following key tables:
- `users` - Authentication data (managed by Supabase Auth)
- `profiles` - User profile information
- `posts` - Social media posts
- `jobs` - Job opportunities
- `mentorship_requests` - Mentorship requests
- `mentorships` - Active mentorship relationships
- `conversations` - Messaging conversations
- `messages` - Individual messages
- `notifications` - User notifications

### Security Features
- JWT-based authentication with secure HTTP-only cookies
- Role-based access control
- Input validation and sanitization
- Supabase Row Level Security (RLS) policies
- Automatic token refresh mechanism
- Password strength requirements
- Secure password reset functionality

## Development Guidelines

### Code Structure
```
minixy/
├── src/
│   ├── controllers/     # Route handlers
│   ├── services/        # Business logic
│   ├── repositories/    # Data access layer
│   └── auth_utils.py    # Authentication utilities
├── templates/           # HTML templates
├── static/              # Static assets
├── main.py             # Application entry point
└── README.md           # This file
```

### Adding New Features
1. Create controller in `src/controllers/`
2. Implement business logic in `src/services/`
3. Add data access in `src/repositories/`
4. Create HTML templates in `templates/`
5. Add routes to `main.py`

## Deployment

The application is built with FastAPI and can be deployed using any ASGI-compatible server. Static files are served directly by FastAPI.

Environment variables required:
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase API key

## Contributing

To contribute to the Minixy platform:
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Write appropriate documentation
5. Submit a pull request

## Support

For issues, questions, or feature requests, please open an issue in the repository.
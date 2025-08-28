# How User Interactions Work in Minixy

This document explains how three key user interactions work in the Minixy platform: comments, conversations (messaging), and mentorship requests. These features connect alumni and students in meaningful ways.

## 1. Comments System

Comments allow users to engage with posts in the community feed. Both alumni and students can comment on any post in the system.

### How It Works:
1. **Adding a Comment**:
   - When a user types a comment and submits it, the browser sends a request to the server
   - The system validates the comment content (makes sure it's not empty)
   - The comment is saved to the database with the user ID, post ID, and content
   - The system sends a notification to the post owner about the new comment
   - The comment appears immediately in the comment section

2. **Viewing Comments**:
   - When a user clicks on the "Comment" button for a post, the system loads all comments for that post
   - The system also fetches profile information for each comment author to display names and roles
   - Comments are displayed in chronological order (oldest first)

3. **Technical Flow**:
   ```
   User submits comment → 
   Frontend JavaScript sends request → 
   Controller receives request → 
   CommentsService processes → 
   CommentsRepository saves to database → 
   Notification sent to post owner
   ```

### Key Features:
- Real-time display of new comments
- Author information (name and role) shown with each comment
- Empty comment validation to prevent spam
- Notification system to alert post owners

## 2. Conversations and Messaging System

The messaging system allows direct communication between any users on the platform, including alumni-to-alumni, student-to-student, and alumni-to-student communication.

### How It Works:
1. **Starting a Conversation**:
   - When a user sends their first message to another user, a conversation is automatically created
   - The system checks if a conversation already exists between these two users
   - If not, it creates a new conversation record in the database
   - The message is then saved to the messages table

2. **Sending Messages**:
   - Users type their message in the input field and click send (or press Enter)
   - The message is immediately displayed in the chat window for the sender
   - The message is saved to the database
   - The recipient will see the message when they open the conversation

3. **Viewing Conversations**:
   - Users see a list of all their conversations in the sidebar
   - Each conversation shows the other person's name and email
   - When a user clicks on a conversation, the message history loads
   - New messages appear in real-time as they are sent

4. **Technical Flow**:
   ```
   User sends message → 
   Frontend JavaScript sends request → 
   Controller receives request → 
   ConversationsService checks/creates conversation → 
   MessagesService saves message → 
   MessagesRepository stores in database
   ```

### Key Features:
- Conversation history maintained for all users
- Real-time message display
- Conversation list with participant information
- Works the same way for both alumni and student users

## 3. Mentorship Request System

The mentorship system is the primary way students connect with alumni for guidance and career advice.

### How It Works:
1. **Requesting Mentorship**:
   - Students browse the mentorship hub to find available alumni mentors
   - When a student finds a mentor they want to connect with, they click "Request Mentorship"
   - They write a message explaining why they want mentorship
   - The request is sent to the alumni mentor

2. **Receiving a Request**:
   - Alumni mentors see new requests in their mentorship hub
   - They can view details about the student who sent the request
   - They have the option to accept or reject the request

3. **Accepting a Request**:
   - When an alumni mentor accepts a request, the status changes to "accepted"
   - The student receives a notification that their request was accepted
   - A messaging conversation is automatically enabled between the mentor and student

4. **Rejecting a Request**:
   - If an alumni mentor rejects a request, the status changes to "rejected"
   - The student receives a notification that their request was not accepted
   - The student can still request mentorship from other alumni

5. **Technical Flow**:
   ```
   Student sends request → 
   Frontend JavaScript sends request → 
   Controller receives request → 
   MentorshipService creates request → 
   MentorshipRepository saves to database → 
   Notification sent to alumni mentor
   ```

### Key Features:
- Students can browse and search available mentors
- Alumni can set their availability status (available/unavailable for mentorship)
- Request status tracking (pending, accepted, rejected)
- Integration with messaging system for accepted mentorships
- Notification system for all request activities

## How These Systems Connect Alumni and Students

### Comments:
- Both alumni and students can comment on each other's posts
- Creates a community discussion environment
- Allows for knowledge sharing and feedback

### Conversations:
- Direct messaging between any users
- Enables private communication for deeper discussions
- Works the same for all user types (alumni, student, admin)

### Mentorship Requests:
- Primary connection point between students and alumni
- Formal process for establishing mentor-mentee relationships
- Automatically enables messaging after acceptance

## Database Structure

All these interactions are stored in the Supabase database:

1. **Comments**: Stored in the `comments` table with post_id, user_id, and content
2. **Conversations**: Stored in the `conversations` table with sender_id and receiver_id
3. **Messages**: Stored in the `messages` table with conversation_id, sender_id, and content
4. **Mentorship Requests**: Stored in the `mentor_requests` table with requester_id, receiver_id, and status

## Real-World User Experience

### For Students:
- Comment on posts to participate in discussions
- Message alumni directly after connecting through mentorship
- Request mentorship from alumni to get career guidance
- Receive notifications about comment replies and mentorship updates

### For Alumni:
- Comment on posts to share knowledge and experiences
- Receive mentorship requests from students
- Accept or reject mentorship requests based on availability
- Message students who have been accepted as mentors

This system creates a rich, interconnected community where alumni and students can learn from each other, share experiences, and build meaningful professional relationships.
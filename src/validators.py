import re
import html

class AuthValidator:
    @staticmethod
    def validate_email(email):
        if not email or len(email.strip()) == 0:
            return False, "Email is required"
        
        email = email.strip().lower()
        
        if len(email) > 254:
            return False, "Email is too long"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        return True, None

    @staticmethod
    def validate_password(password):
        if not password:
            return False, ["Password is required"]
        
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        if len(password) > 128:
            errors.append("Password is too long (maximum 128 characters)")
        
        return len(errors) == 0, errors

    @staticmethod
    def validate_name(name, field_name="Name"):
        if not name or len(name.strip()) == 0:
            return False, f"{field_name} is required"
        
        name = name.strip()
        
        if len(name) < 2:
            return False, f"{field_name} must be at least 2 characters long"
        
        if len(name) > 50:
            return False, f"{field_name} is too long (maximum 50 characters)"
        
        if not re.match(r'^[a-zA-Z\s\'-]+$', name):
            return False, f"{field_name} can only contain letters, spaces, hyphens, and apostrophes"
        
        return True, None

    @staticmethod
    def sanitize_input(input_string):
        if not input_string:
            return ""
        
        sanitized = html.escape(input_string.strip())
        
        sanitized = re.sub(r'<script.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        
        return sanitized


class SecurityHelper:
    @staticmethod
    def is_secure_session_token(token):
        if not token or len(token) < 10:
            return False
        
        if any(char in token for char in ['<', '>', '"', "'", '&']):
            return False
        
        return True

    @staticmethod
    def validate_role(role):
        valid_roles = ['student', 'alumni', 'admin']
        
        if not role or role.lower() not in valid_roles:
            return False, f"Invalid role. Must be one of: {', '.join(valid_roles)}"
        
        return True, None
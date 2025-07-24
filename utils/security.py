"""
Security utilities for CodeRoot Bot
Contains functions for hashing, token generation, input sanitization, and admin checks
"""

import re
import hashlib
import secrets
import string
import bcrypt
import logging
from typing import Optional, Union, List, Dict, Any
from datetime import datetime, timedelta

from config import Config

logger = logging.getLogger(__name__)


class Security:
    """Security utility functions"""
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> str:
        """Hash password using bcrypt"""
        try:
            if salt:
                # Use provided salt
                password_bytes = password.encode('utf-8')
                salt_bytes = salt.encode('utf-8')
                hashed = bcrypt.hashpw(password_bytes, salt_bytes)
            else:
                # Generate new salt
                password_bytes = password.encode('utf-8')
                salt_bytes = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password_bytes, salt_bytes)
            
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"Error hashing password: {e}")
            return ""
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            password_bytes = password.encode('utf-8')
            hashed_bytes = hashed.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False
    
    @staticmethod
    def generate_token(length: int = 32, include_special: bool = False) -> str:
        """Generate secure random token"""
        try:
            if include_special:
                chars = string.ascii_letters + string.digits + "!@#$%^&*"
            else:
                chars = string.ascii_letters + string.digits
            
            return ''.join(secrets.choice(chars) for _ in range(length))
        except Exception as e:
            logger.error(f"Error generating token: {e}")
            return ""
    
    @staticmethod
    def generate_api_key(prefix: str = "cr", length: int = 32) -> str:
        """Generate API key with prefix"""
        try:
            random_part = Security.generate_token(length - len(prefix) - 1)
            return f"{prefix}_{random_part}"
        except Exception as e:
            logger.error(f"Error generating API key: {e}")
            return ""
    
    @staticmethod
    def generate_shop_token() -> str:
        """Generate unique token for shop identification"""
        try:
            timestamp = str(int(datetime.utcnow().timestamp()))
            random_part = Security.generate_token(16)
            return f"shop_{timestamp}_{random_part}"
        except Exception as e:
            logger.error(f"Error generating shop token: {e}")
            return ""
    
    @staticmethod
    def generate_referral_code(user_id: int, length: int = 8) -> str:
        """Generate referral code for user"""
        try:
            # Use user_id and timestamp for uniqueness
            base_string = f"{user_id}_{int(datetime.utcnow().timestamp())}"
            hash_object = hashlib.md5(base_string.encode())
            hash_hex = hash_object.hexdigest()
            
            # Take first 'length' characters and convert to uppercase
            code = hash_hex[:length].upper()
            
            # Ensure it starts with letters (replace numbers with letters if needed)
            if code[0].isdigit():
                code = chr(ord('A') + int(code[0])) + code[1:]
            
            return f"CR{code}"
        except Exception as e:
            logger.error(f"Error generating referral code: {e}")
            return Security.generate_token(length)
    
    @staticmethod
    def sanitize_input(text: str, max_length: int = 1000, allow_html: bool = False) -> str:
        """Sanitize user input to prevent injection attacks"""
        if not isinstance(text, str):
            return ""
        
        # Limit length
        text = text[:max_length]
        
        # Remove null bytes and control characters
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        if not allow_html:
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            
            # Remove script tags and their content
            text = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', text, flags=re.IGNORECASE)
            
            # Remove style tags and their content
            text = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', text, flags=re.IGNORECASE)
        
        # Remove dangerous characters for SQL injection prevention
        dangerous_chars = [';', '--', '/*', '*/', 'xp_', 'sp_']
        for char in dangerous_chars:
            text = text.replace(char, '')
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to prevent directory traversal"""
        if not isinstance(filename, str):
            return "unknown"
        
        # Remove path components
        filename = filename.split('/')[-1].split('\\')[-1]
        
        # Remove dangerous characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        
        # Remove dots at the beginning (hidden files)
        filename = filename.lstrip('.')
        
        # Limit length
        filename = filename[:100]
        
        # Ensure it's not empty
        if not filename:
            filename = f"file_{Security.generate_token(8)}"
        
        return filename
    
    @staticmethod
    def validate_bot_token(token: str) -> bool:
        """Validate Telegram bot token format"""
        if not token or not isinstance(token, str):
            return False
        
        # Telegram bot token pattern: number:alphanumeric_string
        pattern = r'^\d+:[A-Za-z0-9_-]{35,}$'
        return bool(re.match(pattern, token))
    
    @staticmethod
    def is_admin(user_id: int) -> bool:
        """Check if user is admin"""
        try:
            return int(user_id) == Config.ADMIN_USER_ID
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_safe_url(url: str) -> bool:
        """Check if URL is safe (no malicious content)"""
        if not url or not isinstance(url, str):
            return False
        
        # Convert to lowercase for checking
        url_lower = url.lower()
        
        # Check for malicious patterns
        malicious_patterns = [
            'javascript:', 'data:', 'vbscript:', 'file:', 'ftp:',
            'mailto:', 'tel:', 'sms:', 'about:', 'chrome:',
            '<script', '</script', 'onerror=', 'onload=',
            'onclick=', 'onmouseover=', 'onfocus='
        ]
        
        for pattern in malicious_patterns:
            if pattern in url_lower:
                return False
        
        # Only allow http and https
        if not (url_lower.startswith('http://') or url_lower.startswith('https://')):
            return False
        
        return True
    
    @staticmethod
    def mask_sensitive_data(data: str, show_chars: int = 4, mask_char: str = "*") -> str:
        """Mask sensitive data for logging/display"""
        if not data or len(data) <= show_chars:
            return data
        
        if show_chars == 0:
            return mask_char * len(data)
        
        visible_start = show_chars // 2
        visible_end = show_chars - visible_start
        masked_length = len(data) - show_chars
        
        if visible_end == 0:
            return data[:visible_start] + mask_char * masked_length
        else:
            return data[:visible_start] + mask_char * masked_length + data[-visible_end:]
    
    @staticmethod
    def generate_csrf_token() -> str:
        """Generate CSRF token for forms"""
        return Security.generate_token(32)
    
    @staticmethod
    def validate_csrf_token(token: str, expected: str) -> bool:
        """Validate CSRF token"""
        if not token or not expected:
            return False
        return secrets.compare_digest(token, expected)
    
    @staticmethod
    def encrypt_data(data: str, key: str) -> str:
        """Simple encryption for non-critical data (placeholder)"""
        # This is a simple XOR encryption - for production use proper encryption
        try:
            if not key:
                return data
            
            encrypted = ""
            key_length = len(key)
            
            for i, char in enumerate(data):
                key_char = key[i % key_length]
                encrypted_char = chr(ord(char) ^ ord(key_char))
                encrypted += encrypted_char
            
            # Base64 encode for safe storage
            import base64
            return base64.b64encode(encrypted.encode()).decode()
        except Exception as e:
            logger.error(f"Error encrypting data: {e}")
            return data
    
    @staticmethod
    def decrypt_data(encrypted_data: str, key: str) -> str:
        """Simple decryption for non-critical data (placeholder)"""
        try:
            if not key or not encrypted_data:
                return encrypted_data
            
            # Base64 decode
            import base64
            encrypted = base64.b64decode(encrypted_data.encode()).decode()
            
            decrypted = ""
            key_length = len(key)
            
            for i, char in enumerate(encrypted):
                key_char = key[i % key_length]
                decrypted_char = chr(ord(char) ^ ord(key_char))
                decrypted += decrypted_char
            
            return decrypted
        except Exception as e:
            logger.error(f"Error decrypting data: {e}")
            return encrypted_data
    
    @staticmethod
    def validate_input_length(text: str, min_length: int = 0, max_length: int = 1000) -> bool:
        """Validate input length"""
        if not isinstance(text, str):
            return False
        
        length = len(text.strip())
        return min_length <= length <= max_length
    
    @staticmethod
    def check_rate_limit(user_id: int, action: str, limit: int, window: int) -> bool:
        """Check if user has exceeded rate limit (placeholder for Redis implementation)"""
        # This would typically use Redis for proper rate limiting
        # For now, always return True (no rate limiting)
        return True
    
    @staticmethod
    def log_security_event(event_type: str, user_id: Optional[int] = None, details: Dict = None):
        """Log security-related events"""
        try:
            log_entry = {
                'timestamp': datetime.utcnow().isoformat(),
                'event_type': event_type,
                'user_id': user_id,
                'details': details or {}
            }
            
            logger.warning(f"Security event: {log_entry}")
            
            # In production, this would also log to a security monitoring system
            
        except Exception as e:
            logger.error(f"Error logging security event: {e}")
    
    @staticmethod
    def validate_permission(user_id: int, permission: str) -> bool:
        """Validate user permissions (placeholder)"""
        # For now, only check admin status
        if permission == 'admin':
            return Security.is_admin(user_id)
        
        # Add more permissions as needed
        return True
    
    @staticmethod
    def clean_phone_number(phone: str) -> str:
        """Clean and format phone number"""
        if not phone:
            return ""
        
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        
        # Remove country code if present
        if digits.startswith('98') and len(digits) == 12:
            digits = '0' + digits[2:]
        elif digits.startswith('0098') and len(digits) == 13:
            digits = '0' + digits[4:]
        
        return digits
    
    @staticmethod
    def validate_iranian_national_id(national_id: str) -> bool:
        """Validate Iranian national ID"""
        if not national_id or not isinstance(national_id, str):
            return False
        
        # Remove any non-digit characters
        national_id = re.sub(r'\D', '', national_id)
        
        # Must be exactly 10 digits
        if len(national_id) != 10:
            return False
        
        # Check if all digits are the same (invalid)
        if len(set(national_id)) == 1:
            return False
        
        # Calculate checksum
        try:
            check_sum = 0
            for i in range(9):
                check_sum += int(national_id[i]) * (10 - i)
            
            remainder = check_sum % 11
            
            if remainder < 2:
                return int(national_id[9]) == remainder
            else:
                return int(national_id[9]) == 11 - remainder
        except:
            return False
    
    @staticmethod
    def generate_session_id() -> str:
        """Generate session ID"""
        return Security.generate_token(64)
    
    @staticmethod
    def validate_session(session_id: str, user_id: int) -> bool:
        """Validate user session (placeholder)"""
        # This would typically check against stored sessions
        # For now, just validate format
        return len(session_id) == 64 and session_id.isalnum()
    
    @staticmethod
    def hash_file_content(content: bytes) -> str:
        """Generate hash of file content for integrity checking"""
        try:
            return hashlib.sha256(content).hexdigest()
        except Exception as e:
            logger.error(f"Error hashing file content: {e}")
            return ""
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
        """Validate file extension against allowed list"""
        if not filename or not allowed_extensions:
            return False
        
        # Get file extension
        extension = filename.lower().split('.')[-1] if '.' in filename else ''
        
        # Check against allowed extensions
        return f".{extension}" in [ext.lower() for ext in allowed_extensions]
    
    @staticmethod
    def escape_sql(text: str) -> str:
        """Escape SQL special characters (basic protection)"""
        if not isinstance(text, str):
            return ""
        
        # Replace single quotes
        text = text.replace("'", "''")
        
        # Remove other dangerous characters
        dangerous = ['--', ';', '/*', '*/', 'xp_', 'sp_']
        for danger in dangerous:
            text = text.replace(danger, '')
        
        return text
    
    @staticmethod
    def generate_otp(length: int = 6) -> str:
        """Generate numeric OTP"""
        try:
            return ''.join(secrets.choice(string.digits) for _ in range(length))
        except Exception as e:
            logger.error(f"Error generating OTP: {e}")
            return ""
    
    @staticmethod
    def validate_otp_format(otp: str, expected_length: int = 6) -> bool:
        """Validate OTP format"""
        if not otp or not isinstance(otp, str):
            return False
        
        return len(otp) == expected_length and otp.isdigit()
    
    @staticmethod
    def secure_compare(a: str, b: str) -> bool:
        """Secure string comparison to prevent timing attacks"""
        try:
            return secrets.compare_digest(str(a), str(b))
        except Exception:
            return False
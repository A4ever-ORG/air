"""
Security utilities for CodeRoot Bot
ابزارهای امنیتی ربات CodeRoot
"""

import hashlib
import secrets
import re
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SecurityUtils:
    """Security utilities class"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate secure random token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate API key"""
        return f"cr_{secrets.token_urlsafe(32)}"
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input"""
        if not text:
            return ""
        
        # Remove dangerous characters
        text = re.sub(r'[<>"\'\\/]', '', text)
        text = text.strip()
        
        return text
    
    @staticmethod
    def is_admin(user_id: int) -> bool:
        """Check if user is admin"""
        from config import Config
        return user_id == Config.ADMIN_USER_ID
    
    @staticmethod
    def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
        """Mask sensitive data for logging"""
        if not data or len(data) <= visible_chars * 2:
            return "*" * len(data) if data else ""
        
        return data[:visible_chars] + "*" * (len(data) - visible_chars * 2) + data[-visible_chars:]
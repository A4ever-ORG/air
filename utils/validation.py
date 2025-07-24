"""
Validation utilities for CodeRoot Bot
ابزارهای اعتبارسنجی ربات CodeRoot
"""

import re
from typing import Optional


class ValidationUtils:
    """Validation utilities class"""
    
    @staticmethod
    def validate_bot_token(token: str) -> bool:
        """Validate Telegram bot token format"""
        if not token or not isinstance(token, str):
            return False
        
        # Telegram bot token pattern: number:alphanumeric_string
        pattern = r'^\d+:[A-Za-z0-9_-]+$'
        return bool(re.match(pattern, token))
    
    @staticmethod
    def validate_shop_name(name: str) -> bool:
        """Validate shop name"""
        if not name or not isinstance(name, str):
            return False
        
        name = name.strip()
        
        # Check length
        if len(name) < 3 or len(name) > 50:
            return False
        
        # Check for valid characters (Persian, English, numbers, spaces)
        pattern = r'^[\u0600-\u06FFa-zA-Z0-9\s]+$'
        return bool(re.match(pattern, name))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate Iranian phone number"""
        if not phone or not isinstance(phone, str):
            return False
        
        phone = phone.strip().replace(' ', '').replace('-', '')
        
        # Iranian mobile number pattern
        pattern = r'^09\d{9}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address"""
        if not email or not isinstance(email, str):
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_card_number(card_number: str) -> bool:
        """Validate Iranian bank card number"""
        if not card_number or not isinstance(card_number, str):
            return False
        
        card_number = card_number.replace(' ', '').replace('-', '')
        
        # 16 digit card number
        if len(card_number) != 16 or not card_number.isdigit():
            return False
        
        return True
    
    @staticmethod
    def validate_product_name(name: str) -> bool:
        """Validate product name"""
        if not name or not isinstance(name, str):
            return False
        
        name = name.strip()
        
        # Check length
        if len(name) < 2 or len(name) > 100:
            return False
        
        # Check for valid characters
        pattern = r'^[\u0600-\u06FFa-zA-Z0-9\s\-_.()]+$'
        return bool(re.match(pattern, name))
    
    @staticmethod
    def validate_price(price) -> bool:
        """Validate product price"""
        try:
            price = float(price)
            return price >= 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_quantity(quantity) -> bool:
        """Validate product quantity"""
        try:
            quantity = int(quantity)
            return quantity >= 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_description(description: str, max_length: int = 500) -> bool:
        """Validate description text"""
        if not description or not isinstance(description, str):
            return False
        
        description = description.strip()
        
        # Check length
        if len(description) > max_length:
            return False
        
        return True
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate Telegram username"""
        if not username or not isinstance(username, str):
            return False
        
        username = username.strip().replace('@', '')
        
        # Telegram username pattern
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]{4,31}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_user_id(user_id) -> bool:
        """Validate Telegram user ID"""
        try:
            user_id = int(user_id)
            return user_id > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_referral_code(code: str) -> bool:
        """Validate referral code format"""
        if not code or not isinstance(code, str):
            return False
        
        code = code.strip().upper()
        
        # 8 character alphanumeric code
        pattern = r'^[A-Z0-9]{8}$'
        return bool(re.match(pattern, code))
    
    @staticmethod
    def validate_order_id(order_id: str) -> bool:
        """Validate order ID format"""
        if not order_id or not isinstance(order_id, str):
            return False
        
        # Order ID pattern: CR + YYYYMMDD + 4 digits
        pattern = r'^CR\d{8}\d{4}$'
        return bool(re.match(pattern, order_id))
    
    @staticmethod
    def validate_payment_amount(amount) -> bool:
        """Validate payment amount"""
        try:
            amount = float(amount)
            return 1000 <= amount <= 100000000  # 1K to 100M Tomans
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_message_text(text: str, max_length: int = 4000) -> bool:
        """Validate message text for broadcasting"""
        if not text or not isinstance(text, str):
            return False
        
        text = text.strip()
        
        # Check length (Telegram message limit is 4096)
        if len(text) > max_length:
            return False
        
        return True
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input"""
        if not text or not isinstance(text, str):
            return ""
        
        # Remove dangerous characters
        text = text.strip()
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    @staticmethod
    def validate_file_size(file_size: int, max_size_mb: int = 20) -> bool:
        """Validate file size"""
        max_size_bytes = max_size_mb * 1024 * 1024
        return 0 < file_size <= max_size_bytes
    
    @staticmethod
    def validate_image_format(file_name: str) -> bool:
        """Validate image file format"""
        if not file_name or not isinstance(file_name, str):
            return False
        
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
        file_extension = file_name.lower().split('.')[-1]
        return f'.{file_extension}' in allowed_extensions
    
    @staticmethod
    def validate_video_format(file_name: str) -> bool:
        """Validate video file format"""
        if not file_name or not isinstance(file_name, str):
            return False
        
        allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}
        file_extension = file_name.lower().split('.')[-1]
        return f'.{file_extension}' in allowed_extensions
    
    @staticmethod
    def validate_document_format(file_name: str) -> bool:
        """Validate document file format"""
        if not file_name or not isinstance(file_name, str):
            return False
        
        allowed_extensions = {'.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls'}
        file_extension = file_name.lower().split('.')[-1]
        return f'.{file_extension}' in allowed_extensions
    
    @staticmethod
    def format_phone_number(phone: str) -> str:
        """Format phone number for display"""
        if not ValidationUtils.validate_phone(phone):
            return phone
        
        phone = phone.strip().replace(' ', '').replace('-', '')
        # Format as: 0912-345-6789
        return f"{phone[:4]}-{phone[4:7]}-{phone[7:]}"
    
    @staticmethod
    def format_card_number(card_number: str) -> str:
        """Format card number for display"""
        if not ValidationUtils.validate_card_number(card_number):
            return card_number
        
        card_number = card_number.replace(' ', '').replace('-', '')
        # Format as: 1234-5678-9012-3456
        return f"{card_number[:4]}-{card_number[4:8]}-{card_number[8:12]}-{card_number[12:]}"
    
    @staticmethod
    def format_price(price: float) -> str:
        """Format price for display"""
        try:
            return f"{int(price):,}"
        except (ValueError, TypeError):
            return "0"
    
    @staticmethod
    def validate_sku(sku: str) -> bool:
        """Validate product SKU"""
        if not sku or not isinstance(sku, str):
            return False
        
        sku = sku.strip().upper()
        
        # SKU pattern: letters, numbers, hyphens, underscores
        pattern = r'^[A-Z0-9_-]{3,20}$'
        return bool(re.match(pattern, sku))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        if not url or not isinstance(url, str):
            return False
        
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def validate_persian_text(text: str) -> bool:
        """Validate Persian text content"""
        if not text or not isinstance(text, str):
            return False
        
        # Check if text contains Persian characters
        persian_pattern = r'[\u0600-\u06FF]'
        return bool(re.search(persian_pattern, text))
    
    @staticmethod
    def clean_markdown(text: str) -> str:
        """Clean text from markdown formatting"""
        if not text or not isinstance(text, str):
            return ""
        
        # Remove markdown formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
        text = re.sub(r'`(.*?)`', r'\1', text)        # Code
        text = re.sub(r'~~(.*?)~~', r'\1', text)      # Strikethrough
        
        return text.strip()
    
    @staticmethod
    def validate_positive_integer(value) -> bool:
        """Validate positive integer"""
        try:
            value = int(value)
            return value > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_non_negative_integer(value) -> bool:
        """Validate non-negative integer"""
        try:
            value = int(value)
            return value >= 0
        except (ValueError, TypeError):
            return False
"""
Validation utilities for CodeRoot Bot
Contains all input validation functions and data format checks
"""

import re
import os
from typing import Optional, Union, List, Dict, Any
from datetime import datetime


class Validation:
    """Static methods for validating various types of inputs and data formats"""
    
    # Regex patterns
    BOT_TOKEN_PATTERN = re.compile(r'^\d+:[A-Za-z0-9_-]{35,}$')
    PHONE_PATTERN = re.compile(r'^(\+98|0098|98|0)?9\d{9}$')
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    CARD_NUMBER_PATTERN = re.compile(r'^\d{4}-?\d{4}-?\d{4}-?\d{4}$')
    USERNAME_PATTERN = re.compile(r'^@?[a-zA-Z0-9_]{5,32}$')
    PERSIAN_TEXT_PATTERN = re.compile(r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\s\d\w\-_.,!?()]*$')
    URL_PATTERN = re.compile(r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$')
    
    @staticmethod
    def validate_bot_token(token: str) -> bool:
        """Validate Telegram bot token format"""
        if not token or not isinstance(token, str):
            return False
        return bool(Validation.BOT_TOKEN_PATTERN.match(token.strip()))
    
    @staticmethod
    def validate_shop_name(name: str) -> bool:
        """Validate shop name"""
        if not name or not isinstance(name, str):
            return False
        
        name = name.strip()
        
        # Length check
        if len(name) < 3 or len(name) > 50:
            return False
        
        # Character check - allow Persian, English, numbers, spaces, and some symbols
        allowed_pattern = re.compile(r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FFa-zA-Z0-9\s\-_.,!()]*$')
        if not allowed_pattern.match(name):
            return False
        
        # Must contain at least one letter or number
        if not re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FFa-zA-Z0-9]', name):
            return False
        
        return True
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate Iranian phone number"""
        if not phone or not isinstance(phone, str):
            return False
        
        # Remove spaces and dashes
        cleaned_phone = re.sub(r'[\s\-]', '', phone.strip())
        
        return bool(Validation.PHONE_PATTERN.match(cleaned_phone))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address"""
        if not email or not isinstance(email, str):
            return False
        
        email = email.strip().lower()
        
        if len(email) > 254:  # RFC 5321 limit
            return False
        
        return bool(Validation.EMAIL_PATTERN.match(email))
    
    @staticmethod
    def validate_card_number(card_number: str) -> bool:
        """Validate Iranian bank card number"""
        if not card_number or not isinstance(card_number, str):
            return False
        
        # Remove spaces and dashes
        cleaned = re.sub(r'[\s\-]', '', card_number.strip())
        
        # Check format
        if not re.match(r'^\d{16}$', cleaned):
            return False
        
        # Check if it's a valid Iranian card (starts with known prefixes)
        iranian_prefixes = [
            '627760', '627761', '627762', '627763', '627764', '627765',  # Post Bank
            '627381', '627382', '627383', '627384', '627385',  # Ansar Bank
            '627593', '627594', '627595', '627596',  # Iran Zamin Bank
            '627648', '627649', '627650',  # Tosee Taavon Bank
            '627412', '627413', '627414',  # Eghtesad Novin Bank
            '627381', '627382',  # Ansar Bank
            '606373', '627760',  # Mehr Iran Bank
            '627593',  # Iran Zamin Bank
            '627760', '627761',  # Post Bank Iran
            '627648',  # Tosee Taavon Bank
            '627412',  # Eghtesad Novin Bank
            '627884',  # Parsian Bank
            '639607',  # Sina Bank
            '627648',  # Tosee Taavon Bank
            '505785',  # Iran Khodro Bank
            '622106',  # Pasargad Bank
            '639348',  # Pasargad Bank
            '627760',  # Post Bank Iran
            '627412',  # Eghtesad Novin Bank
            '639607',  # Sina Bank
            '627381',  # Ansar Bank
        ]
        
        return any(cleaned.startswith(prefix) for prefix in iranian_prefixes)
    
    @staticmethod
    def validate_product_name(name: str) -> bool:
        """Validate product name"""
        if not name or not isinstance(name, str):
            return False
        
        name = name.strip()
        
        # Length check
        if len(name) < 2 or len(name) > 100:
            return False
        
        # Character check
        if not re.match(r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FFa-zA-Z0-9\s\-_.,!()]*$', name):
            return False
        
        return True
    
    @staticmethod
    def validate_price(price: Union[str, int, float]) -> bool:
        """Validate product price"""
        try:
            if isinstance(price, str):
                # Remove commas and convert
                price = float(price.replace(',', ''))
            else:
                price = float(price)
            
            # Price must be positive and reasonable
            return 0 < price <= 1000000000  # Max 1 billion Tomans
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_quantity(quantity: Union[str, int]) -> bool:
        """Validate product quantity"""
        try:
            if isinstance(quantity, str):
                quantity = int(quantity)
            else:
                quantity = int(quantity)
            
            return 0 <= quantity <= 100000  # Max 100k items
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_description(description: str, max_length: int = 1000) -> bool:
        """Validate description text"""
        if not isinstance(description, str):
            return False
        
        description = description.strip()
        
        if len(description) > max_length:
            return False
        
        return True
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate Telegram username"""
        if not username or not isinstance(username, str):
            return False
        
        username = username.strip()
        
        # Remove @ if present
        if username.startswith('@'):
            username = username[1:]
        
        return bool(Validation.USERNAME_PATTERN.match(username))
    
    @staticmethod
    def validate_user_id(user_id: Union[str, int]) -> bool:
        """Validate Telegram user ID"""
        try:
            user_id = int(user_id)
            return 1 <= user_id <= 999999999999  # Telegram ID range
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_referral_code(code: str) -> bool:
        """Validate referral code format"""
        if not code or not isinstance(code, str):
            return False
        
        code = code.strip().upper()
        
        # Should be 6-12 characters, alphanumeric
        return bool(re.match(r'^[A-Z0-9]{6,12}$', code))
    
    @staticmethod
    def validate_order_id(order_id: str) -> bool:
        """Validate order ID format"""
        if not order_id or not isinstance(order_id, str):
            return False
        
        # MongoDB ObjectId format or custom order number
        if re.match(r'^[a-fA-F0-9]{24}$', order_id):  # MongoDB ObjectId
            return True
        
        if re.match(r'^ORD-\d{8}-\d{4}$', order_id):  # Custom format: ORD-20231225-0001
            return True
        
        return False
    
    @staticmethod
    def validate_payment_amount(amount: Union[str, int, float]) -> bool:
        """Validate payment amount"""
        try:
            if isinstance(amount, str):
                amount = float(amount.replace(',', ''))
            else:
                amount = float(amount)
            
            # Must be positive and reasonable for Iranian market
            return 1000 <= amount <= 1000000000  # 1k to 1B Tomans
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_message_text(text: str, max_length: int = 4000) -> bool:
        """Validate message text for Telegram"""
        if not isinstance(text, str):
            return False
        
        text = text.strip()
        
        if len(text) == 0 or len(text) > max_length:
            return False
        
        return True
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input by removing dangerous characters"""
        if not isinstance(text, str):
            return ""
        
        # Remove control characters except newline and tab
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        return sanitized
    
    @staticmethod
    def validate_file_size(file_size: int, max_size_mb: int = 50) -> bool:
        """Validate file size"""
        if not isinstance(file_size, int):
            return False
        
        max_size_bytes = max_size_mb * 1024 * 1024
        return 0 < file_size <= max_size_bytes
    
    @staticmethod
    def validate_image_format(filename: str) -> bool:
        """Validate image file format"""
        if not filename or not isinstance(filename, str):
            return False
        
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
        file_ext = os.path.splitext(filename.lower())[1]
        
        return file_ext in allowed_extensions
    
    @staticmethod
    def validate_video_format(filename: str) -> bool:
        """Validate video file format"""
        if not filename or not isinstance(filename, str):
            return False
        
        allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
        file_ext = os.path.splitext(filename.lower())[1]
        
        return file_ext in allowed_extensions
    
    @staticmethod
    def validate_document_format(filename: str) -> bool:
        """Validate document file format"""
        if not filename or not isinstance(filename, str):
            return False
        
        allowed_extensions = {'.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.csv'}
        file_ext = os.path.splitext(filename.lower())[1]
        
        return file_ext in allowed_extensions
    
    @staticmethod
    def format_phone_number(phone: str) -> str:
        """Format phone number to standard Iranian format"""
        if not Validation.validate_phone(phone):
            return phone
        
        # Remove all non-digits
        digits = re.sub(r'\D', '', phone)
        
        # Convert to 11-digit format starting with 09
        if digits.startswith('98'):
            digits = '0' + digits[2:]
        elif digits.startswith('+98'):
            digits = '0' + digits[3:]
        elif not digits.startswith('09'):
            digits = '09' + digits[-9:]
        
        # Format as 09XX XXX XXXX
        if len(digits) == 11:
            return f"{digits[:4]} {digits[4:7]} {digits[7:]}"
        
        return phone
    
    @staticmethod
    def format_card_number(card_number: str) -> str:
        """Format card number with dashes"""
        if not Validation.validate_card_number(card_number):
            return card_number
        
        # Remove all non-digits
        digits = re.sub(r'\D', '', card_number)
        
        # Format as XXXX-XXXX-XXXX-XXXX
        if len(digits) == 16:
            return f"{digits[:4]}-{digits[4:8]}-{digits[8:12]}-{digits[12:]}"
        
        return card_number
    
    @staticmethod
    def format_price(price: Union[str, int, float]) -> str:
        """Format price with commas and currency"""
        try:
            if isinstance(price, str):
                price = float(price.replace(',', ''))
            
            # Format with commas
            formatted = f"{int(price):,}"
            return f"{formatted} تومان"
        except (ValueError, TypeError):
            return str(price)
    
    @staticmethod
    def validate_sku(sku: str) -> bool:
        """Validate product SKU"""
        if not sku or not isinstance(sku, str):
            return False
        
        sku = sku.strip().upper()
        
        # SKU should be 3-20 characters, alphanumeric with hyphens
        return bool(re.match(r'^[A-Z0-9\-]{3,20}$', sku))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        if not url or not isinstance(url, str):
            return False
        
        url = url.strip()
        
        return bool(Validation.URL_PATTERN.match(url))
    
    @staticmethod
    def validate_persian_text(text: str) -> bool:
        """Validate that text contains Persian characters"""
        if not text or not isinstance(text, str):
            return False
        
        # Check if text contains at least some Persian characters
        persian_chars = re.findall(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]', text)
        return len(persian_chars) > 0
    
    @staticmethod
    def clean_markdown(text: str) -> str:
        """Clean markdown characters that might interfere with Telegram formatting"""
        if not isinstance(text, str):
            return ""
        
        # Escape markdown special characters
        special_chars = ['*', '_', '`', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        
        return text
    
    @staticmethod
    def validate_positive_integer(value: Union[str, int]) -> bool:
        """Validate positive integer"""
        try:
            num = int(value)
            return num > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_non_negative_integer(value: Union[str, int]) -> bool:
        """Validate non-negative integer"""
        try:
            num = int(value)
            return num >= 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_date_string(date_str: str, format_str: str = '%Y-%m-%d') -> bool:
        """Validate date string format"""
        if not date_str or not isinstance(date_str, str):
            return False
        
        try:
            datetime.strptime(date_str, format_str)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_json_structure(data: Any, required_keys: List[str]) -> bool:
        """Validate JSON structure has required keys"""
        if not isinstance(data, dict):
            return False
        
        return all(key in data for key in required_keys)
    
    @staticmethod
    def validate_color_hex(color: str) -> bool:
        """Validate hex color code"""
        if not color or not isinstance(color, str):
            return False
        
        color = color.strip()
        
        # Remove # if present
        if color.startswith('#'):
            color = color[1:]
        
        return bool(re.match(r'^[A-Fa-f0-9]{6}$', color))
    
    @staticmethod
    def validate_language_code(code: str) -> bool:
        """Validate language code (ISO 639-1)"""
        if not code or not isinstance(code, str):
            return False
        
        valid_codes = {'fa', 'en', 'ar', 'de', 'fr', 'es', 'ru', 'tr', 'zh', 'ja', 'ko'}
        return code.lower().strip() in valid_codes
    
    @staticmethod
    def validate_percentage(value: Union[str, int, float]) -> bool:
        """Validate percentage value (0-100)"""
        try:
            if isinstance(value, str):
                value = float(value.replace('%', ''))
            else:
                value = float(value)
            
            return 0 <= value <= 100
        except (ValueError, TypeError):
            return False
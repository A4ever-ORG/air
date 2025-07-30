"""
Bot utility functions for CodeRoot Bot
Contains helper functions for common bot operations, formatting, and Telegram API interactions
"""

import re
import json
import math
import random
import string
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any, Tuple
from pyrogram import Client
from pyrogram.types import Chat, ChatMember
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, FloodWait
import asyncio
import logging

from config import Config

logger = logging.getLogger(__name__)


class BotUtils:
    """Utility functions for bot operations"""
    
    @staticmethod
    async def check_channel_membership(client: Client, user_id: int, channel_username: str) -> bool:
        """Check if user is a member of the specified channel"""
        try:
            # Remove @ if present
            if channel_username.startswith('@'):
                channel_username = channel_username[1:]
            
            # Get chat member
            member = await client.get_chat_member(f"@{channel_username}", user_id)
            
            # Check if user is banned
            if member.status in ["kicked", "banned"]:
                return False
            
            # User is member if status is any valid status except left
            return member.status in ["creator", "administrator", "member", "restricted"]
            
        except UserNotParticipant:
            return False
        except Exception as e:
            logger.error(f"Error checking channel membership: {e}")
            return False
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate Iranian phone number format"""
        if not phone or not isinstance(phone, str):
            return False
        
        # Remove spaces and dashes
        phone = re.sub(r'[\s\-]', '', phone.strip())
        
        # Iranian mobile patterns
        patterns = [
            r'^09\d{9}$',           # 09xxxxxxxxx
            r'^\+989\d{9}$',        # +989xxxxxxxxx
            r'^00989\d{9}$',        # 00989xxxxxxxxx
            r'^989\d{9}$'           # 989xxxxxxxxx
        ]
        
        return any(re.match(pattern, phone) for pattern in patterns)
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """Format phone number to standard display format"""
        if not BotUtils.validate_phone(phone):
            return phone
        
        # Extract digits
        digits = re.sub(r'\D', '', phone)
        
        # Convert to 11-digit format
        if digits.startswith('98') and len(digits) == 12:
            digits = '0' + digits[2:]
        elif digits.startswith('989') and len(digits) == 12:
            digits = '0' + digits[2:]
        elif not digits.startswith('09'):
            digits = '09' + digits[-9:]
        
        # Format as 09XX XXX XXXX
        if len(digits) == 11:
            return f"{digits[:4]} {digits[4:7]} {digits[7:]}"
        
        return phone
    
    @staticmethod
    def format_price(price: Union[str, int, float], currency: str = "تومان") -> str:
        """Format price with thousand separators and currency"""
        try:
            if isinstance(price, str):
                price = float(price.replace(',', ''))
            
            price = int(price)
            formatted = f"{price:,}"
            return f"{formatted} {currency}"
            
        except (ValueError, TypeError):
            return f"0 {currency}"
    
    @staticmethod
    def format_datetime(dt: datetime, format_type: str = "full") -> str:
        """Format datetime for display in Persian/Jalali format"""
        try:
            if format_type == "date":
                return dt.strftime("%Y/%m/%d")
            elif format_type == "time":
                return dt.strftime("%H:%M")
            elif format_type == "short":
                return dt.strftime("%Y/%m/%d %H:%M")
            else:  # full
                return dt.strftime("%Y/%m/%d %H:%M:%S")
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning(f"Date formatting error: {e}")
            return str(dt)
    
    @staticmethod
    def calculate_days_until(target_date: datetime) -> int:
        """Calculate days until target date"""
        try:
            delta = target_date - datetime.utcnow()
            return max(0, delta.days)
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning(f"Date calculation error: {e}")
            return 0
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """Truncate text to specified length with suffix"""
        if not text or len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def escape_markdown(text: str) -> str:
        """Escape markdown special characters for Telegram"""
        if not isinstance(text, str):
            return ""
        
        # Characters that need escaping in MarkdownV2
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        
        return text
    
    @staticmethod
    def clean_html(text: str) -> str:
        """Remove HTML tags from text"""
        if not isinstance(text, str):
            return ""
        
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', text)
        
        # Decode HTML entities
        html_entities = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#39;': "'",
            '&nbsp;': ' '
        }
        
        for entity, char in html_entities.items():
            clean = clean.replace(entity, char)
        
        return clean.strip()
    
    @staticmethod
    def extract_command_args(text: str) -> List[str]:
        """Extract arguments from command text"""
        if not text:
            return []
        
        parts = text.strip().split()
        return parts[1:] if len(parts) > 1 else []
    
    @staticmethod
    def is_valid_telegram_url(url: str) -> bool:
        """Check if URL is a valid Telegram URL"""
        if not url:
            return False
        
        telegram_patterns = [
            r'^https://t\.me/',
            r'^https://telegram\.me/',
            r'^tg://'
        ]
        
        return any(re.match(pattern, url) for pattern in telegram_patterns)
    
    @staticmethod
    async def generate_invite_link(client: Client, chat_id: Union[int, str]) -> Optional[str]:
        """Generate invite link for a chat"""
        try:
            link = await client.export_chat_invite_link(chat_id)
            return link
        except Exception as e:
            logger.error(f"Error generating invite link: {e}")
            return None
    
    @staticmethod
    def parse_callback_data(data: str) -> Dict[str, str]:
        """Parse callback data into components"""
        try:
            if ':' in data:
                parts = data.split(':')
                if len(parts) >= 2:
                    return {
                        'action': parts[0],
                        'param': parts[1],
                        'extra': ':'.join(parts[2:]) if len(parts) > 2 else ''
                    }
            
            return {'action': data, 'param': '', 'extra': ''}
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning(f"Callback data parsing error: {e}")
            return {'action': data, 'param': '', 'extra': ''}
    
    @staticmethod
    def create_callback_data(action: str, param: str = '', extra: str = '') -> str:
        """Create callback data string"""
        parts = [action]
        if param:
            parts.append(param)
        if extra:
            parts.append(extra)
        
        # Telegram callback data limit is 64 bytes
        data = ':'.join(parts)
        return data[:64] if len(data.encode()) > 64 else data
    
    @staticmethod
    def calculate_pagination(total_items: int, page: int, items_per_page: int = 10) -> Dict[str, int]:
        """Calculate pagination parameters"""
        total_pages = math.ceil(total_items / items_per_page) if total_items > 0 else 1
        page = max(1, min(page, total_pages))
        
        start_index = (page - 1) * items_per_page
        end_index = min(start_index + items_per_page, total_items)
        
        return {
            'current_page': page,
            'total_pages': total_pages,
            'items_per_page': items_per_page,
            'start_index': start_index,
            'end_index': end_index,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'total_items': total_items
        }
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        
        return f"{s} {size_names[i]}"
    
    @staticmethod
    def generate_order_number() -> str:
        """Generate unique order number"""
        timestamp = datetime.now().strftime("%Y%m%d")
        random_suffix = ''.join(random.choices(string.digits, k=4))
        return f"ORD-{timestamp}-{random_suffix}"
    
    @staticmethod
    def mask_sensitive_data(data: str, mask_char: str = "*", visible_chars: int = 4) -> str:
        """Mask sensitive data like card numbers, phones"""
        if not data or len(data) <= visible_chars:
            return data
        
        visible_start = visible_chars // 2
        visible_end = visible_chars - visible_start
        masked_length = len(data) - visible_chars
        
        return (
            data[:visible_start] + 
            mask_char * masked_length + 
            data[-visible_end:] if visible_end > 0 else ""
        )
    
    @staticmethod
    def validate_json_structure(data: Any, required_fields: List[str]) -> bool:
        """Validate JSON data structure"""
        if not isinstance(data, dict):
            return False
        
        return all(field in data for field in required_fields)
    
    @staticmethod
    def safe_int(value: Any, default: int = 0) -> int:
        """Safely convert value to integer"""
        try:
            if isinstance(value, str):
                value = value.replace(',', '')
            return int(float(value))
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_float(value: Any, default: float = 0.0) -> float:
        """Safely convert value to float"""
        try:
            if isinstance(value, str):
                value = value.replace(',', '')
            return float(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_str(value: Any, default: str = "") -> str:
        """Safely convert value to string"""
        try:
            if value is None:
                return default
            return str(value)
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning(f"String conversion error: {e}")
            return default
    
    @staticmethod
    async def send_long_message(client: Client, chat_id: Union[int, str], text: str, **kwargs):
        """Send long message by splitting if necessary"""
        max_length = 4000
        
        if len(text) <= max_length:
            return await client.send_message(chat_id, text, **kwargs)
        
        # Split message
        messages = []
        current_pos = 0
        
        while current_pos < len(text):
            end_pos = current_pos + max_length
            
            if end_pos >= len(text):
                chunk = text[current_pos:]
            else:
                # Find last newline or space within limit
                chunk = text[current_pos:end_pos]
                last_newline = chunk.rfind('\n')
                last_space = chunk.rfind(' ')
                
                if last_newline > max_length * 0.8:  # If newline is in last 20%
                    end_pos = current_pos + last_newline
                elif last_space > max_length * 0.8:  # If space is in last 20%
                    end_pos = current_pos + last_space
                
                chunk = text[current_pos:end_pos]
            
            messages.append(chunk.strip())
            current_pos = end_pos
        
        # Send all chunks
        sent_messages = []
        for i, message in enumerate(messages):
            try:
                sent = await client.send_message(chat_id, message, **kwargs)
                sent_messages.append(sent)
                
                # Add delay between messages to avoid flood
                if i < len(messages) - 1:
                    await asyncio.sleep(1)
                    
            except FloodWait as e:
                await asyncio.sleep(e.value)
                sent = await client.send_message(chat_id, message, **kwargs)
                sent_messages.append(sent)
        
        return sent_messages
    
    @staticmethod
    def create_progress_bar(current: int, total: int, length: int = 20) -> str:
        """Create text progress bar"""
        if total == 0:
            return "█" * length
        
        filled = int(length * current / total)
        bar = "█" * filled + "░" * (length - filled)
        percentage = int(100 * current / total)
        
        return f"{bar} {percentage}%"
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """Format duration in seconds to human readable format"""
        if seconds < 60:
            return f"{seconds} ثانیه"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} دقیقه"
        elif seconds < 86400:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours} ساعت و {minutes} دقیقه"
        else:
            days = seconds // 86400
            hours = (seconds % 86400) // 3600
            return f"{days} روز و {hours} ساعت"
    
    @staticmethod
    def generate_random_string(length: int = 8, chars: str = None) -> str:
        """Generate random string"""
        if chars is None:
            chars = string.ascii_uppercase + string.digits
        
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    @staticmethod
    def is_admin_user(user_id: int) -> bool:
        """Check if user is admin"""
        return user_id == Config.ADMIN_USER_ID
    
    @staticmethod
    def get_plan_emoji(plan: str) -> str:
        """Get emoji for subscription plan"""
        plan_emojis = {
            'free': '🆓',
            'professional': '⭐',
            'vip': '👑'
        }
        return plan_emojis.get(plan, '📦')
    
    @staticmethod
    def get_status_emoji(status: str) -> str:
        """Get emoji for status"""
        status_emojis = {
            'active': '✅',
            'inactive': '❌',
            'pending': '⏳',
            'suspended': '⏸',
            'processing': '🔄',
            'completed': '✅',
            'cancelled': '❌',
            'delivered': '📦',
            'shipped': '🚚'
        }
        return status_emojis.get(status, '❓')
    
    @staticmethod
    def create_mention(user_id: int, name: str = None) -> str:
        """Create user mention"""
        if name:
            return f"[{name}](tg://user?id={user_id})"
        return f"[User](tg://user?id={user_id})"
    
    @staticmethod
    async def get_chat_info(client: Client, chat_id: Union[int, str]) -> Optional[Dict]:
        """Get chat information"""
        try:
            chat = await client.get_chat(chat_id)
            return {
                'id': chat.id,
                'type': chat.type,
                'title': getattr(chat, 'title', None),
                'username': getattr(chat, 'username', None),
                'first_name': getattr(chat, 'first_name', None),
                'last_name': getattr(chat, 'last_name', None),
                'member_count': getattr(chat, 'members_count', 0)
            }
        except Exception as e:
            logger.error(f"Error getting chat info: {e}")
            return None
    
    @staticmethod
    def rate_limit_key(user_id: int, action: str) -> str:
        """Generate rate limit key for Redis"""
        return f"rate_limit:{user_id}:{action}"
    
    @staticmethod
    def cache_key(prefix: str, identifier: str) -> str:
        """Generate cache key for Redis"""
        return f"cache:{prefix}:{identifier}"
    
    @staticmethod
    def serialize_user_data(user_data: Dict) -> str:
        """Serialize user data for caching"""
        try:
            # Convert datetime objects to strings
            serializable_data = {}
            for key, value in user_data.items():
                if isinstance(value, datetime):
                    serializable_data[key] = value.isoformat()
                elif key == '_id':
                    serializable_data[key] = str(value)
                else:
                    serializable_data[key] = value
            
            return json.dumps(serializable_data, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error serializing user data: {e}")
            return "{}"
    
    @staticmethod
    def deserialize_user_data(data_str: str) -> Dict:
        """Deserialize user data from cache"""
        try:
            data = json.loads(data_str)
            
            # Convert ISO datetime strings back to datetime objects
            datetime_fields = ['created_at', 'updated_at', 'last_activity']
            for field in datetime_fields:
                if field in data and isinstance(data[field], str):
                    try:
                        data[field] = datetime.fromisoformat(data[field])
                    except (ValueError, TypeError) as e:
                        logger.warning(f"DateTime parsing error for field {field}: {e}")
                        pass
            
            return data
        except Exception as e:
            logger.error(f"Error deserializing user data: {e}")
            return {}
    
    @staticmethod
    def generate_hash(data: str, algorithm: str = 'md5') -> str:
        """Generate hash of data"""
        try:
            if algorithm == 'md5':
                return hashlib.md5(data.encode()).hexdigest()
            elif algorithm == 'sha256':
                return hashlib.sha256(data.encode()).hexdigest()
            elif algorithm == 'sha1':
                return hashlib.sha1(data.encode()).hexdigest()
            else:
                return hashlib.md5(data.encode()).hexdigest()
        except Exception:
            return ""
    
    @staticmethod
    def extract_numbers(text: str) -> List[int]:
        """Extract all numbers from text"""
        try:
            numbers = re.findall(r'\d+', text)
            return [int(num) for num in numbers]
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning(f"Number extraction error: {e}")
            return []
    
    @staticmethod
    def extract_mentions(text: str) -> List[str]:
        """Extract all @mentions from text"""
        try:
            mentions = re.findall(r'@(\w+)', text)
            return mentions
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning(f"Mentions extraction error: {e}")
            return []
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """Extract all #hashtags from text"""
        try:
            hashtags = re.findall(r'#(\w+)', text)
            return hashtags
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning(f"Hashtags extraction error: {e}")
            return []
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for search and comparison"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep Persian characters
        text = re.sub(r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FFa-zA-Z0-9\s]', '', text)
        
        return text.strip()
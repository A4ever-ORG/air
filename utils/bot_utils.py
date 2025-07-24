"""
Bot utility functions for CodeRoot
توابع کمکی ربات CodeRoot
"""

import asyncio
import logging
import re
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from pyrogram import Client
from pyrogram.types import ChatMember
from pyrogram.errors import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired

logger = logging.getLogger(__name__)


class BotUtils:
    """Bot utility functions"""
    
    @staticmethod
    async def check_channel_membership(client: Client, user_id: int, channel_username: str) -> bool:
        """Check if user is member of a channel"""
        try:
            if not channel_username:
                return True
            
            # Remove @ if present
            channel_username = channel_username.replace('@', '')
            
            # Get chat member
            member = await client.get_chat_member(f"@{channel_username}", user_id)
            
            # Check if user is banned
            if member.status in ["banned", "kicked"]:
                return False
            
            # User is member if status is not "left"
            return member.status != "left"
            
        except UserNotParticipant:
            return False
        except UsernameNotOccupied:
            logger.error(f"Channel @{channel_username} does not exist")
            return True  # Allow if channel doesn't exist
        except Exception as e:
            logger.error(f"Error checking membership: {e}")
            return True  # Allow if error occurs
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate Iranian phone number"""
        if not phone:
            return False
        
        # Remove spaces and dashes
        phone = phone.strip().replace(' ', '').replace('-', '')
        
        # Iranian mobile pattern
        pattern = r'^09\d{9}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """Format phone number for display"""
        if not phone:
            return ""
        
        phone = phone.strip().replace(' ', '').replace('-', '')
        if len(phone) == 11 and phone.startswith('09'):
            return f"{phone[:4]}-{phone[4:7]}-{phone[7:]}"
        return phone
    
    @staticmethod
    def format_price(price: float) -> str:
        """Format price for display"""
        try:
            return f"{int(price):,}"
        except (ValueError, TypeError):
            return "0"
    
    @staticmethod
    def format_datetime(dt: datetime, include_time: bool = True) -> str:
        """Format datetime for Persian display"""
        try:
            if include_time:
                return dt.strftime("%Y/%m/%d %H:%M")
            return dt.strftime("%Y/%m/%d")
        except:
            return "نامعلوم"
    
    @staticmethod
    def calculate_days_until(target_date: datetime) -> int:
        """Calculate days until target date"""
        try:
            delta = target_date - datetime.utcnow()
            return max(0, delta.days)
        except:
            return 0
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100) -> str:
        """Truncate text with ellipsis"""
        if not text:
            return ""
        
        if len(text) <= max_length:
            return text
        
        return text[:max_length-3] + "..."
    
    @staticmethod
    def escape_markdown(text: str) -> str:
        """Escape markdown characters"""
        if not text:
            return ""
        
        # Characters that need escaping in Telegram markdown
        chars_to_escape = ['*', '_', '`', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        
        for char in chars_to_escape:
            text = text.replace(char, f'\\{char}')
        
        return text
    
    @staticmethod
    def clean_html(text: str) -> str:
        """Clean HTML tags from text"""
        if not text:
            return ""
        
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)
        return clean_text.strip()
    
    @staticmethod
    def extract_command_args(text: str) -> List[str]:
        """Extract arguments from command text"""
        if not text:
            return []
        
        # Split by spaces and remove empty strings
        args = [arg.strip() for arg in text.split() if arg.strip()]
        
        # Remove the command itself (first element)
        return args[1:] if len(args) > 1 else []
    
    @staticmethod
    def is_valid_telegram_url(url: str) -> bool:
        """Check if URL is a valid Telegram URL"""
        if not url:
            return False
        
        telegram_patterns = [
            r'^https://t\.me/[a-zA-Z][a-zA-Z0-9_]{4,31}$',  # Channel/group
            r'^https://t\.me/joinchat/[a-zA-Z0-9_-]+$',      # Invite link
            r'^@[a-zA-Z][a-zA-Z0-9_]{4,31}$'                 # Username
        ]
        
        return any(re.match(pattern, url) for pattern in telegram_patterns)
    
    @staticmethod
    def generate_invite_link(bot_username: str, referral_code: str) -> str:
        """Generate referral invite link"""
        return f"https://t.me/{bot_username}?start={referral_code}"
    
    @staticmethod
    def parse_callback_data(data: str) -> Dict[str, str]:
        """Parse callback data into components"""
        if not data:
            return {}
        
        if ':' in data:
            parts = data.split(':')
            if len(parts) >= 2:
                return {'action': parts[0], 'value': ':'.join(parts[1:])}
        
        if '_' in data:
            parts = data.split('_', 1)
            if len(parts) >= 2:
                return {'action': parts[0], 'value': parts[1]}
        
        return {'action': data, 'value': ''}
    
    @staticmethod
    def create_callback_data(action: str, value: str = "") -> str:
        """Create callback data from action and value"""
        if value:
            return f"{action}_{value}"
        return action
    
    @staticmethod
    def calculate_pagination(total_items: int, page: int, per_page: int = 10) -> Dict[str, int]:
        """Calculate pagination parameters"""
        total_pages = max(1, (total_items + per_page - 1) // per_page)
        current_page = max(1, min(page, total_pages))
        offset = (current_page - 1) * per_page
        
        return {
            'total_pages': total_pages,
            'current_page': current_page,
            'offset': offset,
            'per_page': per_page,
            'has_previous': current_page > 1,
            'has_next': current_page < total_pages
        }
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    @staticmethod
    def generate_order_number() -> str:
        """Generate unique order number"""
        import random
        import string
        
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M")
        random_part = ''.join(random.choices(string.digits, k=4))
        return f"CR{timestamp}{random_part}"
    
    @staticmethod
    def mask_sensitive_data(data: str, mask_char: str = "*") -> str:
        """Mask sensitive data for logging"""
        if not data or len(data) < 4:
            return mask_char * len(data) if data else ""
        
        visible_chars = 2
        masked_length = len(data) - (visible_chars * 2)
        
        return data[:visible_chars] + (mask_char * masked_length) + data[-visible_chars:]
    
    @staticmethod
    def validate_json_structure(data: Dict, required_fields: List[str]) -> bool:
        """Validate if dictionary has required fields"""
        if not isinstance(data, dict):
            return False
        
        return all(field in data for field in required_fields)
    
    @staticmethod
    def safe_int(value: Any, default: int = 0) -> int:
        """Safely convert value to integer"""
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_float(value: Any, default: float = 0.0) -> float:
        """Safely convert value to float"""
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_str(value: Any, default: str = "") -> str:
        """Safely convert value to string"""
        try:
            return str(value) if value is not None else default
        except:
            return default
    
    @staticmethod
    async def send_long_message(client: Client, chat_id: int, text: str, max_length: int = 4000):
        """Send long message by splitting into multiple messages"""
        if len(text) <= max_length:
            await client.send_message(chat_id, text)
            return
        
        # Split text into chunks
        chunks = []
        current_chunk = ""
        
        for line in text.split('\n'):
            if len(current_chunk) + len(line) + 1 <= max_length:
                current_chunk += line + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Send chunks
        for i, chunk in enumerate(chunks):
            if i > 0:
                await asyncio.sleep(0.5)  # Small delay between messages
            await client.send_message(chat_id, chunk)
    
    @staticmethod
    def create_progress_bar(current: int, total: int, length: int = 20) -> str:
        """Create text progress bar"""
        if total == 0:
            return "▱" * length
        
        filled_length = int(length * current // total)
        bar = "▰" * filled_length + "▱" * (length - filled_length)
        percentage = round(100 * current / total, 1)
        
        return f"{bar} {percentage}%"
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """Format duration in human readable format"""
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
    def generate_random_string(length: int = 8) -> str:
        """Generate random alphanumeric string"""
        import random
        import string
        
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=length))
    
    @staticmethod
    def is_admin_user(user_id: int) -> bool:
        """Check if user is admin"""
        from config import Config
        return user_id == Config.ADMIN_USER_ID
    
    @staticmethod
    def get_plan_emoji(plan: str) -> str:
        """Get emoji for subscription plan"""
        plan_emojis = {
            'free': '🆓',
            'professional': '⭐',
            'vip': '👑'
        }
        return plan_emojis.get(plan, '❓')
    
    @staticmethod
    def get_status_emoji(status: str) -> str:
        """Get emoji for status"""
        status_emojis = {
            'active': '✅',
            'inactive': '❌',
            'pending': '⏳',
            'suspended': '⏸',
            'deleted': '🗑',
            'confirmed': '✅',
            'cancelled': '❌',
            'processing': '⚙️',
            'shipped': '🚚',
            'delivered': '📦'
        }
        return status_emojis.get(status, '❓')
    
    @staticmethod
    def create_mention(user_id: int, name: str) -> str:
        """Create user mention"""
        return f"[{name}](tg://user?id={user_id})"
    
    @staticmethod
    async def get_chat_info(client: Client, chat_id: int) -> Optional[Dict]:
        """Get chat information safely"""
        try:
            chat = await client.get_chat(chat_id)
            return {
                'id': chat.id,
                'type': chat.type,
                'title': getattr(chat, 'title', ''),
                'username': getattr(chat, 'username', ''),
                'description': getattr(chat, 'description', ''),
                'members_count': getattr(chat, 'members_count', 0)
            }
        except Exception as e:
            logger.error(f"Error getting chat info for {chat_id}: {e}")
            return None
    
    @staticmethod
    def rate_limit_key(user_id: int, action: str) -> str:
        """Generate rate limit key"""
        return f"rate_limit:{user_id}:{action}"
    
    @staticmethod
    def cache_key(prefix: str, *args) -> str:
        """Generate cache key"""
        return f"{prefix}:" + ":".join(str(arg) for arg in args)
    
    @staticmethod
    def serialize_user_data(user) -> Dict:
        """Serialize user data for caching"""
        if not user:
            return {}
        
        return {
            'user_id': user.get('user_id'),
            'first_name': user.get('first_name', ''),
            'last_name': user.get('last_name', ''),
            'username': user.get('username', ''),
            'subscription': user.get('subscription', {}),
            'statistics': user.get('statistics', {}),
            'status': user.get('status', 'active')
        }
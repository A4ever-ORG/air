"""
Comprehensive Error Handler for CodeRoot Bot
Provides centralized error handling, logging, and user-friendly error messages
"""

import logging
import traceback
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import (
    FloodWait, UserIsBlocked, UserDeactivated, 
    ChatWriteForbidden, MessageNotModified,
    BadRequest, Unauthorized, Forbidden
)

from config import Config
from utils.language import translator

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Centralized error handling for the bot"""
    
    @staticmethod
    async def handle_pyrogram_error(error: Exception, client: Client, 
                                   message: Optional[Message] = None,
                                   callback_query: Optional[CallbackQuery] = None,
                                   user_lang: str = 'fa') -> bool:
        """
        Handle Pyrogram-specific errors with appropriate user feedback
        
        Returns:
            bool: True if error was handled, False if it needs to be re-raised
        """
        user_id = None
        
        try:
            if message:
                user_id = message.from_user.id
            elif callback_query:
                user_id = callback_query.from_user.id
            
            # Handle FloodWait errors
            if isinstance(error, FloodWait):
                logger.warning(f"FloodWait error: waiting {error.x} seconds")
                await asyncio.sleep(error.x)
                return True
            
            # Handle user-related errors
            elif isinstance(error, (UserIsBlocked, UserDeactivated)):
                logger.info(f"User {user_id} has blocked/deactivated bot")
                return True
            
            # Handle chat permission errors
            elif isinstance(error, ChatWriteForbidden):
                logger.warning(f"Cannot write to chat with user {user_id}")
                return True
            
            # Handle message modification errors
            elif isinstance(error, MessageNotModified):
                logger.debug("Message content was not modified")
                return True
            
            # Handle authorization errors
            elif isinstance(error, (Unauthorized, Forbidden)):
                logger.error(f"Authorization error for user {user_id}: {error}")
                error_msg = translator.get_text('error.permission_denied', user_lang)
                await ErrorHandler._send_error_message(client, message, callback_query, error_msg)
                return True
            
            # Handle bad request errors
            elif isinstance(error, BadRequest):
                logger.error(f"Bad request error for user {user_id}: {error}")
                error_msg = translator.get_text('error.invalid_input', user_lang)
                await ErrorHandler._send_error_message(client, message, callback_query, error_msg)
                return True
            
            # Unhandled Pyrogram error
            else:
                logger.error(f"Unhandled Pyrogram error for user {user_id}: {error}")
                return False
                
        except Exception as e:
            logger.error(f"Error in Pyrogram error handler: {e}")
            return False
    
    @staticmethod
    async def handle_database_error(error: Exception, operation: str, 
                                  user_id: Optional[int] = None) -> None:
        """Handle database-related errors"""
        logger.error(f"Database error in {operation} for user {user_id}: {error}")
        
        # Log detailed error information
        logger.error(f"Database operation failed: {operation}")
        logger.error(f"Error type: {type(error).__name__}")
        logger.error(f"Error details: {str(error)}")
        
        # If critical database error, could trigger alerts here
        if "connection" in str(error).lower():
            logger.critical("Database connection issue detected")
    
    @staticmethod
    async def handle_ai_service_error(error: Exception, user_id: Optional[int] = None,
                                    user_lang: str = 'fa') -> str:
        """Handle AI service errors and return fallback response"""
        logger.error(f"AI service error for user {user_id}: {error}")
        
        # Return appropriate fallback message based on language
        fallback_messages = {
            'fa': "متأسفانه سیستم پشتیبانی هوشمند در حال حاضر در دسترس نیست. لطفاً با پشتیبانی انسانی تماس بگیرید.",
            'en': "Sorry, AI support is currently unavailable. Please contact human support.",
            'ar': "عذراً، الدعم الذكي غير متاح حالياً. يرجى التواصل مع الدعم البشري."
        }
        
        return fallback_messages.get(user_lang, fallback_messages['fa'])
    
    @staticmethod
    async def handle_file_operation_error(error: Exception, operation: str,
                                        user_id: Optional[int] = None) -> None:
        """Handle file operation errors"""
        logger.error(f"File operation error in {operation} for user {user_id}: {error}")
        
        # Log file operation details
        logger.error(f"File operation: {operation}")
        logger.error(f"Error type: {type(error).__name__}")
    
    @staticmethod
    async def handle_external_api_error(error: Exception, service: str,
                                      user_id: Optional[int] = None) -> None:
        """Handle external API errors"""
        logger.error(f"External API error ({service}) for user {user_id}: {error}")
        
        # Could implement retry logic here for certain types of errors
        if "timeout" in str(error).lower():
            logger.warning(f"Timeout error for {service} API")
        elif "rate limit" in str(error).lower():
            logger.warning(f"Rate limit hit for {service} API")
    
    @staticmethod
    async def log_unhandled_error(error: Exception, context: Dict[str, Any]) -> None:
        """Log unhandled errors with full context"""
        logger.error("Unhandled error occurred:")
        logger.error(f"Error type: {type(error).__name__}")
        logger.error(f"Error message: {str(error)}")
        logger.error(f"Context: {context}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # In production, this could trigger alerts/notifications
        if Config.PRODUCTION_MODE:
            await ErrorHandler._trigger_error_alert(error, context)
    
    @staticmethod
    async def _send_error_message(client: Client, message: Optional[Message],
                                callback_query: Optional[CallbackQuery],
                                error_msg: str) -> None:
        """Send error message to user"""
        try:
            if callback_query:
                await callback_query.answer(error_msg, show_alert=True)
            elif message:
                await message.reply_text(error_msg)
        except Exception as e:
            logger.error(f"Failed to send error message to user: {e}")
    
    @staticmethod
    async def _trigger_error_alert(error: Exception, context: Dict[str, Any]) -> None:
        """Trigger alerts for critical errors (placeholder for future implementation)"""
        # This could send notifications to admin, external monitoring services, etc.
        logger.critical(f"Critical error alert triggered: {error}")

def error_handler(func: Callable) -> Callable:
    """
    Decorator for automatic error handling in bot functions
    """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Extract context from function arguments
            context = {
                'function': func.__name__,
                'args': str(args)[:200],  # Truncate for log size
                'kwargs': str(kwargs)[:200],
                'timestamp': datetime.now().isoformat()
            }
            
            # Try to extract user info from common argument patterns
            user_id = None
            user_lang = 'fa'
            client = None
            message = None
            callback_query = None
            
            for arg in args:
                if hasattr(arg, 'from_user') and hasattr(arg.from_user, 'id'):
                    user_id = arg.from_user.id
                    if hasattr(arg, 'reply_text'):  # Message
                        message = arg
                    elif hasattr(arg, 'answer'):  # CallbackQuery
                        callback_query = arg
                elif hasattr(arg, 'send_message'):  # Client
                    client = arg
            
            context['user_id'] = user_id
            
            # Handle Pyrogram errors first
            if client and hasattr(e, '__module__') and 'pyrogram' in str(e.__module__):
                handled = await ErrorHandler.handle_pyrogram_error(
                    e, client, message, callback_query, user_lang
                )
                if handled:
                    return None
            
            # Log the unhandled error
            await ErrorHandler.log_unhandled_error(e, context)
            
            # Send generic error message to user if possible
            if client and (message or callback_query):
                generic_error = translator.get_text('error.generic', user_lang)
                await ErrorHandler._send_error_message(client, message, callback_query, generic_error)
            
            # Re-raise for critical errors in production
            if Config.PRODUCTION_MODE:
                raise e
            
    return wrapper

class RateLimiter:
    """Rate limiting for bot operations"""
    
    def __init__(self):
        self.user_operations = {}
        self.limits = Config.RATE_LIMITS if hasattr(Config, 'RATE_LIMITS') else {
            'messages_per_minute': 30,
            'commands_per_minute': 10
        }
    
    async def is_allowed(self, user_id: int, operation: str) -> bool:
        """Check if user is within rate limits for operation"""
        current_time = datetime.now()
        
        if user_id not in self.user_operations:
            self.user_operations[user_id] = {}
        
        if operation not in self.user_operations[user_id]:
            self.user_operations[user_id][operation] = []
        
        # Clean old entries (older than 1 minute)
        cutoff_time = current_time - timedelta(minutes=1)
        self.user_operations[user_id][operation] = [
            timestamp for timestamp in self.user_operations[user_id][operation]
            if timestamp > cutoff_time
        ]
        
        # Check limit
        limit_key = f"{operation}_per_minute"
        limit = self.limits.get(limit_key, 30)
        
        if len(self.user_operations[user_id][operation]) >= limit:
            logger.warning(f"Rate limit exceeded for user {user_id} operation {operation}")
            return False
        
        # Add current operation
        self.user_operations[user_id][operation].append(current_time)
        return True

# Global instances
rate_limiter = RateLimiter()
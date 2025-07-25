"""
File Storage Service for CodeRoot Bot
Handles file uploads and management using S3-compatible storage
"""

import os
import logging
import asyncio
from typing import Optional, Dict, Any, BinaryIO
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from config import Config

logger = logging.getLogger(__name__)

class FileStorageService:
    """
    File storage service using S3-compatible storage (Amazon S3, MinIO, etc.)
    """
    
    def __init__(self):
        """Initialize file storage service"""
        self.enabled = Config.S3_ACCESS_KEY and Config.S3_SECRET_KEY
        self.client = None
        
        if self.enabled:
            try:
                self.client = boto3.client(
                    's3',
                    aws_access_key_id=Config.S3_ACCESS_KEY,
                    aws_secret_access_key=Config.S3_SECRET_KEY,
                    endpoint_url=Config.S3_ENDPOINT_URL if Config.S3_ENDPOINT_URL else None,
                    region_name=Config.S3_REGION
                )
                logger.info("File storage service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize file storage: {e}")
                self.enabled = False
        else:
            logger.warning("File storage service disabled - missing credentials")
    
    async def upload_file(self, file_data: bytes, file_name: str, content_type: str = 'application/octet-stream', 
                         folder: str = 'uploads') -> Optional[str]:
        """
        Upload file to storage
        
        Args:
            file_data: File content as bytes
            file_name: Original file name
            content_type: MIME type of the file
            folder: Folder/prefix for the file
        
        Returns:
            Public URL of uploaded file or None if failed
        """
        if not self.enabled:
            logger.warning("File storage not available")
            return None
        
        try:
            # Generate unique file name with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_name = f"{folder}/{timestamp}_{file_name}"
            
            # Upload file
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.put_object(
                    Bucket=Config.S3_BUCKET_NAME,
                    Key=unique_name,
                    Body=file_data,
                    ContentType=content_type,
                    ACL='public-read'  # Make file publicly accessible
                )
            )
            
            # Generate public URL
            if Config.S3_ENDPOINT_URL:
                # Custom endpoint (MinIO, etc.)
                public_url = f"{Config.S3_ENDPOINT_URL.rstrip('/')}/{Config.S3_BUCKET_NAME}/{unique_name}"
            else:
                # AWS S3
                public_url = f"https://{Config.S3_BUCKET_NAME}.s3.{Config.S3_REGION}.amazonaws.com/{unique_name}"
            
            logger.info(f"File uploaded successfully: {unique_name}")
            return public_url
            
        except Exception as e:
            logger.error(f"File upload failed: {e}")
            return None
    
    async def upload_user_file(self, user_id: int, file_data: bytes, file_name: str, 
                              file_type: str = 'document') -> Optional[str]:
        """
        Upload user-specific file (profile pictures, documents, etc.)
        
        Args:
            user_id: User ID
            file_data: File content
            file_name: Original file name
            file_type: Type of file (profile, document, product_image, etc.)
        
        Returns:
            Public URL of uploaded file
        """
        folder = f"users/{user_id}/{file_type}"
        
        # Determine content type
        content_type = self._get_content_type(file_name)
        
        return await self.upload_file(file_data, file_name, content_type, folder)
    
    async def upload_shop_file(self, shop_id: str, file_data: bytes, file_name: str, 
                              file_type: str = 'product') -> Optional[str]:
        """
        Upload shop-specific file (product images, shop logo, etc.)
        
        Args:
            shop_id: Shop ID
            file_data: File content
            file_name: Original file name
            file_type: Type of file (product, logo, banner, etc.)
        
        Returns:
            Public URL of uploaded file
        """
        folder = f"shops/{shop_id}/{file_type}"
        
        # Determine content type
        content_type = self._get_content_type(file_name)
        
        return await self.upload_file(file_data, file_name, content_type, folder)
    
    async def delete_file(self, file_url: str) -> bool:
        """
        Delete file from storage
        
        Args:
            file_url: Public URL of the file to delete
        
        Returns:
            True if deleted successfully, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            # Extract key from URL
            key = self._extract_key_from_url(file_url)
            if not key:
                return False
            
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.delete_object(
                    Bucket=Config.S3_BUCKET_NAME,
                    Key=key
                )
            )
            
            logger.info(f"File deleted successfully: {key}")
            return True
            
        except Exception as e:
            logger.error(f"File deletion failed: {e}")
            return False
    
    async def generate_presigned_url(self, file_key: str, expiration: int = 3600) -> Optional[str]:
        """
        Generate presigned URL for temporary access to private files
        
        Args:
            file_key: S3 object key
            expiration: URL expiration time in seconds
        
        Returns:
            Presigned URL or None if failed
        """
        if not self.enabled:
            return None
        
        try:
            url = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': Config.S3_BUCKET_NAME, 'Key': file_key},
                    ExpiresIn=expiration
                )
            )
            
            return url
            
        except Exception as e:
            logger.error(f"Presigned URL generation failed: {e}")
            return None
    
    async def list_user_files(self, user_id: int, file_type: str = None) -> list:
        """
        List files for a specific user
        
        Args:
            user_id: User ID
            file_type: Optional file type filter
        
        Returns:
            List of file information dictionaries
        """
        if not self.enabled:
            return []
        
        try:
            prefix = f"users/{user_id}/"
            if file_type:
                prefix += f"{file_type}/"
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.list_objects_v2(
                    Bucket=Config.S3_BUCKET_NAME,
                    Prefix=prefix
                )
            )
            
            files = []
            for obj in response.get('Contents', []):
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'],
                    'url': self._generate_public_url(obj['Key'])
                })
            
            return files
            
        except Exception as e:
            logger.error(f"File listing failed: {e}")
            return []
    
    async def get_storage_usage(self, prefix: str = '') -> Dict[str, Any]:
        """
        Get storage usage statistics
        
        Args:
            prefix: Optional prefix to filter objects
        
        Returns:
            Dictionary with usage statistics
        """
        if not self.enabled:
            return {'total_size': 0, 'file_count': 0}
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.list_objects_v2(
                    Bucket=Config.S3_BUCKET_NAME,
                    Prefix=prefix
                )
            )
            
            total_size = 0
            file_count = 0
            
            for obj in response.get('Contents', []):
                total_size += obj['Size']
                file_count += 1
            
            return {
                'total_size': total_size,
                'file_count': file_count,
                'total_size_mb': round(total_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            logger.error(f"Storage usage calculation failed: {e}")
            return {'total_size': 0, 'file_count': 0}
    
    def _get_content_type(self, file_name: str) -> str:
        """Get content type based on file extension"""
        extension = file_name.lower().split('.')[-1] if '.' in file_name else ''
        
        content_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'pdf': 'application/pdf',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'txt': 'text/plain',
            'zip': 'application/zip',
            'mp4': 'video/mp4',
            'mp3': 'audio/mpeg'
        }
        
        return content_types.get(extension, 'application/octet-stream')
    
    def _extract_key_from_url(self, file_url: str) -> Optional[str]:
        """Extract S3 object key from public URL"""
        try:
            if Config.S3_ENDPOINT_URL and Config.S3_ENDPOINT_URL in file_url:
                # Custom endpoint
                return file_url.split(f"/{Config.S3_BUCKET_NAME}/")[-1]
            elif 's3.' in file_url and 'amazonaws.com' in file_url:
                # AWS S3
                return file_url.split(f"{Config.S3_BUCKET_NAME}/")[-1]
            else:
                return None
        except:
            return None
    
    def _generate_public_url(self, key: str) -> str:
        """Generate public URL for an S3 object key"""
        if Config.S3_ENDPOINT_URL:
            return f"{Config.S3_ENDPOINT_URL.rstrip('/')}/{Config.S3_BUCKET_NAME}/{key}"
        else:
            return f"https://{Config.S3_BUCKET_NAME}.s3.{Config.S3_REGION}.amazonaws.com/{key}"
    
    def is_enabled(self) -> bool:
        """Check if file storage is enabled and available"""
        return self.enabled
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on file storage service"""
        if not self.enabled:
            return {
                'status': 'disabled',
                'message': 'File storage service is disabled'
            }
        
        try:
            # Try to list bucket contents (limited)
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.list_objects_v2(
                    Bucket=Config.S3_BUCKET_NAME,
                    MaxKeys=1
                )
            )
            
            return {
                'status': 'healthy',
                'message': 'File storage service is operational',
                'bucket': Config.S3_BUCKET_NAME,
                'endpoint': Config.S3_ENDPOINT_URL or 'AWS S3'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'File storage service error: {str(e)}'
            }

# Global file storage instance
file_storage = FileStorageService()
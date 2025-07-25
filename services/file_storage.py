"""
File Storage Service for CodeRoot Bot
Supports Amazon S3 and MinIO for file uploads and management
"""

import asyncio
import logging
import mimetypes
from typing import Dict, List, Optional, Tuple, BinaryIO
from datetime import datetime, timedelta
import hashlib
import os
from pathlib import Path

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

from config import Config
from utils.security import validate_file_extension, hash_file_content

logger = logging.getLogger(__name__)

class FileStorageService:
    """Service for handling file uploads and storage"""
    
    def __init__(self):
        """Initialize file storage service"""
        self.s3_client = None
        self.local_storage_path = Path("uploads")
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.allowed_extensions = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
            'documents': ['.pdf', '.doc', '.docx', '.txt'],
            'videos': ['.mp4', '.avi', '.mov', '.webm'],
            'audio': ['.mp3', '.wav', '.ogg', '.m4a']
        }
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize storage backend (S3 or local)"""
        if BOTO3_AVAILABLE and Config.S3_ACCESS_KEY and Config.S3_SECRET_KEY:
            try:
                session = boto3.Session(
                    aws_access_key_id=Config.S3_ACCESS_KEY,
                    aws_secret_access_key=Config.S3_SECRET_KEY
                )
                
                self.s3_client = session.client(
                    's3',
                    endpoint_url=Config.S3_ENDPOINT_URL if Config.S3_ENDPOINT_URL else None,
                    region_name=Config.S3_REGION
                )
                
                # Test connection
                self.s3_client.head_bucket(Bucket=Config.S3_BUCKET_NAME)
                logger.info("S3 storage initialized successfully")
                
            except (ClientError, NoCredentialsError) as e:
                logger.warning(f"S3 initialization failed: {e}. Falling back to local storage")
                self.s3_client = None
        else:
            logger.info("S3 credentials not provided. Using local storage")
        
        # Ensure local storage directory exists
        self.local_storage_path.mkdir(exist_ok=True)
        (self.local_storage_path / "images").mkdir(exist_ok=True)
        (self.local_storage_path / "documents").mkdir(exist_ok=True)
        (self.local_storage_path / "videos").mkdir(exist_ok=True)
        (self.local_storage_path / "audio").mkdir(exist_ok=True)
    
    async def upload_file(self, 
                         file_data: bytes, 
                         filename: str, 
                         user_id: int,
                         file_type: str = 'documents') -> Dict[str, str]:
        """
        Upload file to storage
        
        Args:
            file_data: File content as bytes
            filename: Original filename
            user_id: User ID for organization
            file_type: Type of file (images, documents, videos, audio)
        
        Returns:
            Dictionary with file info (url, path, size, etc.)
        """
        try:
            # Validate file
            validation_result = await self._validate_file(file_data, filename, file_type)
            if not validation_result['valid']:
                raise ValueError(validation_result['error'])
            
            # Generate unique filename
            file_hash = hashlib.md5(file_data).hexdigest()[:8]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_ext = Path(filename).suffix.lower()
            unique_filename = f"{user_id}_{timestamp}_{file_hash}{file_ext}"
            
            # Determine storage path
            storage_path = f"{file_type}/{unique_filename}"
            
            # Upload to S3 or local storage
            if self.s3_client:
                file_url = await self._upload_to_s3(file_data, storage_path)
            else:
                file_url = await self._upload_to_local(file_data, storage_path)
            
            return {
                'url': file_url,
                'filename': unique_filename,
                'original_filename': filename,
                'path': storage_path,
                'size': len(file_data),
                'type': file_type,
                'mime_type': mimetypes.guess_type(filename)[0],
                'uploaded_at': datetime.now().isoformat(),
                'user_id': user_id
            }
            
        except Exception as e:
            logger.error(f"File upload error: {e}")
            raise
    
    async def _validate_file(self, file_data: bytes, filename: str, file_type: str) -> Dict[str, any]:
        """Validate file before upload"""
        # Check file size
        if len(file_data) > self.max_file_size:
            return {
                'valid': False,
                'error': f'File too large. Maximum size: {self.max_file_size // (1024*1024)}MB'
            }
        
        # Check file extension
        file_ext = Path(filename).suffix.lower()
        if file_type not in self.allowed_extensions:
            return {'valid': False, 'error': 'Invalid file type'}
        
        if file_ext not in self.allowed_extensions[file_type]:
            return {
                'valid': False,
                'error': f'File extension not allowed for {file_type}. Allowed: {self.allowed_extensions[file_type]}'
            }
        
        # Check file content (basic validation)
        if not file_data or len(file_data) < 10:
            return {'valid': False, 'error': 'File appears to be empty or corrupted'}
        
        return {'valid': True, 'error': None}
    
    async def _upload_to_s3(self, file_data: bytes, storage_path: str) -> str:
        """Upload file to S3 storage"""
        try:
            # Upload file
            self.s3_client.put_object(
                Bucket=Config.S3_BUCKET_NAME,
                Key=storage_path,
                Body=file_data,
                ContentType=mimetypes.guess_type(storage_path)[0] or 'application/octet-stream'
            )
            
            # Generate URL
            if Config.S3_ENDPOINT_URL:
                # For MinIO or custom S3 endpoint
                file_url = f"{Config.S3_ENDPOINT_URL}/{Config.S3_BUCKET_NAME}/{storage_path}"
            else:
                # For AWS S3
                file_url = f"https://{Config.S3_BUCKET_NAME}.s3.{Config.S3_REGION}.amazonaws.com/{storage_path}"
            
            logger.info(f"File uploaded to S3: {storage_path}")
            return file_url
            
        except ClientError as e:
            logger.error(f"S3 upload error: {e}")
            raise
    
    async def _upload_to_local(self, file_data: bytes, storage_path: str) -> str:
        """Upload file to local storage"""
        try:
            file_path = self.local_storage_path / storage_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(file_path, 'wb') as f:
                f.write(file_data)
            
            # Generate local URL (would need a web server to serve these)
            file_url = f"/uploads/{storage_path}"
            
            logger.info(f"File uploaded locally: {storage_path}")
            return file_url
            
        except Exception as e:
            logger.error(f"Local upload error: {e}")
            raise
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete file from storage"""
        try:
            if self.s3_client:
                self.s3_client.delete_object(
                    Bucket=Config.S3_BUCKET_NAME,
                    Key=file_path
                )
            else:
                local_path = self.local_storage_path / file_path
                if local_path.exists():
                    local_path.unlink()
            
            logger.info(f"File deleted: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"File deletion error: {e}")
            return False
    
    async def get_file(self, file_path: str) -> Optional[bytes]:
        """Retrieve file content from storage"""
        try:
            if self.s3_client:
                response = self.s3_client.get_object(
                    Bucket=Config.S3_BUCKET_NAME,
                    Key=file_path
                )
                return response['Body'].read()
            else:
                local_path = self.local_storage_path / file_path
                if local_path.exists():
                    return local_path.read_bytes()
            
            return None
            
        except Exception as e:
            logger.error(f"File retrieval error: {e}")
            return None
    
    async def generate_presigned_url(self, file_path: str, expiration: int = 3600) -> Optional[str]:
        """Generate presigned URL for direct file access (S3 only)"""
        if not self.s3_client:
            logger.warning("Presigned URLs not available for local storage")
            return None
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': Config.S3_BUCKET_NAME, 'Key': file_path},
                ExpiresIn=expiration
            )
            return url
            
        except ClientError as e:
            logger.error(f"Presigned URL generation error: {e}")
            return None
    
    async def list_user_files(self, user_id: int, file_type: Optional[str] = None) -> List[Dict]:
        """List files uploaded by a specific user"""
        try:
            files = []
            
            if self.s3_client:
                # List from S3
                prefix = f"{file_type}/" if file_type else ""
                response = self.s3_client.list_objects_v2(
                    Bucket=Config.S3_BUCKET_NAME,
                    Prefix=prefix
                )
                
                for obj in response.get('Contents', []):
                    key = obj['Key']
                    if key.startswith(f"{file_type}/{user_id}_") if file_type else str(user_id) in key:
                        files.append({
                            'path': key,
                            'size': obj['Size'],
                            'modified': obj['LastModified'].isoformat(),
                            'url': f"https://{Config.S3_BUCKET_NAME}.s3.{Config.S3_REGION}.amazonaws.com/{key}"
                        })
            else:
                # List from local storage
                search_paths = [self.local_storage_path / file_type] if file_type else [self.local_storage_path]
                
                for search_path in search_paths:
                    if search_path.exists():
                        for file_path in search_path.rglob(f"{user_id}_*"):
                            if file_path.is_file():
                                stat = file_path.stat()
                                files.append({
                                    'path': str(file_path.relative_to(self.local_storage_path)),
                                    'size': stat.st_size,
                                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                    'url': f"/uploads/{file_path.relative_to(self.local_storage_path)}"
                                })
            
            return files
            
        except Exception as e:
            logger.error(f"File listing error: {e}")
            return []
    
    async def get_storage_stats(self) -> Dict[str, any]:
        """Get storage usage statistics"""
        try:
            stats = {
                'total_files': 0,
                'total_size': 0,
                'by_type': {},
                'storage_backend': 'S3' if self.s3_client else 'Local'
            }
            
            if self.s3_client:
                # Get S3 stats
                response = self.s3_client.list_objects_v2(Bucket=Config.S3_BUCKET_NAME)
                
                for obj in response.get('Contents', []):
                    stats['total_files'] += 1
                    stats['total_size'] += obj['Size']
                    
                    # Categorize by type
                    file_type = obj['Key'].split('/')[0] if '/' in obj['Key'] else 'other'
                    if file_type not in stats['by_type']:
                        stats['by_type'][file_type] = {'count': 0, 'size': 0}
                    stats['by_type'][file_type]['count'] += 1
                    stats['by_type'][file_type]['size'] += obj['Size']
            else:
                # Get local stats
                for file_path in self.local_storage_path.rglob('*'):
                    if file_path.is_file():
                        stats['total_files'] += 1
                        size = file_path.stat().st_size
                        stats['total_size'] += size
                        
                        # Categorize by parent directory
                        file_type = file_path.parent.name
                        if file_type not in stats['by_type']:
                            stats['by_type'][file_type] = {'count': 0, 'size': 0}
                        stats['by_type'][file_type]['count'] += 1
                        stats['by_type'][file_type]['size'] += size
            
            return stats
            
        except Exception as e:
            logger.error(f"Storage stats error: {e}")
            return {'error': str(e)}
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    
    def is_s3_configured(self) -> bool:
        """Check if S3 is properly configured"""
        return self.s3_client is not None
    
    async def health_check(self) -> Dict[str, any]:
        """Perform health check on storage service"""
        try:
            if self.s3_client:
                # Test S3 connection
                self.s3_client.head_bucket(Bucket=Config.S3_BUCKET_NAME)
                return {
                    'status': 'healthy',
                    'backend': 'S3',
                    'bucket': Config.S3_BUCKET_NAME,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                # Check local storage
                if self.local_storage_path.exists() and os.access(self.local_storage_path, os.W_OK):
                    return {
                        'status': 'healthy',
                        'backend': 'Local',
                        'path': str(self.local_storage_path),
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    return {
                        'status': 'error',
                        'error': 'Local storage path not writable',
                        'timestamp': datetime.now().isoformat()
                    }
                    
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Global file storage service instance
file_storage = FileStorageService()
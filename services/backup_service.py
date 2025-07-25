"""
Backup Service for CodeRoot Bot
Handles automatic database and file backups to S3 or local storage
"""

import asyncio
import logging
import json
import gzip
import shutil
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
import tarfile
import tempfile
import os

try:
    import boto3
    from botocore.exceptions import ClientError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

from config import Config
from database import DatabaseManager

logger = logging.getLogger(__name__)

class BackupService:
    """Service for creating and managing backups"""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize backup service"""
        self.db_manager = db_manager
        self.s3_client = None
        self.local_backup_path = Path("backups")
        self.backup_formats = ['json', 'archive']  # JSON for data, archive for complete backup
        self._initialize_backup_storage()
    
    def _initialize_backup_storage(self):
        """Initialize backup storage (S3 or local)"""
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
                
                # Test connection and create backup bucket if it doesn't exist
                try:
                    self.s3_client.head_bucket(Bucket=Config.BACKUP_S3_BUCKET)
                except ClientError as e:
                    if e.response['Error']['Code'] == '404':
                        self.s3_client.create_bucket(Bucket=Config.BACKUP_S3_BUCKET)
                        logger.info(f"Created backup bucket: {Config.BACKUP_S3_BUCKET}")
                
                logger.info("S3 backup storage initialized successfully")
                
            except Exception as e:
                logger.warning(f"S3 backup initialization failed: {e}. Using local backup")
                self.s3_client = None
        else:
            logger.info("S3 credentials not provided for backup. Using local backup")
        
        # Ensure local backup directory exists
        self.local_backup_path.mkdir(exist_ok=True)
        (self.local_backup_path / "database").mkdir(exist_ok=True)
        (self.local_backup_path / "files").mkdir(exist_ok=True)
        (self.local_backup_path / "complete").mkdir(exist_ok=True)
    
    async def create_database_backup(self, backup_type: str = 'full') -> Dict[str, any]:
        """
        Create database backup
        
        Args:
            backup_type: 'full' or 'incremental'
        
        Returns:
            Backup information dictionary
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"database_{backup_type}_{timestamp}"
            
            logger.info(f"Starting {backup_type} database backup: {backup_name}")
            
            # Collect database data
            backup_data = await self._collect_database_data(backup_type)
            
            # Create backup file
            backup_file_path = await self._create_backup_file(backup_data, backup_name, 'database')
            
            # Upload to S3 or keep local
            if self.s3_client:
                s3_path = f"database/{backup_name}.json.gz"
                await self._upload_backup_to_s3(backup_file_path, s3_path)
                backup_url = f"s3://{Config.BACKUP_S3_BUCKET}/{s3_path}"
            else:
                backup_url = str(backup_file_path)
            
            backup_info = {
                'name': backup_name,
                'type': 'database',
                'backup_type': backup_type,
                'timestamp': timestamp,
                'size': backup_file_path.stat().st_size,
                'url': backup_url,
                'collections': list(backup_data.keys()),
                'total_documents': sum(len(docs) for docs in backup_data.values())
            }
            
            # Store backup metadata
            await self._store_backup_metadata(backup_info)
            
            logger.info(f"Database backup completed: {backup_name}")
            return backup_info
            
        except Exception as e:
            logger.error(f"Database backup error: {e}")
            raise
    
    async def _collect_database_data(self, backup_type: str) -> Dict[str, List]:
        """Collect data from all database collections"""
        backup_data = {}
        
        try:
            # Get all collections
            collections = {
                'users': self.db_manager.users,
                'shops': self.db_manager.shops,
                'products': self.db_manager.products,
                'orders': self.db_manager.orders,
                'payments': self.db_manager.payments,
                'analytics': self.db_manager.analytics
            }
            
            for collection_name, manager in collections.items():
                if manager and hasattr(manager, 'collection'):
                    if backup_type == 'full':
                        # Full backup - get all documents
                        documents = await manager.collection.find({}).to_list(None)
                    else:
                        # Incremental backup - get documents modified in last 24 hours
                        since = datetime.now() - timedelta(hours=24)
                        query = {
                            '$or': [
                                {'created_at': {'$gte': since}},
                                {'updated_at': {'$gte': since}}
                            ]
                        }
                        documents = await manager.collection.find(query).to_list(None)
                    
                    # Convert ObjectId to string for JSON serialization
                    for doc in documents:
                        if '_id' in doc:
                            doc['_id'] = str(doc['_id'])
                    
                    backup_data[collection_name] = documents
                    logger.info(f"Collected {len(documents)} documents from {collection_name}")
            
            return backup_data
            
        except Exception as e:
            logger.error(f"Data collection error: {e}")
            raise
    
    async def _create_backup_file(self, data: Dict, backup_name: str, backup_type: str) -> Path:
        """Create compressed backup file"""
        try:
            # Create JSON backup
            backup_data = {
                'metadata': {
                    'name': backup_name,
                    'type': backup_type,
                    'timestamp': datetime.now().isoformat(),
                    'version': '1.0',
                    'collections': list(data.keys())
                },
                'data': data
            }
            
            # Write to temporary file
            temp_file = Path(tempfile.mktemp(suffix='.json'))
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2, default=str)
            
            # Compress the file
            backup_file_path = self.local_backup_path / backup_type / f"{backup_name}.json.gz"
            backup_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(temp_file, 'rb') as f_in:
                with gzip.open(backup_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Clean up temp file
            temp_file.unlink()
            
            return backup_file_path
            
        except Exception as e:
            logger.error(f"Backup file creation error: {e}")
            raise
    
    async def create_files_backup(self) -> Dict[str, any]:
        """Create backup of uploaded files"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"files_{timestamp}"
            
            logger.info(f"Starting files backup: {backup_name}")
            
            # Create archive of files
            backup_file_path = await self._create_files_archive(backup_name)
            
            # Upload to S3 or keep local
            if self.s3_client and backup_file_path.exists():
                s3_path = f"files/{backup_name}.tar.gz"
                await self._upload_backup_to_s3(backup_file_path, s3_path)
                backup_url = f"s3://{Config.BACKUP_S3_BUCKET}/{s3_path}"
            else:
                backup_url = str(backup_file_path)
            
            backup_info = {
                'name': backup_name,
                'type': 'files',
                'timestamp': timestamp,
                'size': backup_file_path.stat().st_size if backup_file_path.exists() else 0,
                'url': backup_url
            }
            
            # Store backup metadata
            await self._store_backup_metadata(backup_info)
            
            logger.info(f"Files backup completed: {backup_name}")
            return backup_info
            
        except Exception as e:
            logger.error(f"Files backup error: {e}")
            raise
    
    async def _create_files_archive(self, backup_name: str) -> Path:
        """Create compressed archive of uploaded files"""
        try:
            backup_file_path = self.local_backup_path / "files" / f"{backup_name}.tar.gz"
            backup_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create tar.gz archive
            with tarfile.open(backup_file_path, 'w:gz') as tar:
                # Add uploads directory if it exists
                uploads_path = Path("uploads")
                if uploads_path.exists():
                    tar.add(uploads_path, arcname="uploads")
                    logger.info(f"Added uploads directory to archive")
                
                # Add logs directory if it exists
                logs_path = Path("logs")
                if logs_path.exists():
                    tar.add(logs_path, arcname="logs")
                    logger.info(f"Added logs directory to archive")
            
            return backup_file_path
            
        except Exception as e:
            logger.error(f"Files archive creation error: {e}")
            raise
    
    async def create_complete_backup(self) -> Dict[str, any]:
        """Create complete system backup (database + files)"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"complete_{timestamp}"
            
            logger.info(f"Starting complete backup: {backup_name}")
            
            # Create database backup
            db_backup = await self.create_database_backup('full')
            
            # Create files backup
            files_backup = await self.create_files_backup()
            
            # Create complete backup metadata
            complete_backup_info = {
                'name': backup_name,
                'type': 'complete',
                'timestamp': timestamp,
                'database_backup': db_backup,
                'files_backup': files_backup,
                'total_size': db_backup['size'] + files_backup['size']
            }
            
            # Store backup metadata
            await self._store_backup_metadata(complete_backup_info)
            
            logger.info(f"Complete backup completed: {backup_name}")
            return complete_backup_info
            
        except Exception as e:
            logger.error(f"Complete backup error: {e}")
            raise
    
    async def _upload_backup_to_s3(self, local_file_path: Path, s3_path: str):
        """Upload backup file to S3"""
        try:
            with open(local_file_path, 'rb') as f:
                self.s3_client.put_object(
                    Bucket=Config.BACKUP_S3_BUCKET,
                    Key=s3_path,
                    Body=f
                )
            logger.info(f"Backup uploaded to S3: {s3_path}")
            
        except ClientError as e:
            logger.error(f"S3 upload error: {e}")
            raise
    
    async def _store_backup_metadata(self, backup_info: Dict):
        """Store backup metadata in database"""
        try:
            if self.db_manager.db:
                collection = self.db_manager.db['backups']
                await collection.insert_one(backup_info)
                logger.info(f"Backup metadata stored: {backup_info['name']}")
        except Exception as e:
            logger.error(f"Backup metadata storage error: {e}")
    
    async def list_backups(self, backup_type: Optional[str] = None) -> List[Dict]:
        """List available backups"""
        try:
            backups = []
            
            # Get from database metadata first
            if self.db_manager.db:
                collection = self.db_manager.db['backups']
                query = {'type': backup_type} if backup_type else {}
                db_backups = await collection.find(query).sort('timestamp', -1).to_list(None)
                
                for backup in db_backups:
                    backup['_id'] = str(backup['_id'])
                    backups.append(backup)
            
            # Also check local files if no database records
            if not backups:
                backups = await self._scan_local_backups(backup_type)
            
            return backups
            
        except Exception as e:
            logger.error(f"Backup listing error: {e}")
            return []
    
    async def _scan_local_backups(self, backup_type: Optional[str] = None) -> List[Dict]:
        """Scan local backup directory for backup files"""
        backups = []
        
        try:
            search_paths = []
            if backup_type:
                search_paths = [self.local_backup_path / backup_type]
            else:
                search_paths = [
                    self.local_backup_path / "database",
                    self.local_backup_path / "files",
                    self.local_backup_path / "complete"
                ]
            
            for search_path in search_paths:
                if search_path.exists():
                    for backup_file in search_path.glob("*"):
                        if backup_file.is_file():
                            stat = backup_file.stat()
                            backups.append({
                                'name': backup_file.stem,
                                'type': search_path.name,
                                'timestamp': datetime.fromtimestamp(stat.st_mtime).strftime("%Y%m%d_%H%M%S"),
                                'size': stat.st_size,
                                'url': str(backup_file),
                                'source': 'local_scan'
                            })
            
            return sorted(backups, key=lambda x: x['timestamp'], reverse=True)
            
        except Exception as e:
            logger.error(f"Local backup scan error: {e}")
            return []
    
    async def restore_backup(self, backup_name: str) -> Dict[str, any]:
        """Restore from backup"""
        try:
            logger.info(f"Starting backup restore: {backup_name}")
            
            # Find backup
            backups = await self.list_backups()
            backup_info = next((b for b in backups if b['name'] == backup_name), None)
            
            if not backup_info:
                raise ValueError(f"Backup not found: {backup_name}")
            
            result = {}
            
            if backup_info['type'] == 'database':
                result = await self._restore_database_backup(backup_info)
            elif backup_info['type'] == 'files':
                result = await self._restore_files_backup(backup_info)
            elif backup_info['type'] == 'complete':
                db_result = await self._restore_database_backup(backup_info['database_backup'])
                files_result = await self._restore_files_backup(backup_info['files_backup'])
                result = {'database': db_result, 'files': files_result}
            
            logger.info(f"Backup restore completed: {backup_name}")
            return result
            
        except Exception as e:
            logger.error(f"Backup restore error: {e}")
            raise
    
    async def _restore_database_backup(self, backup_info: Dict) -> Dict[str, any]:
        """Restore database from backup"""
        try:
            # Download backup file if needed
            backup_file_path = await self._get_backup_file(backup_info)
            
            # Read and decompress backup
            with gzip.open(backup_file_path, 'rt', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            restore_result = {'collections': {}, 'total_restored': 0}
            
            # Restore each collection
            for collection_name, documents in backup_data['data'].items():
                if hasattr(self.db_manager, collection_name):
                    manager = getattr(self.db_manager, collection_name)
                    if manager and hasattr(manager, 'collection'):
                        # Clear existing data (optional - could be made configurable)
                        # await manager.collection.delete_many({})
                        
                        # Insert backup data
                        if documents:
                            # Convert string _id back to ObjectId if needed
                            for doc in documents:
                                if '_id' in doc and isinstance(doc['_id'], str):
                                    from bson import ObjectId
                                    try:
                                        doc['_id'] = ObjectId(doc['_id'])
                                    except:
                                        del doc['_id']  # Let MongoDB generate new ID
                            
                            result = await manager.collection.insert_many(documents)
                            restore_result['collections'][collection_name] = len(result.inserted_ids)
                            restore_result['total_restored'] += len(result.inserted_ids)
                        else:
                            restore_result['collections'][collection_name] = 0
            
            return restore_result
            
        except Exception as e:
            logger.error(f"Database restore error: {e}")
            raise
    
    async def _restore_files_backup(self, backup_info: Dict) -> Dict[str, any]:
        """Restore files from backup"""
        try:
            # Download backup file if needed
            backup_file_path = await self._get_backup_file(backup_info)
            
            # Extract archive
            with tarfile.open(backup_file_path, 'r:gz') as tar:
                tar.extractall(path='.')
            
            return {'status': 'files_restored', 'backup_file': str(backup_file_path)}
            
        except Exception as e:
            logger.error(f"Files restore error: {e}")
            raise
    
    async def _get_backup_file(self, backup_info: Dict) -> Path:
        """Get backup file (download from S3 if needed)"""
        if backup_info['url'].startswith('s3://'):
            # Download from S3
            s3_path = backup_info['url'].replace(f"s3://{Config.BACKUP_S3_BUCKET}/", "")
            local_path = self.local_backup_path / "temp" / backup_info['name']
            local_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.s3_client.download_file(Config.BACKUP_S3_BUCKET, s3_path, str(local_path))
            return local_path
        else:
            # Local file
            return Path(backup_info['url'])
    
    async def cleanup_old_backups(self, retention_days: int = None) -> Dict[str, any]:
        """Clean up old backups based on retention policy"""
        try:
            retention_days = retention_days or Config.BACKUP_RETENTION_DAYS
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            logger.info(f"Cleaning up backups older than {retention_days} days")
            
            cleanup_result = {'deleted_count': 0, 'freed_space': 0}
            
            # Get old backups
            backups = await self.list_backups()
            old_backups = [
                b for b in backups 
                if datetime.strptime(b['timestamp'], "%Y%m%d_%H%M%S") < cutoff_date
            ]
            
            for backup in old_backups:
                try:
                    # Delete file
                    if backup['url'].startswith('s3://'):
                        s3_path = backup['url'].replace(f"s3://{Config.BACKUP_S3_BUCKET}/", "")
                        self.s3_client.delete_object(Bucket=Config.BACKUP_S3_BUCKET, Key=s3_path)
                    else:
                        Path(backup['url']).unlink(missing_ok=True)
                    
                    # Remove from database
                    if self.db_manager.db:
                        collection = self.db_manager.db['backups']
                        await collection.delete_one({'name': backup['name']})
                    
                    cleanup_result['deleted_count'] += 1
                    cleanup_result['freed_space'] += backup.get('size', 0)
                    
                    logger.info(f"Deleted old backup: {backup['name']}")
                    
                except Exception as e:
                    logger.error(f"Error deleting backup {backup['name']}: {e}")
            
            logger.info(f"Cleanup completed: {cleanup_result['deleted_count']} backups deleted")
            return cleanup_result
            
        except Exception as e:
            logger.error(f"Backup cleanup error: {e}")
            raise
    
    async def schedule_backup(self, backup_type: str = 'complete'):
        """Schedule automatic backup (called by scheduler)"""
        try:
            if not Config.AUTO_BACKUP_ENABLED:
                return
            
            logger.info(f"Running scheduled {backup_type} backup")
            
            if backup_type == 'complete':
                result = await self.create_complete_backup()
            elif backup_type == 'database':
                result = await self.create_database_backup('full')
            elif backup_type == 'files':
                result = await self.create_files_backup()
            else:
                raise ValueError(f"Unknown backup type: {backup_type}")
            
            # Cleanup old backups
            await self.cleanup_old_backups()
            
            logger.info(f"Scheduled backup completed: {result['name']}")
            return result
            
        except Exception as e:
            logger.error(f"Scheduled backup error: {e}")
            raise
    
    def get_backup_stats(self) -> Dict[str, any]:
        """Get backup service statistics"""
        try:
            stats = {
                'backup_enabled': Config.AUTO_BACKUP_ENABLED,
                'backup_interval': f"{Config.BACKUP_INTERVAL_HOURS} hours",
                'retention_days': Config.BACKUP_RETENTION_DAYS,
                'storage_backend': 'S3' if self.s3_client else 'Local',
                'local_backup_path': str(self.local_backup_path)
            }
            
            if self.s3_client:
                stats['s3_bucket'] = Config.BACKUP_S3_BUCKET
            
            return stats
            
        except Exception as e:
            logger.error(f"Backup stats error: {e}")
            return {'error': str(e)}
    
    async def health_check(self) -> Dict[str, any]:
        """Perform health check on backup service"""
        try:
            health = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'storage_backend': 'S3' if self.s3_client else 'Local'
            }
            
            # Check storage accessibility
            if self.s3_client:
                try:
                    self.s3_client.head_bucket(Bucket=Config.BACKUP_S3_BUCKET)
                    health['s3_accessible'] = True
                except Exception as e:
                    health['s3_accessible'] = False
                    health['s3_error'] = str(e)
            
            # Check local storage
            if self.local_backup_path.exists() and os.access(self.local_backup_path, os.W_OK):
                health['local_storage_accessible'] = True
            else:
                health['local_storage_accessible'] = False
            
            # Count available backups
            backups = await self.list_backups()
            health['total_backups'] = len(backups)
            health['backup_types'] = list(set(b['type'] for b in backups))
            
            return health
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Global backup service instance (initialized in bot.py with database manager)
backup_service = None
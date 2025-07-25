"""
Backup Service for CodeRoot Bot
Handles automatic database and file backups
"""

import asyncio
import logging
import os
import json
import zipfile
import tempfile
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import schedule
import time
from pathlib import Path

from config import Config
from database import db_manager
from services.file_storage import file_storage

logger = logging.getLogger(__name__)

class BackupService:
    """
    Automatic backup service for database and files
    """
    
    def __init__(self):
        """Initialize backup service"""
        self.enabled = Config.BACKUP_ENABLED
        self.backup_interval = Config.BACKUP_INTERVAL_HOURS or 24  # Default: daily
        self.retention_days = Config.BACKUP_RETENTION_DAYS or 30  # Default: 30 days
        self.local_backup_path = Path("backups")
        self.is_running = False
        
        # Create backup directory
        self.local_backup_path.mkdir(exist_ok=True)
        
        if self.enabled:
            logger.info("Backup service initialized")
        else:
            logger.warning("Backup service disabled")
    
    async def create_full_backup(self) -> Optional[str]:
        """
        Create a complete backup of database and files
        
        Returns:
            Backup file path or None if failed
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"coderoot_backup_{timestamp}"
            
            logger.info(f"Starting full backup: {backup_name}")
            
            # Create temporary directory for backup files
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # 1. Database backup
                db_backup_file = await self._backup_database(temp_path, timestamp)
                if not db_backup_file:
                    logger.error("Database backup failed")
                    return None
                
                # 2. Configuration backup
                config_backup_file = await self._backup_configuration(temp_path, timestamp)
                
                # 3. Create metadata file
                metadata_file = await self._create_backup_metadata(temp_path, timestamp)
                
                # 4. Create ZIP archive
                backup_file_path = self.local_backup_path / f"{backup_name}.zip"
                await self._create_backup_archive(temp_path, backup_file_path)
                
                # 5. Upload to remote storage if available
                remote_url = None
                if file_storage.is_enabled():
                    remote_url = await self._upload_backup_to_remote(backup_file_path, backup_name)
                
                # 6. Record backup information
                await self._record_backup_info(backup_name, backup_file_path, remote_url)
                
                logger.info(f"Full backup completed: {backup_file_path}")
                return str(backup_file_path)
        
        except Exception as e:
            logger.error(f"Full backup failed: {e}")
            return None
    
    async def _backup_database(self, temp_path: Path, timestamp: str) -> Optional[str]:
        """Create database backup"""
        try:
            if not db_manager or not hasattr(db_manager, 'database'):
                logger.warning("Database manager not available for backup")
                return None
            
            backup_data = {}
            
            # Backup all collections
            collections_to_backup = [
                'users', 'shops', 'products', 'orders', 
                'payments', 'referrals', 'analytics'
            ]
            
            for collection_name in collections_to_backup:
                try:
                    if hasattr(db_manager, collection_name):
                        manager = getattr(db_manager, collection_name)
                        if hasattr(manager, 'collection'):
                            collection = manager.collection
                            documents = await collection.find({}).to_list(length=None)
                            
                            # Convert ObjectId to string for JSON serialization
                            for doc in documents:
                                if '_id' in doc:
                                    doc['_id'] = str(doc['_id'])
                                # Convert datetime objects to ISO format
                                for key, value in doc.items():
                                    if isinstance(value, datetime):
                                        doc[key] = value.isoformat()
                            
                            backup_data[collection_name] = documents
                            logger.info(f"Backed up {len(documents)} documents from {collection_name}")
                
                except Exception as e:
                    logger.warning(f"Failed to backup collection {collection_name}: {e}")
                    backup_data[collection_name] = []
            
            # Save database backup to file
            db_backup_file = temp_path / f"database_backup_{timestamp}.json"
            with open(db_backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Database backup saved: {db_backup_file}")
            return str(db_backup_file)
        
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            return None
    
    async def _backup_configuration(self, temp_path: Path, timestamp: str) -> Optional[str]:
        """Create configuration backup"""
        try:
            config_data = {
                'timestamp': timestamp,
                'bot_config': {
                    'bot_token': Config.BOT_TOKEN[:10] + "..." if Config.BOT_TOKEN else None,
                    'admin_user_id': Config.ADMIN_USER_ID,
                    'plans': Config.PLANS,
                    'commission_rate': Config.COMMISSION_RATE,
                    'supported_languages': Config.SUPPORTED_LANGUAGES,
                    'default_language': Config.DEFAULT_LANGUAGE
                },
                'database_config': {
                    'database_name': Config.DATABASE_NAME,
                    'mongo_uri_masked': Config.MONGO_URI[:20] + "..." if Config.MONGO_URI else None
                },
                'features': {
                    'email_enabled': bool(Config.EMAIL_USERNAME),
                    'ai_enabled': Config.AI_ENABLED,
                    'file_storage_enabled': file_storage.is_enabled(),
                    'backup_enabled': Config.BACKUP_ENABLED
                }
            }
            
            config_backup_file = temp_path / f"config_backup_{timestamp}.json"
            with open(config_backup_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Configuration backup saved: {config_backup_file}")
            return str(config_backup_file)
        
        except Exception as e:
            logger.error(f"Configuration backup failed: {e}")
            return None
    
    async def _create_backup_metadata(self, temp_path: Path, timestamp: str) -> str:
        """Create backup metadata file"""
        try:
            # Get database statistics
            db_stats = {}
            if db_manager:
                for collection_name in ['users', 'shops', 'products', 'orders', 'payments']:
                    try:
                        if hasattr(db_manager, collection_name):
                            manager = getattr(db_manager, collection_name)
                            if hasattr(manager, 'collection'):
                                count = await manager.collection.count_documents({})
                                db_stats[collection_name] = count
                    except Exception as e:
                        logger.warning(f"Failed to get stats for {collection_name}: {e}")
                        db_stats[collection_name] = 0
            
            # Get file storage statistics
            storage_stats = {}
            if file_storage.is_enabled():
                try:
                    storage_stats = await file_storage.get_storage_usage()
                except Exception as e:
                    logger.warning(f"Failed to get storage stats: {e}")
            
            metadata = {
                'backup_info': {
                    'timestamp': timestamp,
                    'created_at': datetime.now().isoformat(),
                    'version': '1.0',
                    'type': 'full_backup',
                    'coderoot_version': '1.0.0'
                },
                'database_statistics': db_stats,
                'storage_statistics': storage_stats,
                'backup_contents': [
                    'database_backup.json',
                    'config_backup.json',
                    'metadata.json'
                ]
            }
            
            metadata_file = temp_path / f"metadata_{timestamp}.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Backup metadata created: {metadata_file}")
            return str(metadata_file)
        
        except Exception as e:
            logger.error(f"Metadata creation failed: {e}")
            return str(temp_path / "metadata_error.json")
    
    async def _create_backup_archive(self, temp_path: Path, backup_file_path: Path) -> None:
        """Create ZIP archive of backup files"""
        try:
            with zipfile.ZipFile(backup_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in temp_path.glob('*'):
                    if file_path.is_file():
                        zipf.write(file_path, file_path.name)
            
            logger.info(f"Backup archive created: {backup_file_path}")
        
        except Exception as e:
            logger.error(f"Archive creation failed: {e}")
            raise
    
    async def _upload_backup_to_remote(self, backup_file_path: Path, backup_name: str) -> Optional[str]:
        """Upload backup to remote storage"""
        try:
            if not file_storage.is_enabled():
                return None
            
            with open(backup_file_path, 'rb') as f:
                file_data = f.read()
            
            remote_url = await file_storage.upload_file(
                file_data, 
                f"{backup_name}.zip",
                'application/zip',
                'backups'
            )
            
            if remote_url:
                logger.info(f"Backup uploaded to remote storage: {remote_url}")
            
            return remote_url
        
        except Exception as e:
            logger.error(f"Remote backup upload failed: {e}")
            return None
    
    async def _record_backup_info(self, backup_name: str, local_path: Path, remote_url: Optional[str]) -> None:
        """Record backup information in database"""
        try:
            if not db_manager or not hasattr(db_manager, 'analytics'):
                return
            
            backup_info = {
                'type': 'backup_created',
                'backup_name': backup_name,
                'created_at': datetime.now(),
                'local_path': str(local_path),
                'remote_url': remote_url,
                'file_size': local_path.stat().st_size if local_path.exists() else 0
            }
            
            await db_manager.analytics.record_event('system_backup', 0, backup_info)
            logger.info(f"Backup info recorded: {backup_name}")
        
        except Exception as e:
            logger.error(f"Failed to record backup info: {e}")
    
    async def restore_from_backup(self, backup_file_path: str) -> bool:
        """
        Restore from backup file
        
        Args:
            backup_file_path: Path to backup ZIP file
        
        Returns:
            True if restoration was successful
        """
        try:
            backup_path = Path(backup_file_path)
            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_file_path}")
                return False
            
            logger.info(f"Starting restoration from: {backup_file_path}")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Extract backup archive
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    zipf.extractall(temp_path)
                
                # Find database backup file
                db_backup_files = list(temp_path.glob('database_backup_*.json'))
                if not db_backup_files:
                    logger.error("No database backup found in archive")
                    return False
                
                # Restore database
                db_backup_file = db_backup_files[0]
                success = await self._restore_database(db_backup_file)
                
                if success:
                    logger.info("Database restoration completed successfully")
                    return True
                else:
                    logger.error("Database restoration failed")
                    return False
        
        except Exception as e:
            logger.error(f"Restoration failed: {e}")
            return False
    
    async def _restore_database(self, db_backup_file: Path) -> bool:
        """Restore database from backup file"""
        try:
            if not db_manager:
                logger.error("Database manager not available for restoration")
                return False
            
            with open(db_backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # Restore each collection
            for collection_name, documents in backup_data.items():
                try:
                    if hasattr(db_manager, collection_name):
                        manager = getattr(db_manager, collection_name)
                        if hasattr(manager, 'collection'):
                            collection = manager.collection
                            
                            # Clear existing data (be careful!)
                            # await collection.delete_many({})
                            
                            # Insert backup data
                            if documents:
                                # Convert string IDs back to ObjectId if needed
                                from bson import ObjectId
                                for doc in documents:
                                    if '_id' in doc and isinstance(doc['_id'], str):
                                        try:
                                            doc['_id'] = ObjectId(doc['_id'])
                                        except:
                                            del doc['_id']  # Let MongoDB generate new ID
                                    
                                    # Convert ISO format back to datetime
                                    for key, value in doc.items():
                                        if isinstance(value, str) and 'T' in value and value.endswith('Z'):
                                            try:
                                                doc[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                                            except:
                                                pass
                                
                                await collection.insert_many(documents)
                                logger.info(f"Restored {len(documents)} documents to {collection_name}")
                
                except Exception as e:
                    logger.error(f"Failed to restore collection {collection_name}: {e}")
                    return False
            
            logger.info("Database restoration completed")
            return True
        
        except Exception as e:
            logger.error(f"Database restoration failed: {e}")
            return False
    
    async def cleanup_old_backups(self) -> None:
        """Remove old backup files based on retention policy"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            deleted_count = 0
            
            # Clean up local backups
            for backup_file in self.local_backup_path.glob('coderoot_backup_*.zip'):
                try:
                    # Extract timestamp from filename
                    timestamp_str = backup_file.stem.split('_')[-2] + '_' + backup_file.stem.split('_')[-1]
                    backup_date = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    
                    if backup_date < cutoff_date:
                        backup_file.unlink()
                        deleted_count += 1
                        logger.info(f"Deleted old backup: {backup_file}")
                
                except Exception as e:
                    logger.warning(f"Failed to process backup file {backup_file}: {e}")
            
            logger.info(f"Cleanup completed. Deleted {deleted_count} old backup files")
        
        except Exception as e:
            logger.error(f"Backup cleanup failed: {e}")
    
    async def list_backups(self) -> List[Dict[str, Any]]:
        """List available backup files"""
        try:
            backups = []
            
            for backup_file in self.local_backup_path.glob('coderoot_backup_*.zip'):
                try:
                    stat = backup_file.stat()
                    timestamp_str = backup_file.stem.split('_')[-2] + '_' + backup_file.stem.split('_')[-1]
                    backup_date = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    
                    backups.append({
                        'name': backup_file.name,
                        'path': str(backup_file),
                        'size': stat.st_size,
                        'size_mb': round(stat.st_size / (1024 * 1024), 2),
                        'created_at': backup_date.isoformat(),
                        'age_days': (datetime.now() - backup_date).days
                    })
                
                except Exception as e:
                    logger.warning(f"Failed to process backup file {backup_file}: {e}")
            
            # Sort by creation date (newest first)
            backups.sort(key=lambda x: x['created_at'], reverse=True)
            
            return backups
        
        except Exception as e:
            logger.error(f"Failed to list backups: {e}")
            return []
    
    async def get_backup_status(self) -> Dict[str, Any]:
        """Get backup service status and statistics"""
        try:
            backups = await self.list_backups()
            
            status = {
                'enabled': self.enabled,
                'is_running': self.is_running,
                'backup_interval_hours': self.backup_interval,
                'retention_days': self.retention_days,
                'local_backup_path': str(self.local_backup_path),
                'total_backups': len(backups),
                'latest_backup': backups[0] if backups else None,
                'total_backup_size_mb': sum(b['size_mb'] for b in backups),
                'remote_storage_available': file_storage.is_enabled()
            }
            
            return status
        
        except Exception as e:
            logger.error(f"Failed to get backup status: {e}")
            return {'error': str(e)}
    
    def start_automatic_backups(self) -> None:
        """Start automatic backup scheduler"""
        if not self.enabled:
            logger.warning("Automatic backups disabled")
            return
        
        try:
            # Schedule regular backups
            schedule.every(self.backup_interval).hours.do(self._run_scheduled_backup)
            
            # Schedule cleanup
            schedule.every().day.at("02:00").do(self._run_scheduled_cleanup)
            
            self.is_running = True
            logger.info(f"Automatic backups started (interval: {self.backup_interval} hours)")
            
            # Start scheduler in background
            asyncio.create_task(self._backup_scheduler())
        
        except Exception as e:
            logger.error(f"Failed to start automatic backups: {e}")
    
    def _run_scheduled_backup(self) -> None:
        """Run scheduled backup (called by scheduler)"""
        asyncio.create_task(self._async_scheduled_backup())
    
    async def _async_scheduled_backup(self) -> None:
        """Async wrapper for scheduled backup"""
        try:
            logger.info("Running scheduled backup")
            await self.create_full_backup()
        except Exception as e:
            logger.error(f"Scheduled backup failed: {e}")
    
    def _run_scheduled_cleanup(self) -> None:
        """Run scheduled cleanup (called by scheduler)"""
        asyncio.create_task(self.cleanup_old_backups())
    
    async def _backup_scheduler(self) -> None:
        """Background scheduler for automatic backups"""
        while self.is_running:
            try:
                schedule.run_pending()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Backup scheduler error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    def stop_automatic_backups(self) -> None:
        """Stop automatic backup scheduler"""
        self.is_running = False
        schedule.clear()
        logger.info("Automatic backups stopped")

# Global backup service instance
backup_service = BackupService()
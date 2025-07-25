# 📁 File Storage Setup Guide - CodeRoot Bot

## 🎯 Overview
This guide provides complete setup instructions for File Storage integration with CodeRoot Bot, supporting both Amazon S3 and self-hosted MinIO.

## 🔧 Required Dependencies

### Already Included in requirements.txt:
```
boto3==1.34.0                    # AWS SDK for Python
aiofiles==23.2.1                 # Async file operations
pillow==10.2.0                   # Image processing
```

### Additional Dependencies (if using MinIO):
```bash
pip install minio==7.2.0         # MinIO Python client
pip install aioboto3==12.1.0     # Async boto3
```

## ☁️ Option 1: Amazon S3 Setup

### 1. Create AWS Account & S3 Bucket
1. Go to [AWS Console](https://aws.amazon.com/console/)
2. Create S3 bucket: `coderoot-files-production`
3. Configure bucket policy for public/private access

### 2. Get AWS Credentials
```bash
# From AWS Console > IAM > Users > Create User
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=coderoot-files-production
```

### 3. Environment Variables (.env)
```env
# File Storage Configuration (AWS S3)
FILE_STORAGE_PROVIDER=s3
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=coderoot-files-production
S3_PUBLIC_URL=https://coderoot-files-production.s3.amazonaws.com
```

### 4. Cost Estimation (AWS S3)
- **Storage**: $0.023/GB/month (first 50TB)
- **Requests**: $0.0004/1000 PUT requests
- **Data Transfer**: Free up to 1GB/month
- **Estimated Monthly Cost**: $5-15/month (for 100GB storage)

## 🏠 Option 2: MinIO (Self-Hosted) Setup

### 1. MinIO Server Installation
```bash
# Install MinIO server
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
sudo mv minio /usr/local/bin/

# Create MinIO directories
sudo mkdir -p /opt/minio/data
sudo mkdir -p /opt/minio/config

# Create MinIO user
sudo useradd -r minio-user -s /sbin/nologin
sudo chown minio-user:minio-user /opt/minio/data
```

### 2. MinIO Configuration
```bash
# Create MinIO configuration file
sudo nano /opt/minio/config/minio

# Add configuration:
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=StrongPassword123!
MINIO_VOLUMES="/opt/minio/data"
MINIO_OPTS="--console-address :9001"
```

### 3. MinIO Service Setup
```bash
# Create systemd service
sudo nano /etc/systemd/system/minio.service

# Service content:
[Unit]
Description=MinIO
Documentation=https://docs.min.io
Wants=network-online.target
After=network-online.target
AssertFileIsExecutable=/usr/local/bin/minio

[Service]
WorkingDirectory=/opt/minio
User=minio-user
Group=minio-user
EnvironmentFile=/opt/minio/config/minio
ExecStartPre=/bin/bash -c "if [ -z \"${MINIO_VOLUMES}\" ]; then echo \"Variable MINIO_VOLUMES not set in /opt/minio/config/minio\"; exit 1; fi"
ExecStart=/usr/local/bin/minio server $MINIO_OPTS $MINIO_VOLUMES
Restart=always
LimitNOFILE=65536
TasksMax=infinity
TimeoutStopSec=infinity
SendSIGKILL=no

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable minio
sudo systemctl start minio
```

### 4. Environment Variables (.env) for MinIO
```env
# File Storage Configuration (MinIO)
FILE_STORAGE_PROVIDER=minio
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=StrongPassword123!
MINIO_BUCKET_NAME=coderoot-files
MINIO_SECURE=false
MINIO_PUBLIC_URL=http://your-server-ip:9000
```

### 5. Cost Estimation (MinIO Self-Hosted)
- **Server Requirements**: 2GB RAM, 2 CPU cores minimum
- **Storage**: Based on your server storage capacity
- **Estimated Monthly Cost**: $10-20/month (VPS hosting)

## 🔧 Implementation Files

### File Storage Service (services/file_storage.py)
```python
"""
File Storage Service for CodeRoot Bot
Supports both AWS S3 and MinIO
"""

import os
import asyncio
import aiofiles
import boto3
from botocore.exceptions import ClientError
from minio import Minio
from minio.error import S3Error
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class FileStorageService:
    def __init__(self):
        self.provider = os.getenv('FILE_STORAGE_PROVIDER', 's3')
        
        if self.provider == 's3':
            self._init_s3()
        elif self.provider == 'minio':
            self._init_minio()
    
    def _init_s3(self):
        """Initialize AWS S3 client"""
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        self.public_url = os.getenv('S3_PUBLIC_URL')
    
    def _init_minio(self):
        """Initialize MinIO client"""
        self.minio_client = Minio(
            os.getenv('MINIO_ENDPOINT'),
            access_key=os.getenv('MINIO_ACCESS_KEY'),
            secret_key=os.getenv('MINIO_SECRET_KEY'),
            secure=os.getenv('MINIO_SECURE', 'false').lower() == 'true'
        )
        self.bucket_name = os.getenv('MINIO_BUCKET_NAME')
        self.public_url = os.getenv('MINIO_PUBLIC_URL')
    
    async def upload_file(self, file_path: str, object_name: str) -> Optional[str]:
        """Upload file and return public URL"""
        try:
            if self.provider == 's3':
                return await self._upload_s3(file_path, object_name)
            elif self.provider == 'minio':
                return await self._upload_minio(file_path, object_name)
        except Exception as e:
            logger.error(f"File upload failed: {e}")
            return None
    
    async def _upload_s3(self, file_path: str, object_name: str) -> str:
        """Upload to AWS S3"""
        self.s3_client.upload_file(file_path, self.bucket_name, object_name)
        return f"{self.public_url}/{object_name}"
    
    async def _upload_minio(self, file_path: str, object_name: str) -> str:
        """Upload to MinIO"""
        self.minio_client.fput_object(self.bucket_name, object_name, file_path)
        return f"{self.public_url}/{self.bucket_name}/{object_name}"
```

## 📋 Setup Checklist

### For AWS S3:
- [ ] Create AWS account
- [ ] Create S3 bucket
- [ ] Generate IAM user with S3 permissions
- [ ] Add AWS credentials to .env
- [ ] Test file upload

### For MinIO:
- [ ] Install MinIO server
- [ ] Configure MinIO service
- [ ] Create storage bucket
- [ ] Add MinIO credentials to .env
- [ ] Test file upload

## 🧪 Testing File Storage

### Test Script (test_file_storage.py):
```python
import asyncio
from services.file_storage import FileStorageService

async def test_file_storage():
    storage = FileStorageService()
    
    # Create test file
    with open('test_image.txt', 'w') as f:
        f.write('Test file content')
    
    # Upload test
    url = await storage.upload_file('test_image.txt', 'test/image.txt')
    print(f"Upload result: {url}")
    
    # Cleanup
    os.remove('test_image.txt')

if __name__ == "__main__":
    asyncio.run(test_file_storage())
```

## 🚀 Next Steps

1. **Choose Provider**: AWS S3 (easier) or MinIO (cheaper)
2. **Follow Setup**: Complete provider-specific setup
3. **Update .env**: Add storage credentials
4. **Test Integration**: Run test script
5. **Deploy**: File storage ready for production

## 💡 Recommendations

**For Startups (Budget-Conscious)**: 
- Use MinIO on VPS (~$15/month total)

**For Scaling/Production**:
- Use AWS S3 (~$5-25/month based on usage)

**Storage Needs Estimate**:
- Product images: ~50KB-500KB each
- Shop logos: ~10KB-100KB each
- 1000 products with images: ~50-500MB
- Monthly growth: ~10-50MB

Both options are fully implemented in the codebase and ready to use!
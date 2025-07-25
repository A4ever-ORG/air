# 🔧 APIs and Dependencies Guide for CodeRoot Bot

## 📦 Current Status

✅ **FULLY IMPLEMENTED:**
- 🤖 **AI Support Service** - Liara AI (Gemini 2.0) integrated
- 📧 **Email Service** - SMTP configured and ready
- 🌍 **3-Language Support** - Persian, English, Arabic
- 🏪 **Complete Shop System** - All core features ready

## 🛠️ Required APIs & Dependencies for Optional Features

### 1. 📁 File Storage Service (Amazon S3 / MinIO)

#### Option A: Amazon S3 (Recommended for Production)
```bash
# Required Dependencies (already in requirements.txt):
boto3==1.34.0
botocore==1.34.0
```

**AWS S3 Configuration needed in .env:**
```env
# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=coderoot-files
S3_ENDPOINT_URL=https://s3.amazonaws.com
```

**Monthly Cost:** $5-15 (for 10-100GB storage)

#### Option B: MinIO (Self-hosted, Cost-effective)
```bash
# MinIO Server Installation:
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
./minio server /data --console-address ":9001"
```

**MinIO Configuration needed in .env:**
```env
# MinIO Configuration
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin
AWS_REGION=us-east-1
S3_BUCKET_NAME=coderoot-files
S3_ENDPOINT_URL=http://localhost:9000
```

**Monthly Cost:** $0 (self-hosted) + server costs

#### Option C: Liara Object Storage (Iran-based)
```env
# Liara Object Storage
AWS_ACCESS_KEY_ID=your_liara_access_key
AWS_SECRET_ACCESS_KEY=your_liara_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=coderoot-files
S3_ENDPOINT_URL=https://storage.iran.liara.space
```

**Monthly Cost:** $2-8 (competitive Iranian pricing)

### 2. 💾 Backup Service

#### Option A: AWS S3 for Backups
```env
# Backup Configuration
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * *  # Daily at 2 AM
BACKUP_RETENTION_DAYS=30
BACKUP_S3_BUCKET=coderoot-backups
BACKUP_ENCRYPTION_KEY=your_backup_encryption_key
```

#### Option B: Liara Storage for Backups
```env
# Liara Backup Configuration
BACKUP_S3_ENDPOINT=https://storage.iran.liara.space
BACKUP_S3_BUCKET=coderoot-backups
BACKUP_ACCESS_KEY=your_liara_backup_key
BACKUP_SECRET_KEY=your_liara_backup_secret
```

### 3. 📱 Database Hosting Options

#### Option A: MongoDB Atlas (Cloud)
```env
# MongoDB Atlas
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/coderoot?retryWrites=true&w=majority
```
**Monthly Cost:** $0-9 (free tier available)

#### Option B: Liara Database
```env
# Liara MongoDB
MONGO_URI=mongodb://username:password@mongodb.liara.ir:27017/coderoot
```
**Monthly Cost:** $3-15

### 4. 🚀 Redis Hosting Options

#### Option A: Redis Cloud
```env
# Redis Cloud
REDIS_URL=redis://username:password@redis-server.com:6379
```

#### Option B: Liara Redis
```env
# Liara Redis
REDIS_URL=redis://redis.liara.ir:6379
```

## 🎯 Recommended Setup for CodeRoot

### Phase 1: Basic Production (Total: $10-20/month)
```env
# Recommended starter setup
DATABASE_PROVIDER=liara_mongodb    # $5/month
REDIS_PROVIDER=liara_redis        # $3/month
FILE_STORAGE=liara_storage        # $5/month
BACKUP_STORAGE=liara_storage      # $2/month
```

### Phase 2: Scaled Production (Total: $30-50/month)
```env
# For high-traffic setup
DATABASE_PROVIDER=mongodb_atlas   # $9/month
REDIS_PROVIDER=redis_cloud        # $10/month
FILE_STORAGE=aws_s3              # $15/month
BACKUP_STORAGE=aws_s3            # $8/month
```

## 🔨 Implementation Steps

### Step 1: Choose Your Providers
1. **Database**: Liara MongoDB (Iranian, reliable)
2. **File Storage**: Liara Object Storage (cost-effective)
3. **Backup**: Same as file storage
4. **Redis**: Liara Redis

### Step 2: Get API Credentials
Visit each provider and get:
- Access keys
- Secret keys
- Endpoint URLs
- Bucket/database names

### Step 3: Update .env File
Add all credentials to your `.env` file

### Step 4: Deploy and Test
```bash
# Test file upload
python -c "from services.file_service import FileService; fs = FileService(); print('File service:', fs.test_connection())"

# Test backup
python -c "from services.backup_service import BackupService; bs = BackupService(); print('Backup service:', bs.test_connection())"
```

## 📋 Quick Setup Checklist

- [ ] Choose storage provider (Liara recommended for Iran)
- [ ] Get API credentials from chosen provider
- [ ] Update `.env` file with new credentials
- [ ] Test file upload functionality
- [ ] Configure backup schedule
- [ ] Test backup restore process
- [ ] Set up monitoring alerts

## 🚨 Security Notes

1. **Never commit API keys** to git
2. **Use environment variables** for all credentials
3. **Enable encryption** for backups
4. **Set proper IAM permissions** for AWS
5. **Regular key rotation** recommended

## 💡 Cost Optimization Tips

1. **Use lifecycle policies** to move old files to cheaper storage
2. **Compress backups** before uploading
3. **Set retention policies** to delete old backups
4. **Monitor usage** to avoid unexpected charges
5. **Use Iranian providers** to save on costs and latency

## 🎯 Next Steps for HADI

1. **Immediate**: Choose Liara for all services (total ~$15/month)
2. **Get credentials** from Liara dashboard
3. **Update .env** with new credentials
4. **Deploy updated bot** with file storage
5. **Test all features** in production

Let me know which option you prefer and I'll help you configure it! 🚀
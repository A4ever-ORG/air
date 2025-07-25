# CodeRoot Bot - API Dependencies & Configuration Guide

این سند شامل تمام API ها و وابستگی‌های مورد نیاز برای فیچرهای اختیاری CodeRoot Bot می‌باشد.

## 📋 فهرست وابستگی‌ها

### ✅ پیاده‌سازی شده

#### 1. 🤖 AI Support Service (Liara AI - Gemini)
- **وضعیت**: ✅ پیاده‌سازی کامل
- **API Provider**: Liara AI Platform
- **Model**: Google Gemini 2.0 Flash
- **کاربرد**: پشتیبانی هوشمند، پاسخ به سوالات کاربران
- **Configuration Variables**:
  ```env
  AI_API_BASE_URL=https://ai.liara.ir/api/v1/687e3da1990c24f61dae6d13
  AI_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  AI_MODEL=google/gemini-2.0-flash-001
  AI_MAX_TOKENS=2000
  AI_TEMPERATURE=0.7
  ```

#### 2. 📧 Email Service (SMTP)
- **وضعیت**: ✅ پیاده‌سازی کامل
- **API Provider**: SMTP (Gmail/SendGrid/Mailgun)
- **کاربرد**: ارسال اطلاع‌رسانی‌ها، گزارش‌ها
- **Configuration Variables**:
  ```env
  SMTP_SERVER=smtp.gmail.com
  SMTP_PORT=587
  EMAIL_USERNAME=your-email@gmail.com
  EMAIL_PASSWORD=your-app-password
  FROM_EMAIL=noreply@coderoot.com
  ```
- **راهنمای تنظیم Gmail**:
  1. فعال‌سازی 2-Step Verification
  2. ایجاد App Password
  3. استفاده از App Password به جای رمز عبور اصلی

#### 3. 📁 File Storage Service (Amazon S3/MinIO)
- **وضعیت**: ✅ پیاده‌سازی کامل
- **API Provider**: AWS S3 یا MinIO
- **کاربرد**: ذخیره فایل‌های آپلود شده (تصاویر، اسناد)
- **Configuration Variables**:
  ```env
  S3_BUCKET_NAME=coderoot-files
  S3_ACCESS_KEY=your-access-key
  S3_SECRET_KEY=your-secret-key
  S3_ENDPOINT_URL=https://s3.amazonaws.com  # برای AWS S3
  S3_REGION=us-east-1
  ```

#### 4. 💾 Backup Service
- **وضعیت**: ✅ پیاده‌سازی کامل
- **API Provider**: S3 Compatible Storage
- **کاربرد**: بک‌آپ خودکار دیتابیس و فایل‌ها
- **Configuration Variables**:
  ```env
  BACKUP_S3_BUCKET=coderoot-backups
  BACKUP_INTERVAL_HOURS=24
  BACKUP_RETENTION_DAYS=30
  AUTO_BACKUP_ENABLED=true
  ```

### 🔄 در حال پیاده‌سازی

#### 5. 📱 SMS Service (برای تأیید شماره تلفن)
- **وضعیت**: 🔄 نیاز به API
- **پیشنهادی**: Kavenegar، SMS.ir، یا TeleSign
- **کاربرد**: تأیید شماره تلفن کاربران
- **Configuration Variables مورد نیاز**:
  ```env
  SMS_API_KEY=your-sms-api-key
  SMS_API_URL=https://api.kavenegar.com/v1/YOUR-API-KEY/
  SMS_SENDER_NUMBER=10008663
  ```

#### 6. 💳 Payment Gateway (برای پرداخت خودکار)
- **وضعیت**: 🔄 نیاز به API
- **پیشنهادی**: درگاه‌های ایرانی (زرین‌پال، پی‌پی، ایران‌کیش)
- **کاربرد**: پرداخت خودکار اشتراک‌ها
- **Configuration Variables مورد نیاز**:
  ```env
  PAYMENT_GATEWAY=zarinpal
  PAYMENT_MERCHANT_ID=your-merchant-id
  PAYMENT_API_KEY=your-payment-api-key
  PAYMENT_SANDBOX=false
  ```

## 🔧 راهنمای تنظیم سرویس‌ها

### 1. Liara AI (Gemini) Setup
✅ **آماده**: API Key و Endpoint ارائه شده
```bash
# تست اتصال
curl -X POST "https://ai.liara.ir/api/v1/687e3da1990c24f61dae6d13/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "google/gemini-2.0-flash-001", "messages": [{"role": "user", "content": "Hello"}]}'
```

### 2. Email Service Setup

#### Gmail Configuration:
1. **فعال‌سازی 2-Factor Authentication**
2. **ایجاد App Password**:
   - Google Account → Security → App passwords
   - Select app: Mail
   - Copy the 16-character password
3. **Environment Variables**:
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_USERNAME=your-email@gmail.com
   EMAIL_PASSWORD=16-character-app-password
   ```

#### Alternative SMTP Providers:
- **SendGrid**: Enterprise-grade email delivery
- **Mailgun**: Developer-friendly email API
- **Amazon SES**: AWS Simple Email Service

### 3. File Storage Setup

#### AWS S3:
1. **Create S3 Bucket**
2. **Create IAM User** with S3 permissions
3. **Get Access Keys**
4. **Configuration**:
   ```env
   S3_ACCESS_KEY=AKIA...
   S3_SECRET_KEY=wJalrXUtnFEMI/K7MDENG...
   S3_ENDPOINT_URL=  # Leave empty for AWS
   S3_REGION=us-east-1
   ```

#### MinIO (Self-hosted):
1. **Install MinIO Server**
2. **Create Access Keys**
3. **Configuration**:
   ```env
   S3_ACCESS_KEY=minio-access-key
   S3_SECRET_KEY=minio-secret-key
   S3_ENDPOINT_URL=http://your-minio-server:9000
   S3_REGION=us-east-1
   ```

### 4. SMS Service Setup (اختیاری)

#### Kavenegar:
1. **ثبت‌نام در kavenegar.com**
2. **دریافت API Key**
3. **Configuration**:
   ```env
   SMS_API_KEY=your-kavenegar-api-key
   SMS_API_URL=https://api.kavenegar.com/v1/YOUR-API-KEY/
   SMS_SENDER_NUMBER=10008663
   ```

#### SMS.ir:
1. **ثبت‌نام در sms.ir**
2. **دریافت API Key**
3. **Configuration**:
   ```env
   SMS_API_KEY=your-sms-ir-api-key
   SMS_API_URL=https://api.sms.ir/
   SMS_SENDER_NUMBER=your-number
   ```

### 5. Payment Gateway Setup (اختیاری)

#### ZarinPal:
1. **ثبت‌نام در zarinpal.com**
2. **تأیید هویت و دریافت Merchant ID**
3. **Configuration**:
   ```env
   PAYMENT_GATEWAY=zarinpal
   PAYMENT_MERCHANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   PAYMENT_API_KEY=your-zarinpal-api-key
   PAYMENT_SANDBOX=false
   ```

#### Pay.ir:
1. **ثبت‌نام در pay.ir**
2. **دریافت API Key**
3. **Configuration**:
   ```env
   PAYMENT_GATEWAY=payir
   PAYMENT_API_KEY=your-payir-api-key
   PAYMENT_SANDBOX=false
   ```

## 📦 Dependencies در requirements.txt

```python
# AI Integration
openai==1.54.4

# Email Service
emails==0.6.0

# File Storage
boto3==1.34.0

# Additional dependencies برای فیچرهای جدید:
# SMS (if needed)
requests==2.31.0

# Payment Gateways
zeep==4.2.1  # برای SOAP-based APIs
```

## 🌐 Environment Variables Template

```env
# ===========================================
# CodeRoot Bot - Complete Configuration
# ===========================================

# Core Bot Configuration
BOT_TOKEN=7680510409:AAEHRgIrfH7FeuEa5qr2rFG6vGbfkVMxnVM
API_ID=17064702
API_HASH=f65880b9eededbee85346f874819bbc5
ADMIN_USER_ID=7707164235

# AI Support Service ✅
AI_API_BASE_URL=https://ai.liara.ir/api/v1/687e3da1990c24f61dae6d13
AI_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2ODdhNzhmZjI3NGUxYzRlNjgzZTEwZTkiLCJ0eXBlIjoiYXV0aCIsImlhdCI6MTc1MzEwMzg3Nn0.EiwQySwDwWXZn9BLEbKaNoClUE-Ndz_6Xl4K1J5W_cE
AI_MODEL=google/gemini-2.0-flash-001
AI_MAX_TOKENS=2000
AI_TEMPERATURE=0.7

# Email Service ✅
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
FROM_EMAIL=noreply@coderoot.com
EMAIL_NOTIFICATIONS=true

# File Storage Service ✅
S3_BUCKET_NAME=coderoot-files
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key
S3_ENDPOINT_URL=https://s3.amazonaws.com
S3_REGION=us-east-1

# Backup Service ✅
BACKUP_S3_BUCKET=coderoot-backups
BACKUP_INTERVAL_HOURS=24
BACKUP_RETENTION_DAYS=30
AUTO_BACKUP_ENABLED=true

# SMS Service (Optional) 🔄
SMS_API_KEY=your-sms-api-key
SMS_API_URL=https://api.kavenegar.com/v1/YOUR-API-KEY/
SMS_SENDER_NUMBER=10008663
SMS_VERIFICATION_ENABLED=false

# Payment Gateway (Optional) 🔄
PAYMENT_GATEWAY=zarinpal
PAYMENT_MERCHANT_ID=your-merchant-id
PAYMENT_API_KEY=your-payment-api-key
PAYMENT_SANDBOX=false
AUTOMATIC_PAYMENT_ENABLED=false

# Database
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=coderoot_production
REDIS_URL=redis://localhost:6379
```

## 🧪 Testing Commands

### Test AI Service:
```bash
python3 -c "
import asyncio
from services.ai_service import ai_service

async def test():
    response = await ai_service.get_support_response('سلام', 'fa')
    print(response)

asyncio.run(test())
"
```

### Test Email Service:
```bash
python3 -c "
import asyncio
from services.email_service import EmailService

async def test():
    email_service = EmailService()
    await email_service.send_welcome_email('test@example.com', 'Test User')

asyncio.run(test())
"
```

### Test File Storage:
```bash
python3 -c "
import asyncio
from services.file_storage import file_storage

async def test():
    health = await file_storage.health_check()
    print(health)

asyncio.run(test())
"
```

## 📊 Cost Estimation

### Monthly Costs (تخمینی):

1. **Liara AI**: ✅ Free tier available
2. **Email Service**: 
   - Gmail: Free (محدود)
   - SendGrid: $14.95/month (40k emails)
3. **File Storage**:
   - AWS S3: ~$5-20/month (بسته به حجم)
   - MinIO: Self-hosted (رایگان)
4. **SMS Service**: 
   - Kavenegar: ~$10-50/month (بسته به تعداد پیامک)
5. **Payment Gateway**:
   - ZarinPal: 1.5% transaction fee
   - Pay.ir: 2% transaction fee

**Total Estimated Cost**: $30-100/month (depending on usage)

## 🚀 Next Steps

1. **فوری**: تنظیم Email Service برای اطلاع‌رسانی‌ها
2. **کوتاه‌مدت**: پیاده‌سازی SMS برای تأیید شماره
3. **میان‌مدت**: اتصال درگاه پرداخت خودکار
4. **بلندمدت**: بهینه‌سازی File Storage و CDN

## ⚠️ Security Notes

- همیشه API Keys را در environment variables نگه دارید
- از HTTPS برای تمام API calls استفاده کنید
- API Keys را هرگز در کد commit نکنید
- برای production از Sandbox mode خارج شوید
- Backup های دوره‌ای از configuration بگیرید

---
**Documentation Version**: 1.0  
**Last Updated**: 2024-01-20  
**Contact**: @hadi_admin
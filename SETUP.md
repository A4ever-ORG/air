# 🚀 راهنمای راه‌اندازی سریع CodeRoot Bot

## 📋 پیش‌نیازها

1. **Python 3.8 یا بالاتر**
2. **MongoDB**
3. **Git**

## ⚡ راه‌اندازی سریع

### 1️⃣ دانلود پروژه

### 2️⃣ نصب وابستگی‌ها
```bash
# استفاده از Makefile (توصیه شده)
make setup
make install

# یا دستی
pip install -r requirements.txt
cp .env.example .env
```

### 3️⃣ تنظیم متغیرهای محیطی
فایل `.env` را ویرایش کنید:

```env
# اطلاعات ربات (از @BotFather)
BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRSTuVwXyZ
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890

# اطلاعات مدیر
ADMIN_USER_ID=123456789
ADMIN_USERNAME=your_username

# اطلاعات پرداخت
CARD_NUMBER=6037-9977-7766-5544
CARD_HOLDER_NAME=Your Name

# کانال اصلی (اختیاری)
MAIN_CHANNEL_ID=-1001234567890
MAIN_CHANNEL_USERNAME=your_channel

# دیتابیس
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=coderoot_bot
```

### 4️⃣ راه‌اندازی دیتابیس

#### روش 1: MongoDB محلی
```bash
# نصب MongoDB
# Ubuntu/Debian:
sudo apt update
sudo apt install mongodb

# macOS (با Homebrew):
brew install mongodb-community

# شروع MongoDB
sudo systemctl start mongod
```

#### روش 2: Docker (آسان‌تر)
```bash
# استفاده از Docker Compose
make docker-run

# یا دستی
docker-compose up -d
```

### 5️⃣ اجرای ربات
```bash
# با Makefile
make run

# یا مستقیم
python run.py
```

## 🔧 دستورات مفید

```bash
# مشاهده تمام دستورات
make help

# اجرای ربات
make run

# مشاهده لاگ‌ها
make logs

# پاک‌سازی فایل‌های موقت
make clean

# بیلد Docker
make docker-build

# اجرا با Docker
make docker-run

# توقف Docker
make docker-stop

# بررسی وضعیت
make status
```

## 🛠 تنظیمات پیشرفته

### تنظیم کانال اجباری
1. کانال تلگرام ایجاد کنید
2. ربات را به عنوان ادمین اضافه کنید
3. شناسه کانال و نام کاربری را در `.env` قرار دهید

### تنظیم پرداخت
1. اطلاعات کارت بانکی خود را در `.env` وارد کنید
2. سیستم پرداخت دستی از طریق کارت به کارت کار می‌کند

### تنظیم قیمت‌ها
در فایل `config.py` قیمت پلن‌ها را تغییر دهید:
```python
PROFESSIONAL_PLAN_PRICE = 20000  # تومان
VIP_PLAN_PRICE = 60000          # تومان
```

## 🔍 عیب‌یابی

### مشکل: ربات شروع نمی‌شود
```bash
# بررسی متغیرهای محیطی
make check-env

# مشاهده لاگ‌ها
make logs
```

### مشکل: اتصال به دیتابیس
```bash
# بررسی وضعیت MongoDB
sudo systemctl status mongod

# یا با Docker
docker-compose ps
```

### مشکل: خطای import
```bash
# نصب مجدد وابستگی‌ها
make clean
make install
```

## 📞 پشتیبانی

اگر مشکلی داشتید:

1. **لاگ‌ها را بررسی کنید:** `make logs`
2. **مستندات را مطالعه کنید:** `README.md`
3. **Issue ایجاد کنید** در GitHub
4. **با پشتیبانی تماس بگیرید**

## 🎯 مراحل بعدی

پس از راه‌اندازی موفق:

1. ✅ ربات را در تلگرام تست کنید
2. ✅ پنل مدیریت را بررسی کنید
3. ✅ یک فروشگاه نمونه ایجاد کنید
4. ✅ پرداخت‌ها را تست کنید
5. ✅ گزارش‌ها را بررسی کنید

---

🎉 **تبریک! ربات شما آماده است!**

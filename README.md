# 🏪 CodeRoot - ربات مادر فروشگاهی چندفروشنده‌ای

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0+-green.svg)](https://pyrogram.org)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB-green.svg)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🎯 درباره پروژه

CodeRoot یک ربات تلگرام پیشرفته است که به کاربران اجازه می‌دهد فروشگاه اختصاصی خود را بسازند. این ربات به کاربران امکان می‌دهد:

- ✅ یک فروشگاه جداگانه در تلگرام با برند خود داشته باشند
- ✅ محصولات‌شان را ثبت و مدیریت کنند
- ✅ درآمد کسب کنند
- ✅ از پلن‌های مختلف (رایگان، حرفه‌ای، VIP) استفاده کنند

## 🧱 ویژگی‌های اصلی

### 🟩 رابط کاربری (فروشنده + خریدار)
- 🛍 ساخت فروشگاه (انتخاب پلن و پرداخت)
- 📦 افزودن و مدیریت محصولات
- 🧾 گزارش فروش و سفارش‌ها
- 🎁 ارتقاء پلن‌ها
- 🆘 پشتیبانی / آموزش / قوانین
- 💳 تمدید اشتراک با کارت‌به‌کارت
- 📌 جوین اجباری کانال
- 🏪 ورود به فروشگاه

### 🟥 پنل مدیریت (مدیر اصلی)
- 👥 مدیریت فروشنده‌ها (تأیید/حذف/اطلاعات کامل)
- 📊 مدیریت اشتراک‌ها (تمدید، هشدار، غیرفعال‌سازی)
- 📦 محصولات فروشگاه‌ها (مشاهده، حذف، گزارش)
- 💰 گزارش مالی و کارمزد (اکسل، گزارش، لیست پرداخت‌ها)
- 📢 ارسال پیام و تبلیغات درون‌رباتی
- 🤖 مدیریت ربات‌های فروشگاه زیرمجموعه
- ⚙️ تنظیمات عمومی پروژه

### 💎 پلن‌های اشتراک

#### 🆓 پلن رایگان
- 📦 تا ۱۰ محصول
- 💳 درگاه پرداخت بله
- 📊 گزارش معمولی
- 💰 ۵٪ کارمزد

#### 💼 پلن حرفه‌ای (۲۰,۰۰۰ تومان)
- 📦 تا ۲۰۰ محصول
- 📊 گزارش‌های حرفه‌ای
- 🤖 پیام‌های خودکار
- 🎁 سیستم تخفیف
- 📢 تبلیغات درون‌رباتی
- 💰 ۵٪ کارمزد

#### 👑 پلن VIP (۶۰,۰۰۰ تومان)
- 📦 محصولات نامحدود
- 🏦 درگاه پرداخت اختصاصی
- 📊 گزارش‌های کامل و هوشمند
- 🤖 پیام‌های خودکار پیشرفته
- 🎁 تخفیف‌های پیشرفته
- 📢 تبلیغات ویژه
- 💰 بدون کارمزد

## 🚀 نصب و راه‌اندازی

### 📋 پیش‌نیازها

```bash
Python 3.8+
MongoDB
Redis (اختیاری)
```

### 🔧 نصب

1. **کلون کردن پروژه:**
```bash
git clone https://github.com/yourusername/coderoot-bot.git
cd coderoot-bot
```

2. **نصب وابستگی‌ها:**
```bash
pip install -r requirements.txt
```

3. **تنظیم متغیرهای محیطی:**
```bash
cp .env.example .env
```

سپس فایل `.env` را ویرایش کنید:
```env
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here
API_ID=your_api_id_here
API_HASH=your_api_hash_here

# Database Configuration
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=coderoot_bot

# Admin Configuration
ADMIN_USER_ID=your_admin_user_id
ADMIN_USERNAME=your_admin_username

# Payment Configuration
CARD_NUMBER=your_card_number_here
CARD_HOLDER_NAME=your_card_holder_name

# Channel Configuration
MAIN_CHANNEL_ID=your_main_channel_id
MAIN_CHANNEL_USERNAME=your_main_channel_username
```

4. **راه‌اندازی دیتابیس:**
```bash
# MongoDB باید در حال اجرا باشد
mongod
```

5. **اجرای ربات:**
```bash
python bot.py
```

## 📁 ساختار پروژه

```
coderoot-bot/
├── bot.py                 # فایل اصلی ربات
├── config.py             # تنظیمات و پیکربندی
├── database.py           # اتصال و مدیریت دیتابیس
├── utils.py              # ابزارها و کلاس‌های کمکی
├── requirements.txt      # وابستگی‌های Python
├── .env.example         # نمونه فایل متغیرهای محیطی
├── README.md            # مستندات پروژه
├── handlers/            # کنترل‌کننده‌های مختلف
│   ├── user_handlers.py # کنترل‌کننده‌های کاربری
│   └── admin_handlers.py # کنترل‌کننده‌های مدیریت
└── logs/                # فایل‌های لاگ
```

## 🛠 تکنولوژی‌های استفاده شده

- **زبان برنامه‌نویسی:** Python 3.8+
- **فریمورک ربات:** Pyrogram 2.0+
- **دیتابیس:** MongoDB
- **کتابخانه‌های کمکی:**
  - `motor` - درایور async MongoDB
  - `jdatetime` - تاریخ شمسی
  - `qrcode` - تولید QR کد
  - `pillow` - پردازش تصاویر
  - `pandas` - تولید گزارش اکسل
  - `cryptography` - رمزنگاری
  - `redis` - کش (اختیاری)
    

## 🔐 امنیت

- ✅ تأیید عضویت کانال
- ✅ اعتبارسنجی ورودی‌ها
- ✅ سیستم مجوزهای دسترسی
- ✅ لاگ‌گیری کامل عملیات
- ✅ پاک‌سازی داده‌های ورودی

## 🚀 Future Features

- [ ] سیستم پیام‌رسانی خودکار
- [ ] اتصال به درگاه‌های پرداخت آنلاین
- [ ] پنل وب مدیریت
- [ ] اپلیکیشن موبایل
- [ ] سیستم نوتیفیکیشن پیشرفته
- [ ] گزارش‌های تحلیلی پیشرفته


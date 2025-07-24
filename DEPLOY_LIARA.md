# 🚀 راهنمای دپلویمنت روی Liara - نسخه دمو

## 📋 پیش‌نیازها

1. **حساب کاربری Liara:** [liara.ir](https://liara.ir)
2. **CLI Liara نصب شده:** `npm install -g @liara/cli`
3. **اطلاعات ربات تلگرام** (توکن، API_ID, API_HASH)

## ⚡ راه‌اندازی سریع

### 1️⃣ کلون پروژه
```bash
git clone <repository-url>
cd coderoot-bot
git checkout demo
```

### 2️⃣ نصب Liara CLI
```bash
npm install -g @liara/cli
liara login
```

### 3️⃣ تنظیم متغیرهای محیطی
در پنل Liara برای اپ خود، متغیرهای زیر را تنظیم کنید:

**ضروری:**
```
BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRSTuVwXyZ
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
ADMIN_USER_ID=123456789
```

**اختیاری:**
```
ADMIN_USERNAME=your_username
CARD_NUMBER=6037-9977-7766-5544
CARD_HOLDER_NAME=نام صاحب کارت
MAIN_CHANNEL_USERNAME=your_channel
```

### 4️⃣ ایجاد اپ در Liara
```bash
# ایجاد اپ جدید
liara app:create --name coderoot-demo --platform docker

# یا استفاده از اپ موجود
liara app:list
```

### 5️⃣ دپلویمنت
```bash
# دپلویمنت اول
liara deploy --app coderoot-demo --platform docker

# دپلویمنت‌های بعدی
liara deploy --app coderoot-demo
```

## 🔧 تنظیمات پیشرفته

### فایل liara.json
```json
{
  "platform": "docker",
  "port": 8000,
  "app": "coderoot-demo",
  "environments": {
    "DEMO_MODE": "true",
    "PYTHONUNBUFFERED": "1"
  }
}
```

### مشاهده لاگ‌ها
```bash
# مشاهده لاگ‌های زنده
liara app:logs --app coderoot-demo --follow

# مشاهده لاگ‌های اخیر
liara app:logs --app coderoot-demo --lines 100
```

### ری‌استارت اپ
```bash
liara app:restart --app coderoot-demo
```

## 🐛 عیب‌یابی

### مشکل cryptography
✅ **حل شده:** ورژن cryptography در requirements.txt بهینه‌سازی شده

### مشکل: ربات شروع نمی‌شود
```bash
# بررسی لاگ‌ها
liara app:logs --app coderoot-demo

# بررسی متغیرهای محیطی
liara env:list --app coderoot-demo
```

### مشکل: متغیرهای محیطی
```bash
# تنظیم متغیر جدید
liara env:set BOT_TOKEN=your_token --app coderoot-demo

# حذف متغیر
liara env:unset VARIABLE_NAME --app coderoot-demo
```

## 📊 مانیتورینگ

### چک کردن وضعیت
```bash
liara app:info --app coderoot-demo
```

### مشاهده منابع
```bash
liara app:shell --app coderoot-demo
```

## 🔄 به‌روزرسانی

### دپلویمنت ورژن جدید
```bash
git pull origin demo
liara deploy --app coderoot-demo
```

### بازگشت به ورژن قبلی
```bash
liara app:restart --app coderoot-demo --version previous
```

## 📱 تست ربات

پس از دپلویمنت موفق:

1. ✅ ربات را در تلگرام پیدا کنید: `@your_bot_username`
2. ✅ دستور `/start` را ارسال کنید
3. ✅ دستور `/demo` برای راهنمای دمو
4. ✅ منوهای مختلف را تست کنید
5. ✅ پنل مدیریت را بررسی کنید (اگر ادمین هستید)

## 🎭 ویژگی‌های نسخه دمو

- ✅ تمام قابلیت‌های اصلی فعال
- ✅ بدون نیاز به دیتابیس
- ✅ داده‌های شبیه‌سازی شده
- ✅ ساخت فروشگاه بدون محدودیت
- ✅ پنل مدیریت کامل
- ✅ پرداخت‌های خودکار تأیید

## 💰 هزینه‌ها

**Liara:**
- پلن رایگان: محدود
- پلن پایه: از 50,000 تومان/ماه
- منابع مورد نیاز: 512MB RAM, 1 vCPU

## 📞 پشتیبانی

### مشکلات دپلویمنت:
1. **بررسی لاگ‌ها:** `liara app:logs`
2. **مستندات Liara:** [docs.liara.ir](https://docs.liara.ir)
3. **پشتیبانی Liara:** [console.liara.ir](https://console.liara.ir)

### مشکلات ربات:
1. **بررسی متغیرهای محیطی**
2. **تست در محیط محلی**
3. **مراجعه به مستندات پروژه**

## 🚀 مراحل بعدی

پس از دپلویمنت موفق:

1. ✅ تست کامل قابلیت‌ها
2. ✅ تنظیم دامنه سفارشی (اختیاری)
3. ✅ پیکربندی monitoring
4. ✅ تهیه backup برنامه‌ای

---

🎉 **تبریک! ربات دمو CodeRoot شما روی Liara مستقر شد!**

💡 **نکته:** این نسخه دمو برای نمایش قابلیت‌ها طراحی شده. برای استفاده تجاری، نسخه کامل با دیتابیس واقعی مورد نیاز است.
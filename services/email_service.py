"""
Email service for CodeRoot Bot
Provides email functionality for notifications and communications
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending notifications and reports"""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587,
                 username: str = "", password: str = "", use_tls: bool = True):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.executor = ThreadPoolExecutor(max_workers=3)
    
    async def send_email(self, to_email: str, subject: str, body: str, 
                        html_body: Optional[str] = None, attachments: Optional[List[Dict]] = None) -> bool:
        """Send email asynchronously"""
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                self.executor, 
                self._send_email_sync, 
                to_email, subject, body, html_body, attachments
            )
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def _send_email_sync(self, to_email: str, subject: str, body: str,
                        html_body: Optional[str] = None, attachments: Optional[List[Dict]] = None) -> bool:
        """Send email synchronously"""
        try:
            if not self.username or not self.password:
                logger.warning("Email credentials not configured")
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = to_email
            
            # Add text body
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # Add HTML body if provided
            if html_body:
                html_part = MIMEText(html_body, 'html', 'utf-8')
                msg.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for attachment in attachments:
                    try:
                        with open(attachment['path'], 'rb') as f:
                            attach = MIMEApplication(f.read(), _subtype=attachment.get('type', 'octet-stream'))
                            attach.add_header('Content-Disposition', 'attachment', 
                                            filename=attachment.get('name', 'attachment'))
                            msg.attach(attach)
                    except Exception as e:
                        logger.error(f"Error attaching file {attachment['path']}: {e}")
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            return False
    
    async def send_welcome_email(self, user_email: str, user_name: str, referral_code: str = "") -> bool:
        """Send welcome email to new user"""
        try:
            subject = "🎉 به CodeRoot خوش آمدید!"
            
            # Plain text version
            body = f"""
سلام {user_name} عزیز!

به خانواده بزرگ CodeRoot خوش آمدید! 🚀

CodeRoot پلتفرمی است که به شما امکان ایجاد فروشگاه آنلاین حرفه‌ای را می‌دهد.

🎯 امکانات شما:
• ایجاد فروشگاه اختصاصی
• مدیریت محصولات
• پردازش سفارش‌ها
• گزارش‌گیری پیشرفته
• درآمدزایی آنلاین

🎁 کد معرف شما: {referral_code if referral_code else 'در حال تولید...'}

برای شروع، به ربات CodeRoot مراجعه کنید و فروشگاه خود را بسازید!

موفق باشید،
تیم CodeRoot

---
این ایمیل به صورت خودکار ارسال شده است.
"""
            
            # HTML version
            html_body = EmailTemplates.welcome_email_html(user_name, referral_code)
            
            return await self.send_email(user_email, subject, body, html_body)
            
        except Exception as e:
            logger.error(f"Error sending welcome email: {e}")
            return False
    
    async def send_shop_approved_email(self, user_email: str, user_name: str, shop_name: str, plan: str) -> bool:
        """Send shop approval notification email"""
        try:
            subject = f"✅ فروشگاه {shop_name} تأیید شد!"
            
            body = f"""
تبریک {user_name} عزیز!

فروشگاه «{shop_name}» شما با موفقیت تأیید و فعال شد.

📋 جزئیات فروشگاه:
• نام: {shop_name}
• پلن: {plan}
• تاریخ فعال‌سازی: {datetime.now().strftime('%Y/%m/%d')}

حالا می‌توانید:
✅ محصولات خود را اضافه کنید
✅ سفارش‌های مشتریان را دریافت کنید
✅ گزارش‌های فروش مشاهده کنید

برای مدیریت فروشگاه خود، به ربات CodeRoot مراجعه کنید.

موفق باشید،
تیم CodeRoot
"""
            
            html_body = EmailTemplates.shop_approved_html(user_name, shop_name, plan)
            
            return await self.send_email(user_email, subject, body, html_body)
            
        except Exception as e:
            logger.error(f"Error sending shop approval email: {e}")
            return False
    
    async def send_monthly_report_email(self, user_email: str, user_name: str, 
                                      report_data: Dict, excel_path: Optional[str] = None) -> bool:
        """Send monthly report email with attachment"""
        try:
            subject = f"📊 گزارش ماهانه {datetime.now().strftime('%Y/%m')}"
            
            body = f"""
سلام {user_name} عزیز!

گزارش ماهانه فروشگاه شما آماده است.

📊 خلاصه عملکرد:
• تعداد سفارش‌ها: {report_data.get('orders_count', 0)}
• مبلغ فروش: {report_data.get('total_sales', 0):,} تومان
• تعداد مشتریان جدید: {report_data.get('new_customers', 0)}
• محبوب‌ترین محصول: {report_data.get('top_product', 'نامشخص')}

گزارش کامل در فایل پیوست ارسال شده است.

برای مشاهده جزئیات بیشتر، وارد پنل مدیریت شوید.

موفق باشید،
تیم CodeRoot
"""
            
            attachments = []
            if excel_path:
                attachments.append({
                    'path': excel_path,
                    'name': f'monthly_report_{datetime.now().strftime("%Y_%m")}.xlsx',
                    'type': 'xlsx'
                })
            
            html_body = EmailTemplates.monthly_report_html(user_name, report_data)
            
            return await self.send_email(user_email, subject, body, html_body, attachments)
            
        except Exception as e:
            logger.error(f"Error sending monthly report email: {e}")
            return False
    
    async def send_admin_daily_report(self, admin_email: str, stats: Dict) -> bool:
        """Send daily statistics report to admin"""
        try:
            subject = f"📈 گزارش روزانه CodeRoot - {datetime.now().strftime('%Y/%m/%d')}"
            
            body = f"""
گزارش روزانه سیستم CodeRoot

📊 آمار امروز:
• کاربران جدید: {stats.get('new_users', 0)}
• فروشگاه‌های جدید: {stats.get('new_shops', 0)}
• سفارش‌های جدید: {stats.get('new_orders', 0)}
• پرداخت‌های جدید: {stats.get('new_payments', 0)}
• کل درآمد امروز: {stats.get('daily_revenue', 0):,} تومان

📈 آمار کلی:
• کل کاربران: {stats.get('total_users', 0)}
• کل فروشگاه‌ها: {stats.get('total_shops', 0)}
• کل درآمد: {stats.get('total_revenue', 0):,} تومان

تیم CodeRoot
"""
            
            html_body = EmailTemplates.admin_daily_report_html(stats)
            
            return await self.send_email(admin_email, subject, body, html_body)
            
        except Exception as e:
            logger.error(f"Error sending admin daily report: {e}")
            return False
    
    async def send_subscription_expiry_reminder(self, user_email: str, user_name: str, 
                                              shop_name: str, days_left: int) -> bool:
        """Send subscription expiry reminder"""
        try:
            subject = f"⚠️ اشتراک فروشگاه {shop_name} به پایان می‌رسد"
            
            body = f"""
{user_name} عزیز!

اشتراک فروشگاه «{shop_name}» شما {days_left} روز دیگر به پایان می‌رسد.

برای جلوگیری از قطع خدمات، لطفاً اشتراک خود را تمدید کنید.

مزایای تمدید:
✅ ادامه دسترسی به تمام امکانات
✅ حفظ اطلاعات و تنظیمات
✅ عدم توقف دریافت سفارش‌ها

برای تمدید، به ربات CodeRoot مراجعه کنید.

تیم CodeRoot
"""
            
            return await self.send_email(user_email, subject, body)
            
        except Exception as e:
            logger.error(f"Error sending subscription reminder: {e}")
            return False
    
    async def send_bulk_emails(self, recipients: List[Dict], subject: str, body: str, 
                             html_body: Optional[str] = None) -> Dict[str, int]:
        """Send bulk emails with rate limiting"""
        results = {"sent": 0, "failed": 0}
        
        for recipient in recipients:
            try:
                success = await self.send_email(
                    recipient['email'], 
                    subject, 
                    body.format(**recipient), 
                    html_body.format(**recipient) if html_body else None
                )
                
                if success:
                    results["sent"] += 1
                else:
                    results["failed"] += 1
                
                # Rate limiting - wait between emails
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error sending bulk email to {recipient.get('email', 'unknown')}: {e}")
                results["failed"] += 1
        
        return results


class EmailTemplates:
    """Email templates for various notifications"""
    
    @staticmethod
    def welcome_email_html(user_name: str, referral_code: str) -> str:
        """Welcome email HTML template"""
        return f"""
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>خوش آمدید به CodeRoot</title>
    <style>
        body {{ font-family: 'Tahoma', Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .logo {{ font-size: 28px; font-weight: bold; color: #2c3e50; }}
        .welcome {{ font-size: 24px; color: #27ae60; margin: 20px 0; }}
        .features {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .feature {{ margin: 10px 0; padding: 5px 0; }}
        .referral-code {{ background-color: #e3f2fd; padding: 15px; border-radius: 8px; text-align: center; margin: 20px 0; }}
        .footer {{ text-align: center; margin-top: 30px; color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🚀 CodeRoot</div>
            <div class="welcome">سلام {user_name} عزیز!</div>
        </div>
        
        <p>به خانواده بزرگ CodeRoot خوش آمدید!</p>
        
        <div class="features">
            <h3>🎯 امکانات شما:</h3>
            <div class="feature">✅ ایجاد فروشگاه اختصاصی</div>
            <div class="feature">✅ مدیریت محصولات</div>
            <div class="feature">✅ پردازش سفارش‌ها</div>
            <div class="feature">✅ گزارش‌گیری پیشرفته</div>
            <div class="feature">✅ درآمدزایی آنلاین</div>
        </div>
        
        {f'<div class="referral-code"><strong>🎁 کد معرف شما:</strong> <code>{referral_code}</code></div>' if referral_code else ''}
        
        <p>برای شروع، به ربات CodeRoot مراجعه کنید و فروشگاه خود را بسازید!</p>
        
        <div class="footer">
            <p>موفق باشید،<br>تیم CodeRoot</p>
            <p>این ایمیل به صورت خودکار ارسال شده است.</p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def shop_approved_html(user_name: str, shop_name: str, plan: str) -> str:
        """Shop approval email HTML template"""
        return f"""
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تأیید فروشگاه</title>
    <style>
        body {{ font-family: 'Tahoma', Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .success {{ background-color: #d4edda; color: #155724; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; }}
        .shop-info {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .actions {{ background-color: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .action {{ margin: 10px 0; padding: 5px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="success">
            <h2>🎉 تبریک {user_name} عزیز!</h2>
            <p>فروشگاه شما با موفقیت تأیید شد</p>
        </div>
        
        <div class="shop-info">
            <h3>📋 جزئیات فروشگاه:</h3>
            <p><strong>نام:</strong> {shop_name}</p>
            <p><strong>پلن:</strong> {plan}</p>
            <p><strong>تاریخ فعال‌سازی:</strong> {datetime.now().strftime('%Y/%m/%d')}</p>
        </div>
        
        <div class="actions">
            <h3>حالا می‌توانید:</h3>
            <div class="action">✅ محصولات خود را اضافه کنید</div>
            <div class="action">✅ سفارش‌های مشتریان را دریافت کنید</div>
            <div class="action">✅ گزارش‌های فروش مشاهده کنید</div>
        </div>
        
        <p>برای مدیریت فروشگاه خود، به ربات CodeRoot مراجعه کنید.</p>
        
        <div style="text-align: center; margin-top: 30px; color: #7f8c8d;">
            <p>موفق باشید،<br>تیم CodeRoot</p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def monthly_report_html(user_name: str, report_data: Dict) -> str:
        """Monthly report email HTML template"""
        return f"""
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>گزارش ماهانه</title>
    <style>
        body {{ font-family: 'Tahoma', Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0; }}
        .stat {{ background-color: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ color: #7f8c8d; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>📊 گزارش ماهانه {datetime.now().strftime('%Y/%m')}</h2>
        <p>سلام {user_name} عزیز!</p>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{report_data.get('orders_count', 0)}</div>
                <div class="stat-label">تعداد سفارش‌ها</div>
            </div>
            <div class="stat">
                <div class="stat-value">{report_data.get('total_sales', 0):,}</div>
                <div class="stat-label">مبلغ فروش (تومان)</div>
            </div>
            <div class="stat">
                <div class="stat-value">{report_data.get('new_customers', 0)}</div>
                <div class="stat-label">مشتریان جدید</div>
            </div>
            <div class="stat">
                <div class="stat-value">{report_data.get('top_product', 'نامشخص')}</div>
                <div class="stat-label">محبوب‌ترین محصول</div>
            </div>
        </div>
        
        <p>گزارش کامل در فایل پیوست ارسال شده است.</p>
        
        <div style="text-align: center; margin-top: 30px; color: #7f8c8d;">
            <p>موفق باشید،<br>تیم CodeRoot</p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def admin_daily_report_html(stats: Dict) -> str:
        """Admin daily report HTML template"""
        return f"""
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>گزارش روزانه</title>
    <style>
        body {{ font-family: 'Tahoma', Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 700px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat {{ background-color: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; border-right: 4px solid #007bff; }}
        .stat-value {{ font-size: 20px; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>📈 گزارش روزانه CodeRoot</h2>
        <p>تاریخ: {datetime.now().strftime('%Y/%m/%d')}</p>
        
        <h3>📊 آمار امروز:</h3>
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{stats.get('new_users', 0)}</div>
                <div class="stat-label">کاربران جدید</div>
            </div>
            <div class="stat">
                <div class="stat-value">{stats.get('new_shops', 0)}</div>
                <div class="stat-label">فروشگاه‌های جدید</div>
            </div>
            <div class="stat">
                <div class="stat-value">{stats.get('new_orders', 0)}</div>
                <div class="stat-label">سفارش‌های جدید</div>
            </div>
            <div class="stat">
                <div class="stat-value">{stats.get('new_payments', 0)}</div>
                <div class="stat-label">پرداخت‌های جدید</div>
            </div>
        </div>
        
        <h3>📈 آمار کلی:</h3>
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{stats.get('total_users', 0)}</div>
                <div class="stat-label">کل کاربران</div>
            </div>
            <div class="stat">
                <div class="stat-value">{stats.get('total_shops', 0)}</div>
                <div class="stat-label">کل فروشگاه‌ها</div>
            </div>
            <div class="stat">
                <div class="stat-value">{stats.get('total_revenue', 0):,}</div>
                <div class="stat-label">کل درآمد (تومان)</div>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #7f8c8d;">
            <p>تیم CodeRoot</p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def subscription_expiring(user_name: str, shop_name: str, days_left: int) -> Dict[str, str]:
        """Subscription expiring notification template"""
        return {
            "subject": f"⚠️ اشتراک فروشگاه {shop_name} به پایان می‌رسد",
            "text": f"""
{user_name} عزیز!

اشتراک فروشگاه «{shop_name}» شما {days_left} روز دیگر به پایان می‌رسد.

برای جلوگیری از قطع خدمات، لطفاً اشتراک خود را تمدید کنید.
""",
            "html": f"""
<div style="direction: rtl; font-family: Tahoma;">
    <h3>⚠️ هشدار انقضای اشتراک</h3>
    <p>{user_name} عزیز!</p>
    <p>اشتراک فروشگاه «{shop_name}» شما {days_left} روز دیگر به پایان می‌رسد.</p>
    <p>برای جلوگیری از قطع خدمات، لطفاً اشتراک خود را تمدید کنید.</p>
</div>
"""
        }
    
    @staticmethod
    def payment_received(user_name: str, amount: int, payment_type: str) -> Dict[str, str]:
        """Payment received confirmation template"""
        return {
            "subject": "✅ پرداخت شما دریافت شد",
            "text": f"""
{user_name} عزیز!

پرداخت {amount:,} تومانی شما برای {payment_type} با موفقیت دریافت شد.

تیم CodeRoot
""",
            "html": f"""
<div style="direction: rtl; font-family: Tahoma;">
    <h3>✅ تأیید دریافت پرداخت</h3>
    <p>{user_name} عزیز!</p>
    <p>پرداخت {amount:,} تومانی شما برای {payment_type} با موفقیت دریافت شد.</p>
    <p>تیم CodeRoot</p>
</div>
"""
        }
"""
Email Service for CodeRoot Bot
سرویس ایمیل ربات CodeRoot
"""

import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
import aiofiles

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending notifications and reports"""
    
    def __init__(self, 
                 smtp_server: str = "smtp.gmail.com",
                 smtp_port: int = 587,
                 username: str = "",
                 password: str = "",
                 from_email: str = ""):
        """Initialize email service"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_email = from_email or username
        self.enabled = bool(username and password)
        
        if not self.enabled:
            logger.warning("Email service not configured - emails will be disabled")
    
    async def send_email(self, 
                        to_email: str, 
                        subject: str, 
                        body: str,
                        html_body: Optional[str] = None,
                        attachments: Optional[List[str]] = None) -> bool:
        """Send email with optional HTML and attachments"""
        if not self.enabled:
            logger.warning("Email service not enabled")
            return False
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.from_email
            message["To"] = to_email
            
            # Add text content
            text_part = MIMEText(body, "plain", "utf-8")
            message.attach(text_part)
            
            # Add HTML content if provided
            if html_body:
                html_part = MIMEText(html_body, "html", "utf-8")
                message.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for file_path in attachments:
                    await self._attach_file(message, file_path)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                server.sendmail(self.from_email, to_email, message.as_string())
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    async def _attach_file(self, message: MIMEMultipart, file_path: str):
        """Attach file to email message"""
        try:
            async with aiofiles.open(file_path, "rb") as attachment:
                content = await attachment.read()
            
            part = MIMEBase("application", "octet-stream")
            part.set_payload(content)
            encoders.encode_base64(part)
            
            filename = file_path.split("/")[-1]
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            
            message.attach(part)
            
        except Exception as e:
            logger.error(f"Failed to attach file {file_path}: {e}")
    
    async def send_welcome_email(self, to_email: str, user_name: str, referral_code: str) -> bool:
        """Send welcome email to new users"""
        subject = "🎉 Welcome to CodeRoot - Start Your Online Store Journey!"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; }}
                .header {{ background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
                .footer {{ background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Welcome to CodeRoot!</h1>
                <p>Your Online Store Platform</p>
            </div>
            
            <div class="content">
                <h2>Hello {user_name}! 👋</h2>
                
                <p>Thank you for joining <strong>CodeRoot</strong> - the ultimate platform for creating and managing your online store!</p>
                
                <h3>🎯 What you can do:</h3>
                <ul>
                    <li>🏪 Create your own online store in minutes</li>
                    <li>📦 Manage products with ease</li>
                    <li>📊 Track sales and analytics</li>
                    <li>💰 Earn through our referral program</li>
                </ul>
                
                <h3>🎁 Your Referral Code:</h3>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center;">
                    <code style="font-size: 18px; font-weight: bold;">{referral_code}</code>
                </div>
                
                <p>Share your referral code with friends and earn commissions!</p>
                
                <a href="https://t.me/coderoot_main_bot" class="button">🚀 Start Building Your Store</a>
                
                <h3>📞 Need Help?</h3>
                <p>Our support team is here to help you succeed. Contact us anytime through the bot or email.</p>
            </div>
            
            <div class="footer">
                <p>This email was sent from CodeRoot Bot System</p>
                <p>© 2024 CodeRoot. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        🎉 Welcome to CodeRoot!
        
        Hello {user_name}!
        
        Thank you for joining CodeRoot - the ultimate platform for creating and managing your online store!
        
        🎯 What you can do:
        • 🏪 Create your own online store in minutes
        • 📦 Manage products with ease  
        • 📊 Track sales and analytics
        • 💰 Earn through our referral program
        
        🎁 Your Referral Code: {referral_code}
        
        Share your referral code with friends and earn commissions!
        
        🚀 Start building your store: https://t.me/coderoot_main_bot
        
        📞 Need help? Contact our support team anytime.
        
        © 2024 CodeRoot. All rights reserved.
        """
        
        return await self.send_email(to_email, subject, text_body, html_body)
    
    async def send_shop_approved_email(self, to_email: str, user_name: str, shop_name: str) -> bool:
        """Send shop approval notification email"""
        subject = f"✅ Your Store '{shop_name}' has been Approved!"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; }}
                .header {{ background: linear-gradient(45deg, #28a745 0%, #20c997 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .success-box {{ background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin: 15px 0; }}
                .button {{ background: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎉 Congratulations!</h1>
                <p>Your store has been approved</p>
            </div>
            
            <div class="content">
                <h2>Great News, {user_name}! 🚀</h2>
                
                <div class="success-box">
                    <h3>✅ Store Approved: {shop_name}</h3>
                    <p>Your store has been reviewed and approved by our team!</p>
                </div>
                
                <h3>🎯 What's Next?</h3>
                <ul>
                    <li>📦 Add your first products</li>
                    <li>🎨 Customize your store settings</li>
                    <li>📱 Share your store with customers</li>
                    <li>📊 Monitor your sales dashboard</li>
                </ul>
                
                <a href="https://t.me/coderoot_main_bot" class="button">🏪 Manage Your Store</a>
                
                <p><strong>Tip:</strong> Start by adding 5-10 products with clear descriptions and images for better customer engagement!</p>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        🎉 Congratulations {user_name}!
        
        Great news! Your store '{shop_name}' has been approved and is now active.
        
        🎯 What's Next?
        • 📦 Add your first products
        • 🎨 Customize your store settings  
        • 📱 Share your store with customers
        • 📊 Monitor your sales dashboard
        
        🏪 Manage your store: https://t.me/coderoot_main_bot
        
        Tip: Start by adding 5-10 products with clear descriptions and images for better customer engagement!
        """
        
        return await self.send_email(to_email, subject, text_body, html_body)
    
    async def send_monthly_report_email(self, to_email: str, user_name: str, report_data: Dict) -> bool:
        """Send monthly performance report"""
        subject = f"📊 Your Monthly Report - {datetime.now().strftime('%B %Y')}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; }}
                .header {{ background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .stat-box {{ background: #f8f9fa; border-left: 4px solid #667eea; padding: 15px; margin: 10px 0; }}
                .stat-number {{ font-size: 24px; font-weight: bold; color: #667eea; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Monthly Report</h1>
                <p>{datetime.now().strftime('%B %Y')}</p>
            </div>
            
            <div class="content">
                <h2>Hello {user_name}! 📈</h2>
                
                <p>Here's your performance summary for this month:</p>
                
                <div class="stat-box">
                    <h3>🛒 Orders</h3>
                    <div class="stat-number">{report_data.get('orders', 0)}</div>
                    <p>Total orders this month</p>
                </div>
                
                <div class="stat-box">
                    <h3>💰 Revenue</h3>
                    <div class="stat-number">{report_data.get('revenue', 0):,} Toman</div>
                    <p>Total revenue this month</p>
                </div>
                
                <div class="stat-box">
                    <h3>👥 New Customers</h3>
                    <div class="stat-number">{report_data.get('new_customers', 0)}</div>
                    <p>New customers acquired</p>
                </div>
                
                <div class="stat-box">
                    <h3>📦 Products</h3>
                    <div class="stat-number">{report_data.get('products', 0)}</div>
                    <p>Active products in store</p>
                </div>
                
                <h3>🎯 Keep Growing!</h3>
                <p>Great work this month! Keep adding products and engaging with customers to grow your business.</p>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        📊 Monthly Report - {datetime.now().strftime('%B %Y')}
        
        Hello {user_name}!
        
        Here's your performance summary:
        
        🛒 Orders: {report_data.get('orders', 0)}
        💰 Revenue: {report_data.get('revenue', 0):,} Toman
        👥 New Customers: {report_data.get('new_customers', 0)}
        📦 Products: {report_data.get('products', 0)}
        
        🎯 Keep growing! Great work this month.
        """
        
        return await self.send_email(to_email, subject, text_body, html_body)
    
    async def send_admin_daily_report(self, admin_email: str, stats: Dict) -> bool:
        """Send daily system report to admin"""
        subject = f"🔧 CodeRoot Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; }}
                .header {{ background: #dc3545; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
                .stat-card {{ background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; border-radius: 5px; text-align: center; }}
                .stat-number {{ font-size: 32px; font-weight: bold; color: #dc3545; }}
                .alert {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔧 CodeRoot Admin Dashboard</h1>
                <p>Daily System Report</p>
            </div>
            
            <div class="content">
                <h2>System Overview - {datetime.now().strftime('%B %d, %Y')}</h2>
                
                <div class="stat-grid">
                    <div class="stat-card">
                        <h3>👥 Total Users</h3>
                        <div class="stat-number">{stats.get('total_users', 0)}</div>
                        <p>+{stats.get('new_users_today', 0)} today</p>
                    </div>
                    
                    <div class="stat-card">
                        <h3>🏪 Total Stores</h3>
                        <div class="stat-number">{stats.get('total_stores', 0)}</div>
                        <p>+{stats.get('new_stores_today', 0)} today</p>
                    </div>
                    
                    <div class="stat-card">
                        <h3>🛒 Orders Today</h3>
                        <div class="stat-number">{stats.get('orders_today', 0)}</div>
                        <p>Total processed</p>
                    </div>
                    
                    <div class="stat-card">
                        <h3>💰 Revenue Today</h3>
                        <div class="stat-number">{stats.get('revenue_today', 0):,}</div>
                        <p>Toman</p>
                    </div>
                </div>
                
                <div class="alert">
                    <h3>⚠️ Pending Actions</h3>
                    <ul>
                        <li>Stores awaiting approval: {stats.get('pending_stores', 0)}</li>
                        <li>Payments awaiting verification: {stats.get('pending_payments', 0)}</li>
                        <li>Support tickets open: {stats.get('open_tickets', 0)}</li>
                    </ul>
                </div>
                
                <h3>📈 Performance Metrics</h3>
                <ul>
                    <li>User conversion rate: {stats.get('conversion_rate', 0):.1f}%</li>
                    <li>Average order value: {stats.get('avg_order_value', 0):,} Toman</li>
                    <li>Customer retention: {stats.get('retention_rate', 0):.1f}%</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(admin_email, subject, "", html_body)


# Email templates for different scenarios
class EmailTemplates:
    """Pre-defined email templates"""
    
    @staticmethod
    def subscription_expiring(user_name: str, days_left: int) -> Dict[str, str]:
        """Subscription expiring template"""
        return {
            "subject": f"⚠️ Your CodeRoot subscription expires in {days_left} days",
            "html": f"""
            <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif;">
                <div style="background: #ff6b6b; color: white; padding: 20px; text-align: center;">
                    <h1>⚠️ Subscription Expiring</h1>
                </div>
                <div style="padding: 20px;">
                    <h2>Hello {user_name}!</h2>
                    <p>Your CodeRoot subscription will expire in <strong>{days_left} days</strong>.</p>
                    <p>Renew now to continue enjoying all features:</p>
                    <ul>
                        <li>🏪 Unlimited store management</li>
                        <li>📊 Advanced analytics</li>
                        <li>💰 Commission benefits</li>
                        <li>🆘 Priority support</li>
                    </ul>
                    <a href="https://t.me/coderoot_main_bot" style="background: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 15px 0;">🔄 Renew Subscription</a>
                </div>
            </div>
            """,
            "text": f"""
            ⚠️ Subscription Expiring
            
            Hello {user_name}!
            
            Your CodeRoot subscription will expire in {days_left} days.
            
            Renew now to continue enjoying all features:
            • 🏪 Unlimited store management
            • 📊 Advanced analytics  
            • 💰 Commission benefits
            • 🆘 Priority support
            
            🔄 Renew: https://t.me/coderoot_main_bot
            """
        }
    
    @staticmethod
    def payment_received(user_name: str, amount: float, plan_name: str) -> Dict[str, str]:
        """Payment confirmation template"""
        return {
            "subject": f"✅ Payment Confirmed - {amount:,} Toman",
            "html": f"""
            <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif;">
                <div style="background: #28a745; color: white; padding: 20px; text-align: center;">
                    <h1>✅ Payment Confirmed</h1>
                </div>
                <div style="padding: 20px;">
                    <h2>Thank you {user_name}!</h2>
                    <div style="background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <h3>Payment Details:</h3>
                        <p><strong>Amount:</strong> {amount:,} Toman</p>
                        <p><strong>Plan:</strong> {plan_name}</p>
                        <p><strong>Status:</strong> Confirmed ✅</p>
                    </div>
                    <p>Your subscription has been activated. Enjoy all the premium features!</p>
                </div>
            </div>
            """,
            "text": f"""
            ✅ Payment Confirmed
            
            Thank you {user_name}!
            
            Payment Details:
            Amount: {amount:,} Toman
            Plan: {plan_name}
            Status: Confirmed ✅
            
            Your subscription has been activated!
            """
        }

# Initialize global email service
email_service = EmailService()
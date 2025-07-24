"""
Excel report generator for CodeRoot Bot
مولد گزارش اکسل ربات CodeRoot
"""

import logging
from typing import List, Dict, Any
from datetime import datetime
import io

logger = logging.getLogger(__name__)


class ExcelGenerator:
    """Excel report generator class"""
    
    @staticmethod
    async def generate_users_report(users: List[Dict]) -> bytes:
        """Generate users report in Excel format"""
        try:
            import pandas as pd
            
            # Prepare data
            data = []
            for user in users:
                data.append({
                    'شناسه کاربری': user.get('user_id'),
                    'نام': user.get('first_name', ''),
                    'نام خانوادگی': user.get('last_name', ''),
                    'یوزرنیم': user.get('username', ''),
                    'تلفن': user.get('phone', ''),
                    'ایمیل': user.get('email', ''),
                    'پلن اشتراک': user.get('subscription', {}).get('plan', 'free'),
                    'وضعیت اشتراک': 'فعال' if user.get('subscription', {}).get('is_active') else 'غیرفعال',
                    'تاریخ انقضای اشتراک': user.get('subscription', {}).get('expires_at', ''),
                    'تعداد فروشگاه‌ها': user.get('statistics', {}).get('total_shops', 0),
                    'تعداد سفارش‌ها': user.get('statistics', {}).get('total_orders', 0),
                    'درآمد کل': user.get('statistics', {}).get('total_revenue', 0),
                    'وضعیت': user.get('status', 'active'),
                    'تاریخ ثبت‌نام': user.get('created_at', ''),
                    'آخرین بروزرسانی': user.get('updated_at', '')
                })
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Create Excel file in memory
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='گزارش کاربران', index=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['گزارش کاربران']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            output.seek(0)
            return output.read()
            
        except Exception as e:
            logger.error(f"Error generating users report: {e}")
            return b""
    
    @staticmethod
    async def generate_shops_report(shops: List[Dict]) -> bytes:
        """Generate shops report in Excel format"""
        try:
            import pandas as pd
            
            # Prepare data
            data = []
            for shop in shops:
                data.append({
                    'شناسه فروشگاه': str(shop.get('_id', '')),
                    'نام فروشگاه': shop.get('name', ''),
                    'مالک (شناسه)': shop.get('owner_id'),
                    'پلن': shop.get('plan', 'free'),
                    'توکن ربات': shop.get('bot_token', '')[:20] + '...' if shop.get('bot_token') else '',
                    'یوزرنیم ربات': shop.get('bot_username', ''),
                    'تلفن': shop.get('phone', ''),
                    'تعداد محصولات': shop.get('statistics', {}).get('total_products', 0),
                    'تعداد سفارش‌ها': shop.get('statistics', {}).get('total_orders', 0),
                    'درآمد کل': shop.get('statistics', {}).get('total_revenue', 0),
                    'تعداد مشتریان': shop.get('statistics', {}).get('total_customers', 0),
                    'وضعیت': shop.get('status', 'pending'),
                    'تاریخ ایجاد': shop.get('created_at', ''),
                    'آخرین بروزرسانی': shop.get('updated_at', '')
                })
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Create Excel file in memory
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='گزارش فروشگاه‌ها', index=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['گزارش فروشگاه‌ها']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            output.seek(0)
            return output.read()
            
        except Exception as e:
            logger.error(f"Error generating shops report: {e}")
            return b""
    
    @staticmethod
    async def generate_financial_report(payments: List[Dict]) -> bytes:
        """Generate financial report in Excel format"""
        try:
            import pandas as pd
            
            # Prepare data
            data = []
            for payment in payments:
                data.append({
                    'شناسه پرداخت': str(payment.get('_id', '')),
                    'شناسه کاربر': payment.get('user_id'),
                    'مبلغ (تومان)': payment.get('amount', 0),
                    'نوع پرداخت': payment.get('payment_type', ''),
                    'روش پرداخت': payment.get('payment_method', ''),
                    'وضعیت': payment.get('status', 'pending'),
                    'شناسه تراکنش': payment.get('transaction_id', ''),
                    'توضیحات': payment.get('description', ''),
                    'تاریخ ایجاد': payment.get('created_at', ''),
                    'تاریخ تأیید': payment.get('verified_at', ''),
                    'تأیید شده توسط': payment.get('verified_by', '')
                })
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Create Excel file in memory
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='گزارش مالی', index=False)
                
                # Add summary sheet
                summary_data = {
                    'آمار': ['کل پرداخت‌ها', 'پرداخت‌های تأیید شده', 'پرداخت‌های در انتظار', 'کل مبلغ', 'مبلغ تأیید شده'],
                    'مقدار': [
                        len(payments),
                        len([p for p in payments if p.get('status') == 'confirmed']),
                        len([p for p in payments if p.get('status') == 'pending']),
                        sum([p.get('amount', 0) for p in payments]),
                        sum([p.get('amount', 0) for p in payments if p.get('status') == 'confirmed'])
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='خلاصه', index=False)
                
                # Auto-adjust column widths for both sheets
                for sheet_name in writer.sheets:
                    worksheet = writer.sheets[sheet_name]
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
            
            output.seek(0)
            return output.read()
            
        except Exception as e:
            logger.error(f"Error generating financial report: {e}")
            return b""
    
    @staticmethod
    async def generate_complete_report(users: List[Dict], shops: List[Dict], payments: List[Dict]) -> bytes:
        """Generate complete system report"""
        try:
            import pandas as pd
            
            # Create Excel file in memory
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                
                # Users data
                users_data = []
                for user in users:
                    users_data.append({
                        'شناسه': user.get('user_id'),
                        'نام': user.get('first_name', ''),
                        'یوزرنیم': user.get('username', ''),
                        'پلن': user.get('subscription', {}).get('plan', 'free'),
                        'وضعیت': user.get('status', 'active'),
                        'تاریخ ثبت‌نام': user.get('created_at', '')
                    })
                users_df = pd.DataFrame(users_data)
                users_df.to_excel(writer, sheet_name='کاربران', index=False)
                
                # Shops data
                shops_data = []
                for shop in shops:
                    shops_data.append({
                        'نام فروشگاه': shop.get('name', ''),
                        'مالک': shop.get('owner_id'),
                        'پلن': shop.get('plan', 'free'),
                        'وضعیت': shop.get('status', 'pending'),
                        'تعداد محصولات': shop.get('statistics', {}).get('total_products', 0),
                        'درآمد': shop.get('statistics', {}).get('total_revenue', 0),
                        'تاریخ ایجاد': shop.get('created_at', '')
                    })
                shops_df = pd.DataFrame(shops_data)
                shops_df.to_excel(writer, sheet_name='فروشگاه‌ها', index=False)
                
                # Payments data
                payments_data = []
                for payment in payments:
                    payments_data.append({
                        'کاربر': payment.get('user_id'),
                        'مبلغ': payment.get('amount', 0),
                        'نوع': payment.get('payment_type', ''),
                        'وضعیت': payment.get('status', 'pending'),
                        'تاریخ': payment.get('created_at', '')
                    })
                payments_df = pd.DataFrame(payments_data)
                payments_df.to_excel(writer, sheet_name='پرداخت‌ها', index=False)
                
                # Summary data
                total_users = len(users)
                active_users = len([u for u in users if u.get('status') == 'active'])
                total_shops = len(shops)
                active_shops = len([s for s in shops if s.get('status') == 'active'])
                total_revenue = sum([p.get('amount', 0) for p in payments if p.get('status') == 'confirmed'])
                
                summary_data = {
                    'آمار کلی': [
                        'کل کاربران', 'کاربران فعال', 'کل فروشگاه‌ها', 'فروشگاه‌های فعال',
                        'کل پرداخت‌ها', 'درآمد کل (تومان)', 'تاریخ گزارش'
                    ],
                    'مقدار': [
                        total_users, active_users, total_shops, active_shops,
                        len(payments), total_revenue, datetime.now().strftime('%Y/%m/%d %H:%M')
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='خلاصه کلی', index=False)
                
                # Auto-adjust column widths
                for sheet_name in writer.sheets:
                    worksheet = writer.sheets[sheet_name]
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
            
            output.seek(0)
            return output.read()
            
        except Exception as e:
            logger.error(f"Error generating complete report: {e}")
            return b""
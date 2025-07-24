"""
Excel report generator for CodeRoot Bot
Provides functions to generate various Excel reports for admin and users
"""

import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from io import BytesIO
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import BarChart, LineChart, Reference

logger = logging.getLogger(__name__)


class ExcelGenerator:
    """Excel report generator for various data exports"""
    
    @staticmethod
    def generate_users_report(users: List[Dict], title: str = "گزارش کاربران") -> BytesIO:
        """Generate users report in Excel format"""
        try:
            # Prepare data
            data = []
            for user in users:
                data.append({
                    'شناسه کاربر': user.get('user_id', ''),
                    'نام': user.get('first_name', ''),
                    'نام خانوادگی': user.get('last_name', ''),
                    'نام کاربری': f"@{user.get('username', '')}" if user.get('username') else 'ندارد',
                    'تاریخ عضویت': user.get('created_at', datetime.now()).strftime('%Y/%m/%d') if user.get('created_at') else '',
                    'آخرین فعالیت': user.get('last_activity', datetime.now()).strftime('%Y/%m/%d') if user.get('last_activity') else '',
                    'وضعیت': user.get('status', 'فعال'),
                    'زبان': user.get('language', 'fa'),
                    'تعداد معرفی': user.get('referral_count', 0),
                    'درآمد کل': user.get('total_earnings', 0),
                    'معرف': user.get('referred_by', 'ندارد')
                })
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Create Excel file
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='کاربران', index=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['کاربران']
                
                # Style the worksheet
                ExcelGenerator._style_worksheet(worksheet, title)
                
                # Add summary
                ExcelGenerator._add_users_summary(worksheet, users, len(data) + 5)
            
            output.seek(0)
            return output
            
        except Exception as e:
            logger.error(f"Error generating users report: {e}")
            return BytesIO()
    
    @staticmethod
    def generate_shops_report(shops: List[Dict], title: str = "گزارش فروشگاه‌ها") -> BytesIO:
        """Generate shops report in Excel format"""
        try:
            # Prepare data
            data = []
            for shop in shops:
                data.append({
                    'شناسه فروشگاه': str(shop.get('_id', '')),
                    'نام فروشگاه': shop.get('name', ''),
                    'شناسه مالک': shop.get('owner_id', ''),
                    'پلن اشتراک': shop.get('plan', 'free'),
                    'وضعیت': shop.get('status', 'pending'),
                    'تاریخ ایجاد': shop.get('created_at', datetime.now()).strftime('%Y/%m/%d') if shop.get('created_at') else '',
                    'تعداد محصولات': shop.get('statistics', {}).get('total_products', 0),
                    'تعداد سفارشات': shop.get('statistics', {}).get('total_orders', 0),
                    'درآمد کل': shop.get('statistics', {}).get('total_revenue', 0),
                    'تعداد مشتریان': shop.get('statistics', {}).get('total_customers', 0),
                    'توضیحات': shop.get('description', '')[:50] + '...' if shop.get('description', '') else 'ندارد'
                })
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Create Excel file
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='فروشگاه‌ها', index=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['فروشگاه‌ها']
                
                # Style the worksheet
                ExcelGenerator._style_worksheet(worksheet, title)
                
                # Add summary
                ExcelGenerator._add_shops_summary(worksheet, shops, len(data) + 5)
            
            output.seek(0)
            return output
            
        except Exception as e:
            logger.error(f"Error generating shops report: {e}")
            return BytesIO()
    
    @staticmethod
    def generate_financial_report(payments: List[Dict], orders: List[Dict], title: str = "گزارش مالی") -> BytesIO:
        """Generate financial report in Excel format"""
        try:
            # Prepare payments data
            payments_data = []
            for payment in payments:
                payments_data.append({
                    'شناسه پرداخت': str(payment.get('_id', '')),
                    'شناسه کاربر': payment.get('user_id', ''),
                    'مبلغ (تومان)': payment.get('amount', 0),
                    'نوع پرداخت': payment.get('payment_type', ''),
                    'وضعیت': payment.get('status', 'pending'),
                    'تاریخ پرداخت': payment.get('created_at', datetime.now()).strftime('%Y/%m/%d') if payment.get('created_at') else '',
                    'شرح': payment.get('description', '')
                })
            
            # Prepare orders data
            orders_data = []
            for order in orders:
                orders_data.append({
                    'شماره سفارش': order.get('order_number', ''),
                    'شناسه فروشگاه': str(order.get('shop_id', '')),
                    'شناسه مشتری': order.get('customer_id', ''),
                    'مبلغ کل': order.get('totals', {}).get('total', 0),
                    'وضعیت': order.get('status', 'pending'),
                    'تاریخ سفارش': order.get('created_at', datetime.now()).strftime('%Y/%m/%d') if order.get('created_at') else '',
                    'نام مشتری': order.get('customer_info', {}).get('name', ''),
                    'تلفن مشتری': order.get('customer_info', {}).get('phone', '')
                })
            
            # Create DataFrames
            payments_df = pd.DataFrame(payments_data)
            orders_df = pd.DataFrame(orders_data)
            
            # Create Excel file
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Write payments sheet
                payments_df.to_excel(writer, sheet_name='پرداخت‌ها', index=False)
                
                # Write orders sheet
                orders_df.to_excel(writer, sheet_name='سفارشات', index=False)
                
                # Get workbook
                workbook = writer.book
                
                # Style payments worksheet
                payments_ws = writer.sheets['پرداخت‌ها']
                ExcelGenerator._style_worksheet(payments_ws, "گزارش پرداخت‌ها")
                ExcelGenerator._add_financial_summary(payments_ws, payments, len(payments_data) + 5)
                
                # Style orders worksheet
                orders_ws = writer.sheets['سفارشات']
                ExcelGenerator._style_worksheet(orders_ws, "گزارش سفارشات")
                ExcelGenerator._add_orders_summary(orders_ws, orders, len(orders_data) + 5)
            
            output.seek(0)
            return output
            
        except Exception as e:
            logger.error(f"Error generating financial report: {e}")
            return BytesIO()
    
    @staticmethod
    def generate_complete_report(users: List[Dict], shops: List[Dict], payments: List[Dict], orders: List[Dict]) -> BytesIO:
        """Generate complete comprehensive report"""
        try:
            output = BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Users sheet
                if users:
                    users_data = []
                    for user in users:
                        users_data.append({
                            'شناسه': user.get('user_id', ''),
                            'نام': user.get('first_name', ''),
                            'یوزرنیم': f"@{user.get('username', '')}" if user.get('username') else 'ندارد',
                            'تاریخ عضویت': user.get('created_at', datetime.now()).strftime('%Y/%m/%d') if user.get('created_at') else '',
                            'وضعیت': user.get('status', 'فعال'),
                            'تعداد معرفی': user.get('referral_count', 0)
                        })
                    
                    users_df = pd.DataFrame(users_data)
                    users_df.to_excel(writer, sheet_name='کاربران', index=False)
                    ExcelGenerator._style_worksheet(writer.sheets['کاربران'], "گزارش کاربران")
                
                # Shops sheet
                if shops:
                    shops_data = []
                    for shop in shops:
                        shops_data.append({
                            'نام فروشگاه': shop.get('name', ''),
                            'مالک': shop.get('owner_id', ''),
                            'پلن': shop.get('plan', 'free'),
                            'وضعیت': shop.get('status', 'pending'),
                            'تاریخ ایجاد': shop.get('created_at', datetime.now()).strftime('%Y/%m/%d') if shop.get('created_at') else '',
                            'تعداد محصولات': shop.get('statistics', {}).get('total_products', 0)
                        })
                    
                    shops_df = pd.DataFrame(shops_data)
                    shops_df.to_excel(writer, sheet_name='فروشگاه‌ها', index=False)
                    ExcelGenerator._style_worksheet(writer.sheets['فروشگاه‌ها'], "گزارش فروشگاه‌ها")
                
                # Financial summary sheet
                ExcelGenerator._create_summary_sheet(writer, users, shops, payments, orders)
            
            output.seek(0)
            return output
            
        except Exception as e:
            logger.error(f"Error generating complete report: {e}")
            return BytesIO()
    
    @staticmethod
    def _style_worksheet(worksheet, title: str):
        """Apply styling to worksheet"""
        try:
            # Title styling
            worksheet.insert_rows(1, 2)
            worksheet['A1'] = title
            worksheet['A1'].font = Font(name='B Nazanin', size=16, bold=True)
            worksheet['A1'].alignment = Alignment(horizontal='center')
            
            # Add date
            worksheet['A2'] = f"تاریخ تولید گزارش: {datetime.now().strftime('%Y/%m/%d %H:%M')}"
            worksheet['A2'].font = Font(name='B Nazanin', size=10)
            
            # Header styling
            header_fill = PatternFill(start_color='4F81BD', end_color='4F81BD', fill_type='solid')
            header_font = Font(name='B Nazanin', color='FFFFFF', bold=True)
            border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            
            # Apply header styling
            for cell in worksheet[4]:  # Header row is now row 4
                if cell.value:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.border = border
                    cell.alignment = Alignment(horizontal='center')
            
            # Auto-fit column widths
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
                
        except Exception as e:
            logger.error(f"Error styling worksheet: {e}")
    
    @staticmethod
    def _add_users_summary(worksheet, users: List[Dict], start_row: int):
        """Add users summary to worksheet"""
        try:
            total_users = len(users)
            active_users = len([u for u in users if u.get('status') == 'active'])
            today_users = len([u for u in users if u.get('created_at', datetime.now()).date() == datetime.now().date()])
            
            worksheet[f'A{start_row}'] = "خلاصه آمار:"
            worksheet[f'A{start_row}'].font = Font(bold=True, size=12)
            
            worksheet[f'A{start_row + 1}'] = f"کل کاربران: {total_users}"
            worksheet[f'A{start_row + 2}'] = f"کاربران فعال: {active_users}"
            worksheet[f'A{start_row + 3}'] = f"عضویت امروز: {today_users}"
            
        except Exception as e:
            logger.error(f"Error adding users summary: {e}")
    
    @staticmethod
    def _add_shops_summary(worksheet, shops: List[Dict], start_row: int):
        """Add shops summary to worksheet"""
        try:
            total_shops = len(shops)
            active_shops = len([s for s in shops if s.get('status') == 'active'])
            pending_shops = len([s for s in shops if s.get('status') == 'pending'])
            
            worksheet[f'A{start_row}'] = "خلاصه آمار:"
            worksheet[f'A{start_row}'].font = Font(bold=True, size=12)
            
            worksheet[f'A{start_row + 1}'] = f"کل فروشگاه‌ها: {total_shops}"
            worksheet[f'A{start_row + 2}'] = f"فروشگاه‌های فعال: {active_shops}"
            worksheet[f'A{start_row + 3}'] = f"در انتظار تأیید: {pending_shops}"
            
        except Exception as e:
            logger.error(f"Error adding shops summary: {e}")
    
    @staticmethod
    def _add_financial_summary(worksheet, payments: List[Dict], start_row: int):
        """Add financial summary to worksheet"""
        try:
            total_payments = len(payments)
            confirmed_payments = [p for p in payments if p.get('status') == 'confirmed']
            total_amount = sum(p.get('amount', 0) for p in confirmed_payments)
            
            worksheet[f'A{start_row}'] = "خلاصه مالی:"
            worksheet[f'A{start_row}'].font = Font(bold=True, size=12)
            
            worksheet[f'A{start_row + 1}'] = f"کل پرداخت‌ها: {total_payments}"
            worksheet[f'A{start_row + 2}'] = f"پرداخت‌های تأیید شده: {len(confirmed_payments)}"
            worksheet[f'A{start_row + 3}'] = f"مجموع مبلغ: {total_amount:,} تومان"
            
        except Exception as e:
            logger.error(f"Error adding financial summary: {e}")
    
    @staticmethod
    def _add_orders_summary(worksheet, orders: List[Dict], start_row: int):
        """Add orders summary to worksheet"""
        try:
            total_orders = len(orders)
            completed_orders = len([o for o in orders if o.get('status') == 'delivered'])
            total_revenue = sum(o.get('totals', {}).get('total', 0) for o in orders if o.get('status') == 'delivered')
            
            worksheet[f'A{start_row}'] = "خلاصه سفارشات:"
            worksheet[f'A{start_row}'].font = Font(bold=True, size=12)
            
            worksheet[f'A{start_row + 1}'] = f"کل سفارشات: {total_orders}"
            worksheet[f'A{start_row + 2}'] = f"سفارشات تکمیل شده: {completed_orders}"
            worksheet[f'A{start_row + 3}'] = f"کل فروش: {total_revenue:,} تومان"
            
        except Exception as e:
            logger.error(f"Error adding orders summary: {e}")
    
    @staticmethod
    def _create_summary_sheet(writer, users: List[Dict], shops: List[Dict], payments: List[Dict], orders: List[Dict]):
        """Create executive summary sheet"""
        try:
            # Create summary data
            summary_data = {
                'شاخص': [
                    'کل کاربران',
                    'کاربران فعال',
                    'کل فروشگاه‌ها',
                    'فروشگاه‌های فعال',
                    'کل پرداخت‌ها',
                    'کل سفارشات',
                    'کل درآمد (تومان)'
                ],
                'مقدار': [
                    len(users),
                    len([u for u in users if u.get('status') == 'active']),
                    len(shops),
                    len([s for s in shops if s.get('status') == 'active']),
                    len(payments),
                    len(orders),
                    sum(p.get('amount', 0) for p in payments if p.get('status') == 'confirmed')
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='خلاصه اجرایی', index=False)
            
            # Style the summary sheet
            ExcelGenerator._style_worksheet(writer.sheets['خلاصه اجرایی'], "گزارش خلاصه اجرایی")
            
        except Exception as e:
            logger.error(f"Error creating summary sheet: {e}")
    
    @staticmethod
    def generate_analytics_report(analytics_data: List[Dict], title: str = "گزارش تحلیلی") -> BytesIO:
        """Generate analytics report with charts"""
        try:
            # Prepare data for different analytics
            daily_stats = {}
            event_counts = {}
            
            for event in analytics_data:
                event_date = event.get('timestamp', datetime.now()).strftime('%Y/%m/%d')
                event_type = event.get('event_type', 'unknown')
                
                # Daily statistics
                if event_date not in daily_stats:
                    daily_stats[event_date] = 0
                daily_stats[event_date] += 1
                
                # Event type counts
                if event_type not in event_counts:
                    event_counts[event_type] = 0
                event_counts[event_type] += 1
            
            # Create DataFrames
            daily_df = pd.DataFrame(list(daily_stats.items()), columns=['تاریخ', 'تعداد رویداد'])
            events_df = pd.DataFrame(list(event_counts.items()), columns=['نوع رویداد', 'تعداد'])
            
            # Create Excel file
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                daily_df.to_excel(writer, sheet_name='آمار روزانه', index=False)
                events_df.to_excel(writer, sheet_name='نوع رویدادها', index=False)
                
                # Style worksheets
                ExcelGenerator._style_worksheet(writer.sheets['آمار روزانه'], "آمار روزانه فعالیت")
                ExcelGenerator._style_worksheet(writer.sheets['نوع رویدادها'], "تحلیل نوع رویدادها")
            
            output.seek(0)
            return output
            
        except Exception as e:
            logger.error(f"Error generating analytics report: {e}")
            return BytesIO()
    
    @staticmethod
    def generate_shop_performance_report(shop_data: Dict, orders: List[Dict], products: List[Dict]) -> BytesIO:
        """Generate individual shop performance report"""
        try:
            # Shop info
            shop_info = {
                'نام فروشگاه': shop_data.get('name', ''),
                'مالک': shop_data.get('owner_id', ''),
                'پلن': shop_data.get('plan', 'free'),
                'تاریخ ایجاد': shop_data.get('created_at', datetime.now()).strftime('%Y/%m/%d') if shop_data.get('created_at') else '',
                'وضعیت': shop_data.get('status', 'pending')
            }
            
            # Orders data
            orders_data = []
            for order in orders:
                orders_data.append({
                    'شماره سفارش': order.get('order_number', ''),
                    'تاریخ': order.get('created_at', datetime.now()).strftime('%Y/%m/%d') if order.get('created_at') else '',
                    'مبلغ': order.get('totals', {}).get('total', 0),
                    'وضعیت': order.get('status', 'pending'),
                    'مشتری': order.get('customer_info', {}).get('name', '')
                })
            
            # Products data
            products_data = []
            for product in products:
                products_data.append({
                    'نام محصول': product.get('name', ''),
                    'قیمت': product.get('price', 0),
                    'موجودی': product.get('inventory', {}).get('quantity', 0),
                    'وضعیت': product.get('status', 'active'),
                    'تاریخ ایجاد': product.get('created_at', datetime.now()).strftime('%Y/%m/%d') if product.get('created_at') else ''
                })
            
            # Create Excel file
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Shop info sheet
                shop_df = pd.DataFrame([shop_info])
                shop_df.to_excel(writer, sheet_name='اطلاعات فروشگاه', index=False)
                
                # Orders sheet
                if orders_data:
                    orders_df = pd.DataFrame(orders_data)
                    orders_df.to_excel(writer, sheet_name='سفارشات', index=False)
                
                # Products sheet
                if products_data:
                    products_df = pd.DataFrame(products_data)
                    products_df.to_excel(writer, sheet_name='محصولات', index=False)
                
                # Style sheets
                for sheet_name in writer.sheets:
                    ExcelGenerator._style_worksheet(writer.sheets[sheet_name], f"گزارش {sheet_name}")
            
            output.seek(0)
            return output
            
        except Exception as e:
            logger.error(f"Error generating shop performance report: {e}")
            return BytesIO()
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, DESCENDING, TEXT
import redis.asyncio as redis
from config import Config, PLANS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global database instances
db = None
redis_client = None

class DatabaseManager:
    """Main database manager for MongoDB and Redis"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.redis = None
    
    async def connect(self):
        """Connect to MongoDB and Redis"""
        try:
            # MongoDB connection
            self.client = AsyncIOMotorClient(Config.MONGO_URI)
            self.db = self.client[Config.DATABASE_NAME]
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {Config.DATABASE_NAME}")
            
            # Redis connection
            try:
                self.redis = redis.from_url(Config.REDIS_URL)
                await self.redis.ping()
                logger.info("Connected to Redis")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}")
                self.redis = None
            
            # Initialize indexes
            await self.create_indexes()
            
            return True
            
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    async def close(self):
        """Close database connections"""
        if self.client:
            self.client.close()
        if self.redis:
            await self.redis.close()
        logger.info("Database connections closed")
    
    async def create_indexes(self):
        """Create database indexes for performance"""
        try:
            # Users indexes
            await self.db.users.create_indexes([
                IndexModel([("user_id", ASCENDING)], unique=True),
                IndexModel([("username", ASCENDING)]),
                IndexModel([("referral_code", ASCENDING)], unique=True, sparse=True),
                IndexModel([("subscription.expires_at", ASCENDING)]),
                IndexModel([("created_at", DESCENDING)]),
                IndexModel([("status", ASCENDING)])
            ])
            
            # Shops indexes
            await self.db.shops.create_indexes([
                IndexModel([("owner_id", ASCENDING)]),
                IndexModel([("bot_token", ASCENDING)], unique=True, sparse=True),
                IndexModel([("bot_username", ASCENDING)], unique=True, sparse=True),
                IndexModel([("status", ASCENDING)]),
                IndexModel([("plan", ASCENDING)]),
                IndexModel([("created_at", DESCENDING)]),
                IndexModel([("name", TEXT)])
            ])
            
            # Products indexes
            await self.db.products.create_indexes([
                IndexModel([("shop_id", ASCENDING)]),
                IndexModel([("category_id", ASCENDING)]),
                IndexModel([("status", ASCENDING)]),
                IndexModel([("price", ASCENDING)]),
                IndexModel([("created_at", DESCENDING)]),
                IndexModel([("name", TEXT), ("description", TEXT)])
            ])
            
            # Orders indexes
            await self.db.orders.create_indexes([
                IndexModel([("shop_id", ASCENDING)]),
                IndexModel([("customer_id", ASCENDING)]),
                IndexModel([("status", ASCENDING)]),
                IndexModel([("created_at", DESCENDING)]),
                IndexModel([("total_amount", ASCENDING)])
            ])
            
            # Payments indexes
            await self.db.payments.create_indexes([
                IndexModel([("user_id", ASCENDING)]),
                IndexModel([("shop_id", ASCENDING)]),
                IndexModel([("status", ASCENDING)]),
                IndexModel([("payment_type", ASCENDING)]),
                IndexModel([("created_at", DESCENDING)])
            ])
            
            # Referrals indexes
            await self.db.referrals.create_indexes([
                IndexModel([("referrer_id", ASCENDING)]),
                IndexModel([("referred_id", ASCENDING)]),
                IndexModel([("status", ASCENDING)]),
                IndexModel([("created_at", DESCENDING)])
            ])
            
            # Analytics indexes
            await self.db.analytics.create_indexes([
                IndexModel([("shop_id", ASCENDING)]),
                IndexModel([("date", DESCENDING)]),
                IndexModel([("metric_type", ASCENDING)])
            ])
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")

# Global database manager instance
db_manager = DatabaseManager()

class UserManager:
    """User management operations"""
    
    @staticmethod
    async def create_user(user_data: Dict) -> Dict:
        """Create a new user"""
        try:
            # Generate referral code
            import uuid
            referral_code = str(uuid.uuid4())[:8].upper()
            
            user_document = {
                "user_id": user_data["user_id"],
                "username": user_data.get("username"),
                "first_name": user_data.get("first_name"),
                "last_name": user_data.get("last_name"),
                "phone": user_data.get("phone"),
                "email": user_data.get("email"),
                "referral_code": referral_code,
                "referred_by": user_data.get("referred_by"),
                "subscription": {
                    "plan": "free",
                    "expires_at": datetime.utcnow() + timedelta(days=30),
                    "is_active": True,
                    "auto_renew": False
                },
                "statistics": {
                    "total_shops": 0,
                    "total_orders": 0,
                    "total_revenue": 0,
                    "total_commission_paid": 0,
                    "referral_earnings": 0
                },
                "settings": {
                    "language": "fa",
                    "notifications": True,
                    "email_notifications": False,
                    "marketing_emails": True
                },
                "permissions": {
                    "can_create_shop": True,
                    "can_use_api": False,
                    "admin_access": user_data["user_id"] == Config.ADMIN_USER_ID
                },
                "login_history": [],
                "status": "active",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await db_manager.db.users.insert_one(user_document)
            user_document["_id"] = result.inserted_id
            
            # Handle referral if exists
            if user_data.get("referred_by"):
                await UserManager.process_referral(user_data["referred_by"], user_data["user_id"])
            
            logger.info(f"User created: {user_data['user_id']}")
            return user_document
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    @staticmethod
    async def get_user(user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        try:
            return await db_manager.db.users.find_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None
    
    @staticmethod
    async def get_user_by_referral_code(referral_code: str) -> Optional[Dict]:
        """Get user by referral code"""
        try:
            return await db_manager.db.users.find_one({"referral_code": referral_code})
        except Exception as e:
            logger.error(f"Error getting user by referral code: {e}")
            return None
    
    @staticmethod
    async def update_user(user_id: int, update_data: Dict) -> bool:
        """Update user data"""
        try:
            update_data["updated_at"] = datetime.utcnow()
            result = await db_manager.db.users.update_one(
                {"user_id": user_id},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            return False
    
    @staticmethod
    async def update_subscription(user_id: int, plan: str, days: int) -> bool:
        """Update user subscription"""
        try:
            expires_at = datetime.utcnow() + timedelta(days=days)
            update_data = {
                "subscription.plan": plan,
                "subscription.expires_at": expires_at,
                "subscription.is_active": True,
                "updated_at": datetime.utcnow()
            }
            
            result = await db_manager.db.users.update_one(
                {"user_id": user_id},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating subscription for user {user_id}: {e}")
            return False
    
    @staticmethod
    async def get_all_users(skip: int = 0, limit: int = 100, filters: Dict = None) -> List[Dict]:
        """Get all users with pagination and filters"""
        try:
            query = filters or {}
            cursor = db_manager.db.users.find(query).skip(skip).limit(limit).sort("created_at", -1)
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return []
    
    @staticmethod
    async def get_users_count(filters: Dict = None) -> int:
        """Get total users count"""
        try:
            query = filters or {}
            return await db_manager.db.users.count_documents(query)
        except Exception as e:
            logger.error(f"Error counting users: {e}")
            return 0
    
    @staticmethod
    async def process_referral(referrer_code: str, referred_user_id: int) -> bool:
        """Process referral bonus"""
        try:
            referrer = await UserManager.get_user_by_referral_code(referrer_code)
            if not referrer:
                return False
            
            # Create referral record
            referral_data = {
                "referrer_id": referrer["user_id"],
                "referred_id": referred_user_id,
                "status": "pending",
                "created_at": datetime.utcnow()
            }
            
            await db_manager.db.referrals.insert_one(referral_data)
            logger.info(f"Referral processed: {referrer['user_id']} -> {referred_user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing referral: {e}")
            return False

class ShopManager:
    """Shop management operations"""
    
    @staticmethod
    async def create_shop(shop_data: Dict) -> Dict:
        """Create a new shop"""
        try:
            shop_document = {
                "owner_id": shop_data["owner_id"],
                "name": shop_data["name"],
                "description": shop_data.get("description", ""),
                "bot_token": shop_data.get("bot_token"),
                "bot_username": shop_data.get("bot_username"),
                "plan": shop_data.get("plan", "free"),
                "settings": {
                    "welcome_message": shop_data.get("welcome_message", f"🛍 به فروشگاه {shop_data['name']} خوش آمدید!"),
                    "auto_approve_orders": shop_data.get("auto_approve_orders", False),
                    "payment_methods": shop_data.get("payment_methods", ["card_to_card"]),
                    "delivery_info": shop_data.get("delivery_info", "تحویل حضوری یا پست پیشتاز"),
                    "business_hours": shop_data.get("business_hours", "شنبه تا چهارشنبه 9:00-18:00"),
                    "contact_info": {
                        "phone": shop_data.get("phone"),
                        "email": shop_data.get("email"),
                        "address": shop_data.get("address"),
                        "website": shop_data.get("website")
                    },
                    "appearance": {
                        "theme_color": "#3498db",
                        "logo_url": None,
                        "banner_url": None
                    }
                },
                "statistics": {
                    "total_products": 0,
                    "total_orders": 0,
                    "total_revenue": 0,
                    "total_customers": 0,
                    "views": 0,
                    "conversion_rate": 0.0
                },
                "features": {
                    "categories_enabled": True,
                    "discounts_enabled": PLANS[shop_data.get("plan", "free")]["discounts"],
                    "analytics_enabled": True,
                    "api_access": False
                },
                "status": "pending",  # pending, active, suspended, deleted
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await db_manager.db.shops.insert_one(shop_document)
            shop_document["_id"] = result.inserted_id
            
            logger.info(f"Shop created: {shop_data['name']} for user {shop_data['owner_id']}")
            return shop_document
            
        except Exception as e:
            logger.error(f"Error creating shop: {e}")
            raise
    
    @staticmethod
    async def get_shop(shop_id: str) -> Optional[Dict]:
        """Get shop by ID"""
        try:
            from bson import ObjectId
            return await db_manager.db.shops.find_one({"_id": ObjectId(shop_id)})
        except Exception as e:
            logger.error(f"Error getting shop {shop_id}: {e}")
            return None
    
    @staticmethod
    async def get_shop_by_owner(owner_id: int) -> Optional[Dict]:
        """Get shop by owner ID"""
        try:
            return await db_manager.db.shops.find_one({"owner_id": owner_id})
        except Exception as e:
            logger.error(f"Error getting shop for user {owner_id}: {e}")
            return None
    
    @staticmethod
    async def get_shop_by_username(bot_username: str) -> Optional[Dict]:
        """Get shop by bot username"""
        try:
            return await db_manager.db.shops.find_one({"bot_username": bot_username})
        except Exception as e:
            logger.error(f"Error getting shop by username {bot_username}: {e}")
            return None
    
    @staticmethod
    async def update_shop(shop_id: str, update_data: Dict) -> bool:
        """Update shop data"""
        try:
            from bson import ObjectId
            update_data["updated_at"] = datetime.utcnow()
            result = await db_manager.db.shops.update_one(
                {"_id": ObjectId(shop_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating shop {shop_id}: {e}")
            return False
    
    @staticmethod
    async def get_all_shops(skip: int = 0, limit: int = 100, filters: Dict = None) -> List[Dict]:
        """Get all shops with pagination"""
        try:
            query = filters or {}
            cursor = db_manager.db.shops.find(query).skip(skip).limit(limit).sort("created_at", -1)
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Error getting shops: {e}")
            return []
    
    @staticmethod
    async def get_shops_count(filters: Dict = None) -> int:
        """Get total shops count"""
        try:
            query = filters or {}
            return await db_manager.db.shops.count_documents(query)
        except Exception as e:
            logger.error(f"Error counting shops: {e}")
            return 0

class ProductManager:
    """Product management operations"""
    
    @staticmethod
    async def create_product(product_data: Dict) -> Dict:
        """Create a new product"""
        try:
            product_document = {
                "shop_id": product_data["shop_id"],
                "category_id": product_data.get("category_id"),
                "name": product_data["name"],
                "description": product_data.get("description", ""),
                "price": float(product_data["price"]),
                "original_price": float(product_data.get("original_price", product_data["price"])),
                "discount_percentage": product_data.get("discount_percentage", 0),
                "stock": int(product_data.get("stock", 0)),
                "sku": product_data.get("sku"),
                "images": product_data.get("images", []),
                "videos": product_data.get("videos", []),
                "specifications": product_data.get("specifications", {}),
                "tags": product_data.get("tags", []),
                "seo": {
                    "meta_title": product_data.get("meta_title"),
                    "meta_description": product_data.get("meta_description"),
                    "keywords": product_data.get("keywords", [])
                },
                "inventory": {
                    "track_quantity": product_data.get("track_quantity", True),
                    "allow_backorder": product_data.get("allow_backorder", False),
                    "low_stock_threshold": product_data.get("low_stock_threshold", 5)
                },
                "shipping": {
                    "weight": product_data.get("weight", 0),
                    "dimensions": product_data.get("dimensions", {}),
                    "shipping_required": product_data.get("shipping_required", True),
                    "shipping_cost": product_data.get("shipping_cost", 0)
                },
                "statistics": {
                    "views": 0,
                    "sales_count": 0,
                    "likes": 0,
                    "rating": 0.0,
                    "review_count": 0
                },
                "status": "active",  # active, inactive, draft, deleted
                "featured": product_data.get("featured", False),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await db_manager.db.products.insert_one(product_document)
            product_document["_id"] = result.inserted_id
            
            # Update shop statistics
            await ShopManager.update_shop(product_data["shop_id"], {
                "$inc": {"statistics.total_products": 1}
            })
            
            logger.info(f"Product created: {product_data['name']} in shop {product_data['shop_id']}")
            return product_document
            
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            raise
    
    @staticmethod
    async def get_product(product_id: str) -> Optional[Dict]:
        """Get product by ID"""
        try:
            from bson import ObjectId
            return await db_manager.db.products.find_one({"_id": ObjectId(product_id)})
        except Exception as e:
            logger.error(f"Error getting product {product_id}: {e}")
            return None
    
    @staticmethod
    async def get_products_by_shop(shop_id: str, skip: int = 0, limit: int = 50, filters: Dict = None) -> List[Dict]:
        """Get products by shop"""
        try:
            query = {"shop_id": shop_id, "status": {"$ne": "deleted"}}
            if filters:
                query.update(filters)
            
            cursor = db_manager.db.products.find(query).skip(skip).limit(limit).sort("created_at", -1)
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Error getting products for shop {shop_id}: {e}")
            return []
    
    @staticmethod
    async def update_product(product_id: str, update_data: Dict) -> bool:
        """Update product data"""
        try:
            from bson import ObjectId
            update_data["updated_at"] = datetime.utcnow()
            result = await db_manager.db.products.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating product {product_id}: {e}")
            return False
    
    @staticmethod
    async def get_products_count_by_shop(shop_id: str, filters: Dict = None) -> int:
        """Get products count by shop"""
        try:
            query = {"shop_id": shop_id, "status": {"$ne": "deleted"}}
            if filters:
                query.update(filters)
            return await db_manager.db.products.count_documents(query)
        except Exception as e:
            logger.error(f"Error counting products for shop {shop_id}: {e}")
            return 0

class OrderManager:
    """Order management operations"""
    
    @staticmethod
    async def create_order(order_data: Dict) -> Dict:
        """Create a new order"""
        try:
            order_document = {
                "order_number": order_data.get("order_number") or await OrderManager.generate_order_number(),
                "shop_id": order_data["shop_id"],
                "customer_id": order_data["customer_id"],
                "customer_info": {
                    "name": order_data.get("customer_name"),
                    "phone": order_data.get("customer_phone"),
                    "email": order_data.get("customer_email"),
                    "address": order_data.get("customer_address")
                },
                "items": order_data["items"],  # List of {product_id, quantity, price, name}
                "totals": {
                    "subtotal": order_data["subtotal"],
                    "shipping": order_data.get("shipping_cost", 0),
                    "tax": order_data.get("tax", 0),
                    "discount": order_data.get("discount", 0),
                    "total": order_data["total_amount"]
                },
                "payment": {
                    "method": order_data.get("payment_method", "card_to_card"),
                    "status": "pending",  # pending, paid, failed, refunded
                    "transaction_id": order_data.get("transaction_id"),
                    "receipt_image": order_data.get("receipt_image")
                },
                "shipping": {
                    "method": order_data.get("shipping_method", "standard"),
                    "address": order_data.get("shipping_address"),
                    "tracking_number": None,
                    "estimated_delivery": order_data.get("estimated_delivery")
                },
                "notes": order_data.get("notes", ""),
                "status": "pending",  # pending, confirmed, processing, shipped, delivered, cancelled
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await db_manager.db.orders.insert_one(order_document)
            order_document["_id"] = result.inserted_id
            
            logger.info(f"Order created: {order_document['order_number']} for shop {order_data['shop_id']}")
            return order_document
            
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise
    
    @staticmethod
    async def generate_order_number() -> str:
        """Generate unique order number"""
        import random
        import string
        
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        random_part = ''.join(random.choices(string.digits, k=4))
        return f"CR{timestamp}{random_part}"
    
    @staticmethod
    async def get_order(order_id: str) -> Optional[Dict]:
        """Get order by ID"""
        try:
            from bson import ObjectId
            return await db_manager.db.orders.find_one({"_id": ObjectId(order_id)})
        except Exception as e:
            logger.error(f"Error getting order {order_id}: {e}")
            return None
    
    @staticmethod
    async def get_orders_by_shop(shop_id: str, skip: int = 0, limit: int = 50, filters: Dict = None) -> List[Dict]:
        """Get orders by shop"""
        try:
            query = {"shop_id": shop_id}
            if filters:
                query.update(filters)
            
            cursor = db_manager.db.orders.find(query).skip(skip).limit(limit).sort("created_at", -1)
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Error getting orders for shop {shop_id}: {e}")
            return []
    
    @staticmethod
    async def update_order(order_id: str, update_data: Dict) -> bool:
        """Update order data"""
        try:
            from bson import ObjectId
            update_data["updated_at"] = datetime.utcnow()
            result = await db_manager.db.orders.update_one(
                {"_id": ObjectId(order_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating order {order_id}: {e}")
            return False

class PaymentManager:
    """Payment management operations"""
    
    @staticmethod
    async def create_payment(payment_data: Dict) -> Dict:
        """Create a payment record"""
        try:
            payment_document = {
                "user_id": payment_data["user_id"],
                "shop_id": payment_data.get("shop_id"),
                "order_id": payment_data.get("order_id"),
                "amount": float(payment_data["amount"]),
                "currency": payment_data.get("currency", "IRT"),  # Iranian Toman
                "payment_type": payment_data["payment_type"],  # subscription, order, commission, referral
                "payment_method": payment_data.get("payment_method", "card_to_card"),
                "gateway": payment_data.get("gateway"),
                "transaction_id": payment_data.get("transaction_id"),
                "receipt_image": payment_data.get("receipt_image"),
                "description": payment_data.get("description", ""),
                "metadata": payment_data.get("metadata", {}),
                "status": "pending",  # pending, confirmed, failed, cancelled, refunded
                "gateway_response": payment_data.get("gateway_response"),
                "verified_by": payment_data.get("verified_by"),
                "verified_at": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await db_manager.db.payments.insert_one(payment_document)
            payment_document["_id"] = result.inserted_id
            
            logger.info(f"Payment created: {payment_data['amount']} for user {payment_data['user_id']}")
            return payment_document
            
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            raise
    
    @staticmethod
    async def get_payment(payment_id: str) -> Optional[Dict]:
        """Get payment by ID"""
        try:
            from bson import ObjectId
            return await db_manager.db.payments.find_one({"_id": ObjectId(payment_id)})
        except Exception as e:
            logger.error(f"Error getting payment {payment_id}: {e}")
            return None
    
    @staticmethod
    async def get_payments_by_user(user_id: int, skip: int = 0, limit: int = 50, filters: Dict = None) -> List[Dict]:
        """Get payments by user"""
        try:
            query = {"user_id": user_id}
            if filters:
                query.update(filters)
            
            cursor = db_manager.db.payments.find(query).skip(skip).limit(limit).sort("created_at", -1)
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Error getting payments for user {user_id}: {e}")
            return []
    
    @staticmethod
    async def update_payment(payment_id: str, update_data: Dict) -> bool:
        """Update payment data"""
        try:
            from bson import ObjectId
            update_data["updated_at"] = datetime.utcnow()
            
            if update_data.get("status") == "confirmed":
                update_data["verified_at"] = datetime.utcnow()
            
            result = await db_manager.db.payments.update_one(
                {"_id": ObjectId(payment_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating payment {payment_id}: {e}")
            return False

class AnalyticsManager:
    """Analytics and reporting operations"""
    
    @staticmethod
    async def record_event(event_data: Dict) -> bool:
        """Record analytics event"""
        try:
            event_document = {
                "shop_id": event_data.get("shop_id"),
                "user_id": event_data.get("user_id"),
                "event_type": event_data["event_type"],  # page_view, product_view, order_created, etc.
                "data": event_data.get("data", {}),
                "ip_address": event_data.get("ip_address"),
                "user_agent": event_data.get("user_agent"),
                "created_at": datetime.utcnow()
            }
            
            await db_manager.db.analytics.insert_one(event_document)
            return True
            
        except Exception as e:
            logger.error(f"Error recording analytics event: {e}")
            return False
    
    @staticmethod
    async def get_shop_analytics(shop_id: str, start_date: datetime, end_date: datetime) -> Dict:
        """Get analytics for a shop"""
        try:
            pipeline = [
                {
                    "$match": {
                        "shop_id": shop_id,
                        "created_at": {"$gte": start_date, "$lte": end_date}
                    }
                },
                {
                    "$group": {
                        "_id": "$event_type",
                        "count": {"$sum": 1}
                    }
                }
            ]
            
            result = await db_manager.db.analytics.aggregate(pipeline).to_list(None)
            return {item["_id"]: item["count"] for item in result}
            
        except Exception as e:
            logger.error(f"Error getting shop analytics: {e}")
            return {}

# Database initialization functions
async def init_database():
    """Initialize database connection and setup"""
    global db, redis_client
    
    try:
        await db_manager.connect()
        db = db_manager.db
        redis_client = db_manager.redis
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def close_database():
    """Close database connections"""
    await db_manager.close()
    logger.info("Database connections closed")
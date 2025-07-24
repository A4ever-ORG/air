import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import motor.motor_asyncio
import redis.asyncio as redis
from bson import ObjectId
import pymongo
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Main database manager handling MongoDB and Redis connections"""
    
    def __init__(self):
        self.mongo_client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
        self.database: Optional[motor.motor_asyncio.AsyncIOMotorDatabase] = None
        self.redis_client: Optional[redis.Redis] = None
        
        # Managers
        self.users: Optional[UserManager] = None
        self.shops: Optional[ShopManager] = None
        self.products: Optional[ProductManager] = None
        self.orders: Optional[OrderManager] = None
        self.payments: Optional[PaymentManager] = None
        self.analytics: Optional[AnalyticsManager] = None
    
    async def connect(self):
        """Initialize database connections and managers"""
        try:
            # MongoDB connection
            self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URI)
            self.database = self.mongo_client[Config.DATABASE_NAME]
            
            # Test MongoDB connection
            await self.mongo_client.admin.command('ping')
            logger.info("✅ Connected to MongoDB")
            
            # Redis connection
            self.redis_client = redis.from_url(Config.REDIS_URL)
            await self.redis_client.ping()
            logger.info("✅ Connected to Redis")
            
            # Initialize managers
            self.users = UserManager(self.database, self.redis_client)
            self.shops = ShopManager(self.database, self.redis_client)
            self.products = ProductManager(self.database, self.redis_client)
            self.orders = OrderManager(self.database, self.redis_client)
            self.payments = PaymentManager(self.database, self.redis_client)
            self.analytics = AnalyticsManager(self.database, self.redis_client)
            
            # Create indexes
            await self._create_indexes()
            
            logger.info("✅ Database manager initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise
    
    async def disconnect(self):
        """Close database connections"""
        if self.mongo_client:
            self.mongo_client.close()
        if self.redis_client:
            await self.redis_client.close()
        logger.info("🔌 Database connections closed")
    
    async def _create_indexes(self):
        """Create database indexes for optimal performance"""
        try:
            # Users indexes
            await self.database.users.create_index("user_id", unique=True)
            await self.database.users.create_index("username")
            await self.database.users.create_index("referral_code", unique=True, sparse=True)
            await self.database.users.create_index("referred_by")
            await self.database.users.create_index("created_at")
            
            # Shops indexes
            await self.database.shops.create_index("owner_id")
            await self.database.shops.create_index("bot_username", unique=True, sparse=True)
            await self.database.shops.create_index("status")
            await self.database.shops.create_index("plan")
            await self.database.shops.create_index("created_at")
            await self.database.shops.create_index("subscription.expires_at")
            
            # Products indexes
            await self.database.products.create_index("shop_id")
            await self.database.products.create_index("sku", unique=True, sparse=True)
            await self.database.products.create_index("status")
            await self.database.products.create_index("category_id")
            await self.database.products.create_index("created_at")
            
            # Orders indexes
            await self.database.orders.create_index("shop_id")
            await self.database.orders.create_index("customer_id")
            await self.database.orders.create_index("order_number", unique=True)
            await self.database.orders.create_index("status")
            await self.database.orders.create_index("created_at")
            
            # Payments indexes
            await self.database.payments.create_index("user_id")
            await self.database.payments.create_index("shop_id")
            await self.database.payments.create_index("order_id")
            await self.database.payments.create_index("status")
            await self.database.payments.create_index("created_at")
            
            # Referrals indexes
            await self.database.referrals.create_index("referrer_id")
            await self.database.referrals.create_index("referred_id")
            await self.database.referrals.create_index("created_at")
            
            # Analytics indexes
            await self.database.analytics.create_index("event_type")
            await self.database.analytics.create_index("user_id")
            await self.database.analytics.create_index("shop_id")
            await self.database.analytics.create_index("timestamp")
            
            logger.info("✅ Database indexes created")
            
        except Exception as e:
            logger.error(f"❌ Index creation failed: {e}")

class UserManager:
    """Manages user-related database operations"""
    
    def __init__(self, database, redis_client):
        self.db = database
        self.redis = redis_client
        self.collection = database.users
    
    async def create_user(self, user_data: Dict) -> Dict:
        """Create a new user"""
        user_data.update({
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True,
            'language': Config.DEFAULT_LANGUAGE,
            'referral_count': 0,
            'total_earnings': 0,
            'last_activity': datetime.utcnow()
        })
        
        result = await self.collection.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        
        # Cache user data
        await self._cache_user(user_data)
        
        return user_data
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by Telegram user ID"""
        # Try cache first
        cached = await self.redis.get(f"user:{user_id}")
        if cached:
            import json
            return json.loads(cached)
        
        # Get from database
        user = await self.collection.find_one({"user_id": user_id})
        if user:
            user['_id'] = str(user['_id'])
            await self._cache_user(user)
        
        return user
    
    async def update_user(self, user_id: int, update_data: Dict) -> bool:
        """Update user data"""
        update_data['updated_at'] = datetime.utcnow()
        
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            # Update cache
            user = await self.get_user(user_id)
            if user:
                await self._cache_user(user)
        
        return result.modified_count > 0
    
    async def get_user_by_referral_code(self, referral_code: str) -> Optional[Dict]:
        """Get user by referral code"""
        return await self.collection.find_one({"referral_code": referral_code})
    
    async def update_last_activity(self, user_id: int):
        """Update user's last activity timestamp"""
        await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"last_activity": datetime.utcnow()}}
        )
    
    async def get_users_stats(self) -> Dict:
        """Get user statistics"""
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_users": {"$sum": 1},
                    "active_users": {
                        "$sum": {
                            "$cond": [
                                {"$gte": ["$last_activity", datetime.utcnow() - timedelta(days=30)]},
                                1, 0
                            ]
                        }
                    }
                }
            }
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(1)
        return result[0] if result else {"total_users": 0, "active_users": 0}
    
    async def _cache_user(self, user_data: Dict):
        """Cache user data in Redis"""
        import json
        await self.redis.setex(
            f"user:{user_data['user_id']}", 
            Config.CACHE_TTL, 
            json.dumps(user_data, default=str)
        )

class ShopManager:
    """Manages shop-related database operations"""
    
    def __init__(self, database, redis_client):
        self.db = database
        self.redis = redis_client
        self.collection = database.shops
    
    async def create_shop(self, shop_data: Dict) -> Dict:
        """Create a new shop"""
        shop_data.update({
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'status': 'pending',  # pending, active, suspended, deleted
            'plan': 'free',
            'products_count': 0,
            'orders_count': 0,
            'total_revenue': 0,
            'settings': {
                'auto_messages': False,
                'notifications': True,
                'public_catalog': True
            },
            'features': {
                'discounts': False,
                'analytics': True,
                'custom_domain': False
            },
            'subscription': {
                'started_at': datetime.utcnow(),
                'expires_at': datetime.utcnow() + timedelta(days=30),
                'auto_renewal': False
            }
        })
        
        result = await self.collection.insert_one(shop_data)
        shop_data['_id'] = result.inserted_id
        
        return shop_data
    
    async def get_shop(self, shop_id: str) -> Optional[Dict]:
        """Get shop by ID"""
        try:
            shop = await self.collection.find_one({"_id": ObjectId(shop_id)})
            if shop:
                shop['_id'] = str(shop['_id'])
            return shop
        except:
            return None
    
    async def get_shop_by_owner(self, owner_id: int) -> Optional[Dict]:
        """Get shop by owner user ID"""
        shop = await self.collection.find_one({"owner_id": owner_id})
        if shop:
            shop['_id'] = str(shop['_id'])
        return shop
    
    async def update_shop(self, shop_id: str, update_data: Dict) -> bool:
        """Update shop data"""
        update_data['updated_at'] = datetime.utcnow()
        
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(shop_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    async def get_shops_by_status(self, status: str) -> List[Dict]:
        """Get shops by status"""
        shops = []
        async for shop in self.collection.find({"status": status}):
            shop['_id'] = str(shop['_id'])
            shops.append(shop)
        return shops
    
    async def get_expiring_subscriptions(self, days: int = 3) -> List[Dict]:
        """Get shops with subscriptions expiring in specified days"""
        expiry_threshold = datetime.utcnow() + timedelta(days=days)
        shops = []
        
        async for shop in self.collection.find({
            "subscription.expires_at": {"$lte": expiry_threshold},
            "status": "active"
        }):
            shop['_id'] = str(shop['_id'])
            shops.append(shop)
        
        return shops
    
    async def get_shops_stats(self) -> Dict:
        """Get shop statistics"""
        pipeline = [
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1}
                }
            }
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(None)
        stats = {item['_id']: item['count'] for item in result}
        
        # Add plan statistics
        plan_pipeline = [
            {
                "$group": {
                    "_id": "$plan",
                    "count": {"$sum": 1}
                }
            }
        ]
        
        plan_result = await self.collection.aggregate(plan_pipeline).to_list(None)
        plan_stats = {item['_id']: item['count'] for item in plan_result}
        
        return {
            "by_status": stats,
            "by_plan": plan_stats,
            "total": sum(stats.values())
        }

class ProductManager:
    """Manages product-related database operations"""
    
    def __init__(self, database, redis_client):
        self.db = database
        self.redis = redis_client
        self.collection = database.products
    
    async def create_product(self, product_data: Dict) -> Dict:
        """Create a new product"""
        product_data.update({
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'status': 'active',  # active, inactive, out_of_stock
            'views': 0,
            'orders': 0,
            'inventory': {
                'track_quantity': False,
                'quantity': 0,
                'low_stock_threshold': 5
            },
            'shipping': {
                'weight': 0,
                'dimensions': {'length': 0, 'width': 0, 'height': 0},
                'free_shipping': False,
                'shipping_cost': 0
            },
            'seo': {
                'meta_title': product_data.get('name', ''),
                'meta_description': product_data.get('description', '')[:160],
                'keywords': []
            }
        })
        
        result = await self.collection.insert_one(product_data)
        product_data['_id'] = result.inserted_id
        
        # Update shop products count
        await self.db.shops.update_one(
            {"_id": ObjectId(product_data['shop_id'])},
            {"$inc": {"products_count": 1}}
        )
        
        return product_data
    
    async def get_product(self, product_id: str) -> Optional[Dict]:
        """Get product by ID"""
        try:
            product = await self.collection.find_one({"_id": ObjectId(product_id)})
            if product:
                product['_id'] = str(product['_id'])
            return product
        except:
            return None
    
    async def get_shop_products(self, shop_id: str, status: str = None) -> List[Dict]:
        """Get products for a shop"""
        query = {"shop_id": shop_id}
        if status:
            query["status"] = status
        
        products = []
        async for product in self.collection.find(query).sort("created_at", -1):
            product['_id'] = str(product['_id'])
            products.append(product)
        
        return products
    
    async def update_product(self, product_id: str, update_data: Dict) -> bool:
        """Update product data"""
        update_data['updated_at'] = datetime.utcnow()
        
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    async def delete_product(self, product_id: str, shop_id: str) -> bool:
        """Delete a product"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(product_id)})
            
            if result.deleted_count > 0:
                # Update shop products count
                await self.db.shops.update_one(
                    {"_id": ObjectId(shop_id)},
                    {"$inc": {"products_count": -1}}
                )
            
            return result.deleted_count > 0
        except:
            return False
    
    async def increment_views(self, product_id: str):
        """Increment product view count"""
        try:
            await self.collection.update_one(
                {"_id": ObjectId(product_id)},
                {"$inc": {"views": 1}}
            )
        except:
            pass

class OrderManager:
    """Manages order-related database operations"""
    
    def __init__(self, database, redis_client):
        self.db = database
        self.redis = redis_client
        self.collection = database.orders
    
    async def create_order(self, order_data: Dict) -> Dict:
        """Create a new order"""
        # Generate order number
        order_count = await self.collection.count_documents({})
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{order_count + 1:04d}"
        
        order_data.update({
            'order_number': order_number,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'status': 'pending',  # pending, confirmed, processing, shipped, delivered, cancelled
            'customer_info': {
                'user_id': order_data.get('customer_id'),
                'name': '',
                'phone': '',
                'address': '',
                'notes': ''
            },
            'totals': {
                'subtotal': 0,
                'shipping': 0,
                'discount': 0,
                'total': 0
            },
            'payment': {
                'method': 'card_to_card',
                'status': 'pending',
                'amount': 0,
                'reference_id': ''
            },
            'shipping': {
                'method': 'standard',
                'tracking_number': '',
                'estimated_delivery': None
            }
        })
        
        result = await self.collection.insert_one(order_data)
        order_data['_id'] = result.inserted_id
        
        # Update shop orders count
        await self.db.shops.update_one(
            {"_id": ObjectId(order_data['shop_id'])},
            {"$inc": {"orders_count": 1}}
        )
        
        return order_data
    
    async def get_order(self, order_id: str) -> Optional[Dict]:
        """Get order by ID"""
        try:
            order = await self.collection.find_one({"_id": ObjectId(order_id)})
            if order:
                order['_id'] = str(order['_id'])
            return order
        except:
            return None
    
    async def get_shop_orders(self, shop_id: str, status: str = None) -> List[Dict]:
        """Get orders for a shop"""
        query = {"shop_id": shop_id}
        if status:
            query["status"] = status
        
        orders = []
        async for order in self.collection.find(query).sort("created_at", -1):
            order['_id'] = str(order['_id'])
            orders.append(order)
        
        return orders
    
    async def get_user_orders(self, user_id: int) -> List[Dict]:
        """Get orders for a user"""
        orders = []
        async for order in self.collection.find({"customer_id": user_id}).sort("created_at", -1):
            order['_id'] = str(order['_id'])
            orders.append(order)
        
        return orders
    
    async def update_order_status(self, order_id: str, status: str) -> bool:
        """Update order status"""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(order_id)},
                {
                    "$set": {
                        "status": status,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except:
            return False

class PaymentManager:
    """Manages payment-related database operations"""
    
    def __init__(self, database, redis_client):
        self.db = database
        self.redis = redis_client
        self.collection = database.payments
    
    async def create_payment(self, payment_data: Dict) -> Dict:
        """Create a new payment record"""
        payment_data.update({
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'status': 'pending',  # pending, completed, failed, refunded
            'payment_type': 'subscription',  # subscription, order, commission
            'currency': 'IRR',
            'gateway': 'card_to_card',
            'metadata': {}
        })
        
        result = await self.collection.insert_one(payment_data)
        payment_data['_id'] = result.inserted_id
        
        return payment_data
    
    async def get_payment(self, payment_id: str) -> Optional[Dict]:
        """Get payment by ID"""
        try:
            payment = await self.collection.find_one({"_id": ObjectId(payment_id)})
            if payment:
                payment['_id'] = str(payment['_id'])
            return payment
        except:
            return None
    
    async def get_user_payments(self, user_id: int) -> List[Dict]:
        """Get payments for a user"""
        payments = []
        async for payment in self.collection.find({"user_id": user_id}).sort("created_at", -1):
            payment['_id'] = str(payment['_id'])
            payments.append(payment)
        
        return payments
    
    async def update_payment_status(self, payment_id: str, status: str, reference_id: str = None) -> bool:
        """Update payment status"""
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow()
        }
        
        if reference_id:
            update_data["reference_id"] = reference_id
        
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(payment_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    async def get_payments_stats(self, start_date: datetime = None, end_date: datetime = None) -> Dict:
        """Get payment statistics"""
        query = {}
        if start_date and end_date:
            query["created_at"] = {"$gte": start_date, "$lte": end_date}
        
        pipeline = [
            {"$match": query},
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1},
                    "total_amount": {"$sum": "$amount"}
                }
            }
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(None)
        return {item['_id']: {"count": item['count'], "amount": item['total_amount']} for item in result}

class AnalyticsManager:
    """Manages analytics and tracking"""
    
    def __init__(self, database, redis_client):
        self.db = database
        self.redis = redis_client
        self.collection = database.analytics
    
    async def record_event(self, event_type: str, user_id: int = None, shop_id: str = None, data: Dict = None):
        """Record an analytics event"""
        event = {
            'event_type': event_type,
            'user_id': user_id,
            'shop_id': shop_id,
            'data': data or {},
            'timestamp': datetime.utcnow()
        }
        
        await self.collection.insert_one(event)
    
    async def get_events(self, event_type: str = None, start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
        """Get analytics events"""
        query = {}
        
        if event_type:
            query["event_type"] = event_type
        
        if start_date and end_date:
            query["timestamp"] = {"$gte": start_date, "$lte": end_date}
        
        events = []
        async for event in self.collection.find(query).sort("timestamp", -1):
            event['_id'] = str(event['_id'])
            events.append(event)
        
        return events
    
    async def get_daily_stats(self, date: datetime = None) -> Dict:
        """Get daily statistics"""
        if not date:
            date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        start_date = date
        end_date = date + timedelta(days=1)
        
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": start_date, "$lt": end_date}
                }
            },
            {
                "$group": {
                    "_id": "$event_type",
                    "count": {"$sum": 1}
                }
            }
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(None)
        return {item['_id']: item['count'] for item in result}

# Global database instance
db_manager = DatabaseManager()
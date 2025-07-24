import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import logging
from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(Config.MONGO_URI)
            self.db = self.client[Config.DATABASE_NAME]
            
            # Create indexes
            await self.create_indexes()
            logger.info("Connected to MongoDB successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def create_indexes(self):
        """Create database indexes for better performance"""
        try:
            # Users collection indexes
            await self.db.users.create_index("user_id", unique=True)
            await self.db.users.create_index("username")
            await self.db.users.create_index("phone")
            await self.db.users.create_index("subscription.plan")
            await self.db.users.create_index("subscription.expires_at")
            
            # Shops collection indexes
            await self.db.shops.create_index("owner_id")
            await self.db.shops.create_index("bot_token", unique=True)
            await self.db.shops.create_index("status")
            await self.db.shops.create_index("created_at")
            
            # Products collection indexes
            await self.db.products.create_index("shop_id")
            await self.db.products.create_index("category")
            await self.db.products.create_index("status")
            await self.db.products.create_index("created_at")
            
            # Orders collection indexes
            await self.db.orders.create_index("shop_id")
            await self.db.orders.create_index("customer_id")
            await self.db.orders.create_index("status")
            await self.db.orders.create_index("created_at")
            
            # Payments collection indexes
            await self.db.payments.create_index("user_id")
            await self.db.payments.create_index("shop_id")
            await self.db.payments.create_index("payment_type")
            await self.db.payments.create_index("status")
            await self.db.payments.create_index("created_at")
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create indexes: {e}")
    
    async def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("Database connection closed")

# Global database instance
db = Database()

class UserManager:
    """User management operations"""
    
    @staticmethod
    async def create_user(user_data: Dict) -> Dict:
        """Create a new user"""
        user_data.update({
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "subscription": {
                "plan": "free",
                "expires_at": datetime.utcnow() + timedelta(days=30),
                "is_active": True
            },
            "statistics": {
                "total_orders": 0,
                "total_revenue": 0,
                "total_commission_paid": 0
            },
            "status": "active"
        })
        
        result = await db.db.users.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        return user_data
    
    @staticmethod
    async def get_user(user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        return await db.db.users.find_one({"user_id": user_id})
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[Dict]:
        """Get user by username"""
        return await db.db.users.find_one({"username": username})
    
    @staticmethod
    async def update_user(user_id: int, update_data: Dict) -> bool:
        """Update user data"""
        update_data["updated_at"] = datetime.utcnow()
        result = await db.db.users.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    async def get_all_users(skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all users with pagination"""
        cursor = db.db.users.find().skip(skip).limit(limit).sort("created_at", DESCENDING)
        return await cursor.to_list(length=limit)
    
    @staticmethod
    async def get_users_count() -> int:
        """Get total users count"""
        return await db.db.users.count_documents({})
    
    @staticmethod
    async def update_subscription(user_id: int, plan: str, days: int) -> bool:
        """Update user subscription"""
        expires_at = datetime.utcnow() + timedelta(days=days)
        update_data = {
            "subscription.plan": plan,
            "subscription.expires_at": expires_at,
            "subscription.is_active": True,
            "updated_at": datetime.utcnow()
        }
        
        result = await db.db.users.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        return result.modified_count > 0

class ShopManager:
    """Shop management operations"""
    
    @staticmethod
    async def create_shop(shop_data: Dict) -> Dict:
        """Create a new shop"""
        shop_data.update({
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "pending",  # pending, active, suspended
            "statistics": {
                "total_products": 0,
                "total_orders": 0,
                "total_revenue": 0
            }
        })
        
        result = await db.db.shops.insert_one(shop_data)
        shop_data["_id"] = result.inserted_id
        return shop_data
    
    @staticmethod
    async def get_shop(shop_id: str) -> Optional[Dict]:
        """Get shop by ID"""
        from bson import ObjectId
        return await db.db.shops.find_one({"_id": ObjectId(shop_id)})
    
    @staticmethod
    async def get_shop_by_owner(owner_id: int) -> Optional[Dict]:
        """Get shop by owner ID"""
        return await db.db.shops.find_one({"owner_id": owner_id})
    
    @staticmethod
    async def get_shop_by_token(bot_token: str) -> Optional[Dict]:
        """Get shop by bot token"""
        return await db.db.shops.find_one({"bot_token": bot_token})
    
    @staticmethod
    async def update_shop(shop_id: str, update_data: Dict) -> bool:
        """Update shop data"""
        from bson import ObjectId
        update_data["updated_at"] = datetime.utcnow()
        result = await db.db.shops.update_one(
            {"_id": ObjectId(shop_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    async def get_all_shops(skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all shops with pagination"""
        cursor = db.db.shops.find().skip(skip).limit(limit).sort("created_at", DESCENDING)
        return await cursor.to_list(length=limit)
    
    @staticmethod
    async def get_shops_count() -> int:
        """Get total shops count"""
        return await db.db.shops.count_documents({})

class ProductManager:
    """Product management operations"""
    
    @staticmethod
    async def create_product(product_data: Dict) -> Dict:
        """Create a new product"""
        product_data.update({
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "active",  # active, inactive, deleted
            "sales_count": 0,
            "views_count": 0
        })
        
        result = await db.db.products.insert_one(product_data)
        product_data["_id"] = result.inserted_id
        return product_data
    
    @staticmethod
    async def get_product(product_id: str) -> Optional[Dict]:
        """Get product by ID"""
        from bson import ObjectId
        return await db.db.products.find_one({"_id": ObjectId(product_id)})
    
    @staticmethod
    async def get_products_by_shop(shop_id: str, skip: int = 0, limit: int = 50) -> List[Dict]:
        """Get products by shop ID"""
        cursor = db.db.products.find({"shop_id": shop_id, "status": {"$ne": "deleted"}})
        cursor = cursor.skip(skip).limit(limit).sort("created_at", DESCENDING)
        return await cursor.to_list(length=limit)
    
    @staticmethod
    async def update_product(product_id: str, update_data: Dict) -> bool:
        """Update product data"""
        from bson import ObjectId
        update_data["updated_at"] = datetime.utcnow()
        result = await db.db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    async def get_products_count_by_shop(shop_id: str) -> int:
        """Get products count by shop"""
        return await db.db.products.count_documents({"shop_id": shop_id, "status": {"$ne": "deleted"}})

class OrderManager:
    """Order management operations"""
    
    @staticmethod
    async def create_order(order_data: Dict) -> Dict:
        """Create a new order"""
        order_data.update({
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "pending"  # pending, confirmed, cancelled, completed
        })
        
        result = await db.db.orders.insert_one(order_data)
        order_data["_id"] = result.inserted_id
        return order_data
    
    @staticmethod
    async def get_order(order_id: str) -> Optional[Dict]:
        """Get order by ID"""
        from bson import ObjectId
        return await db.db.orders.find_one({"_id": ObjectId(order_id)})
    
    @staticmethod
    async def get_orders_by_shop(shop_id: str, skip: int = 0, limit: int = 50) -> List[Dict]:
        """Get orders by shop ID"""
        cursor = db.db.orders.find({"shop_id": shop_id})
        cursor = cursor.skip(skip).limit(limit).sort("created_at", DESCENDING)
        return await cursor.to_list(length=limit)
    
    @staticmethod
    async def update_order(order_id: str, update_data: Dict) -> bool:
        """Update order data"""
        from bson import ObjectId
        update_data["updated_at"] = datetime.utcnow()
        result = await db.db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

class PaymentManager:
    """Payment management operations"""
    
    @staticmethod
    async def create_payment(payment_data: Dict) -> Dict:
        """Create a new payment record"""
        payment_data.update({
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "pending"  # pending, confirmed, failed
        })
        
        result = await db.db.payments.insert_one(payment_data)
        payment_data["_id"] = result.inserted_id
        return payment_data
    
    @staticmethod
    async def get_payment(payment_id: str) -> Optional[Dict]:
        """Get payment by ID"""
        from bson import ObjectId
        return await db.db.payments.find_one({"_id": ObjectId(payment_id)})
    
    @staticmethod
    async def get_payments_by_user(user_id: int, skip: int = 0, limit: int = 50) -> List[Dict]:
        """Get payments by user ID"""
        cursor = db.db.payments.find({"user_id": user_id})
        cursor = cursor.skip(skip).limit(limit).sort("created_at", DESCENDING)
        return await cursor.to_list(length=limit)
    
    @staticmethod
    async def update_payment(payment_id: str, update_data: Dict) -> bool:
        """Update payment data"""
        from bson import ObjectId
        update_data["updated_at"] = datetime.utcnow()
        result = await db.db.payments.update_one(
            {"_id": ObjectId(payment_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

# Initialize database connection
async def init_database():
    """Initialize database connection"""
    await db.connect()

# Close database connection
async def close_database():
    """Close database connection"""
    await db.close()
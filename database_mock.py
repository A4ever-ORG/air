import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from config import PLANS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for demo
demo_data = {
    "users": {},
    "shops": {},
    "products": {},
    "orders": {},
    "payments": {}
}

class MockDatabase:
    def __init__(self):
        self.connected = False
        
    async def connect(self):
        """Mock database connection"""
        self.connected = True
        logger.info("Connected to Mock Database successfully")
    
    async def close(self):
        """Mock database close"""
        self.connected = False
        logger.info("Mock Database connection closed")

# Global database instance
db = MockDatabase()

class UserManager:
    """Mock User management operations"""
    
    @staticmethod
    async def create_user(user_data: Dict) -> Dict:
        """Create a new user in memory"""
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
        
        user_id = user_data["user_id"]
        demo_data["users"][user_id] = user_data
        return user_data
    
    @staticmethod
    async def get_user(user_id: int) -> Optional[Dict]:
        """Get user by ID from memory"""
        return demo_data["users"].get(user_id)
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[Dict]:
        """Get user by username from memory"""
        for user in demo_data["users"].values():
            if user.get("username") == username:
                return user
        return None
    
    @staticmethod
    async def update_user(user_id: int, update_data: Dict) -> bool:
        """Update user data in memory"""
        if user_id in demo_data["users"]:
            update_data["updated_at"] = datetime.utcnow()
            demo_data["users"][user_id].update(update_data)
            return True
        return False
    
    @staticmethod
    async def get_all_users(skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all users with pagination from memory"""
        users = list(demo_data["users"].values())
        return users[skip:skip+limit]
    
    @staticmethod
    async def get_users_count() -> int:
        """Get total users count from memory"""
        return len(demo_data["users"])
    
    @staticmethod
    async def update_subscription(user_id: int, plan: str, days: int) -> bool:
        """Update user subscription in memory"""
        if user_id in demo_data["users"]:
            expires_at = datetime.utcnow() + timedelta(days=days)
            demo_data["users"][user_id]["subscription"] = {
                "plan": plan,
                "expires_at": expires_at,
                "is_active": True
            }
            demo_data["users"][user_id]["updated_at"] = datetime.utcnow()
            return True
        return False

class ShopManager:
    """Mock Shop management operations"""
    
    @staticmethod
    async def create_shop(shop_data: Dict) -> Dict:
        """Create a new shop in memory"""
        shop_id = f"shop_{len(demo_data['shops']) + 1}"
        shop_data.update({
            "_id": shop_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "active",  # Auto-approve for demo
            "statistics": {
                "total_products": 0,
                "total_orders": 0,
                "total_revenue": 0
            }
        })
        
        demo_data["shops"][shop_id] = shop_data
        return shop_data
    
    @staticmethod
    async def get_shop(shop_id: str) -> Optional[Dict]:
        """Get shop by ID from memory"""
        return demo_data["shops"].get(shop_id)
    
    @staticmethod
    async def get_shop_by_owner(owner_id: int) -> Optional[Dict]:
        """Get shop by owner ID from memory"""
        for shop in demo_data["shops"].values():
            if shop.get("owner_id") == owner_id:
                return shop
        return None
    
    @staticmethod
    async def get_shop_by_token(bot_token: str) -> Optional[Dict]:
        """Get shop by bot token from memory"""
        for shop in demo_data["shops"].values():
            if shop.get("bot_token") == bot_token:
                return shop
        return None
    
    @staticmethod
    async def update_shop(shop_id: str, update_data: Dict) -> bool:
        """Update shop data in memory"""
        if shop_id in demo_data["shops"]:
            update_data["updated_at"] = datetime.utcnow()
            demo_data["shops"][shop_id].update(update_data)
            return True
        return False
    
    @staticmethod
    async def get_all_shops(skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all shops with pagination from memory"""
        shops = list(demo_data["shops"].values())
        return shops[skip:skip+limit]
    
    @staticmethod
    async def get_shops_count() -> int:
        """Get total shops count from memory"""
        return len(demo_data["shops"])

class ProductManager:
    """Mock Product management operations"""
    
    @staticmethod
    async def create_product(product_data: Dict) -> Dict:
        """Create a new product in memory"""
        product_id = f"product_{len(demo_data['products']) + 1}"
        product_data.update({
            "_id": product_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "active",
            "sales_count": 0,
            "views_count": 0
        })
        
        demo_data["products"][product_id] = product_data
        return product_data
    
    @staticmethod
    async def get_product(product_id: str) -> Optional[Dict]:
        """Get product by ID from memory"""
        return demo_data["products"].get(product_id)
    
    @staticmethod
    async def get_products_by_shop(shop_id: str, skip: int = 0, limit: int = 50) -> List[Dict]:
        """Get products by shop ID from memory"""
        products = [p for p in demo_data["products"].values() 
                   if p.get("shop_id") == shop_id and p.get("status") != "deleted"]
        return products[skip:skip+limit]
    
    @staticmethod
    async def update_product(product_id: str, update_data: Dict) -> bool:
        """Update product data in memory"""
        if product_id in demo_data["products"]:
            update_data["updated_at"] = datetime.utcnow()
            demo_data["products"][product_id].update(update_data)
            return True
        return False
    
    @staticmethod
    async def get_products_count_by_shop(shop_id: str) -> int:
        """Get products count by shop from memory"""
        return len([p for p in demo_data["products"].values() 
                   if p.get("shop_id") == shop_id and p.get("status") != "deleted"])

class OrderManager:
    """Mock Order management operations"""
    
    @staticmethod
    async def create_order(order_data: Dict) -> Dict:
        """Create a new order in memory"""
        order_id = f"order_{len(demo_data['orders']) + 1}"
        order_data.update({
            "_id": order_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "pending"
        })
        
        demo_data["orders"][order_id] = order_data
        return order_data
    
    @staticmethod
    async def get_order(order_id: str) -> Optional[Dict]:
        """Get order by ID from memory"""
        return demo_data["orders"].get(order_id)
    
    @staticmethod
    async def get_orders_by_shop(shop_id: str, skip: int = 0, limit: int = 50) -> List[Dict]:
        """Get orders by shop ID from memory"""
        orders = [o for o in demo_data["orders"].values() if o.get("shop_id") == shop_id]
        return orders[skip:skip+limit]
    
    @staticmethod
    async def update_order(order_id: str, update_data: Dict) -> bool:
        """Update order data in memory"""
        if order_id in demo_data["orders"]:
            update_data["updated_at"] = datetime.utcnow()
            demo_data["orders"][order_id].update(update_data)
            return True
        return False

class PaymentManager:
    """Mock Payment management operations"""
    
    @staticmethod
    async def create_payment(payment_data: Dict) -> Dict:
        """Create a new payment record in memory"""
        payment_id = f"payment_{len(demo_data['payments']) + 1}"
        payment_data.update({
            "_id": payment_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "confirmed"  # Auto-confirm for demo
        })
        
        demo_data["payments"][payment_id] = payment_data
        return payment_data
    
    @staticmethod
    async def get_payment(payment_id: str) -> Optional[Dict]:
        """Get payment by ID from memory"""
        return demo_data["payments"].get(payment_id)
    
    @staticmethod
    async def get_payments_by_user(user_id: int, skip: int = 0, limit: int = 50) -> List[Dict]:
        """Get payments by user ID from memory"""
        payments = [p for p in demo_data["payments"].values() if p.get("user_id") == user_id]
        return payments[skip:skip+limit]
    
    @staticmethod
    async def update_payment(payment_id: str, update_data: Dict) -> bool:
        """Update payment data in memory"""
        if payment_id in demo_data["payments"]:
            update_data["updated_at"] = datetime.utcnow()
            demo_data["payments"][payment_id].update(update_data)
            return True
        return False

# Initialize database connection
async def init_database():
    """Initialize mock database connection"""
    await db.connect()
    
    # Add some demo data
    demo_user = {
        "user_id": 123456789,
        "username": "demo_user",
        "first_name": "کاربر",
        "last_name": "دمو",
        "phone": "09123456789"
    }
    await UserManager.create_user(demo_user)
    
    demo_shop = {
        "owner_id": 123456789,
        "name": "فروشگاه دمو",
        "bot_token": "123456789:demo_token_for_testing",
        "bot_username": "demo_shop_bot",
        "plan": "professional"
    }
    await ShopManager.create_shop(demo_shop)
    
    logger.info("Demo data initialized")

# Close database connection
async def close_database():
    """Close mock database connection"""
    await db.close()
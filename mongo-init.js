// MongoDB initialization script for CodeRoot Bot
// This script will run when the MongoDB container starts for the first time

// Switch to the coderoot_bot database
db = db.getSiblingDB('coderoot_bot');

// Create collections with initial indexes
print('Creating users collection...');
db.createCollection('users');
db.users.createIndex({ "user_id": 1 }, { unique: true });
db.users.createIndex({ "username": 1 });
db.users.createIndex({ "phone": 1 });
db.users.createIndex({ "subscription.plan": 1 });
db.users.createIndex({ "subscription.expires_at": 1 });
db.users.createIndex({ "created_at": 1 });

print('Creating shops collection...');
db.createCollection('shops');
db.shops.createIndex({ "owner_id": 1 });
db.shops.createIndex({ "bot_token": 1 }, { unique: true });
db.shops.createIndex({ "status": 1 });
db.shops.createIndex({ "created_at": 1 });

print('Creating products collection...');
db.createCollection('products');
db.products.createIndex({ "shop_id": 1 });
db.products.createIndex({ "category": 1 });
db.products.createIndex({ "status": 1 });
db.products.createIndex({ "created_at": 1 });

print('Creating orders collection...');
db.createCollection('orders');
db.orders.createIndex({ "shop_id": 1 });
db.orders.createIndex({ "customer_id": 1 });
db.orders.createIndex({ "status": 1 });
db.orders.createIndex({ "created_at": 1 });

print('Creating payments collection...');
db.createCollection('payments');
db.payments.createIndex({ "user_id": 1 });
db.payments.createIndex({ "shop_id": 1 });
db.payments.createIndex({ "payment_type": 1 });
db.payments.createIndex({ "status": 1 });
db.payments.createIndex({ "created_at": 1 });

print('MongoDB initialization completed successfully!');
print('Database: coderoot_bot');
print('Collections created: users, shops, products, orders, payments');
print('Indexes created for better performance');

// Insert a sample admin user (optional)
// Uncomment and modify the following lines if needed
/*
db.users.insertOne({
    user_id: 123456789,
    username: "admin",
    first_name: "Admin",
    last_name: "User",
    phone: null,
    created_at: new Date(),
    updated_at: new Date(),
    subscription: {
        plan: "vip",
        expires_at: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000), // 1 year from now
        is_active: true
    },
    statistics: {
        total_orders: 0,
        total_revenue: 0,
        total_commission_paid: 0
    },
    status: "active"
});
print('Sample admin user created');
*/
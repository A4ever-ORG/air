# Render Deployment Guide for CodeRoot Bot

## 🚨 Current Issue
Your application is failing to deploy on Render because it's trying to connect to `localhost:27017` (MongoDB) and `localhost:6379` (Redis), but Render doesn't provide local database services. You need to use cloud database services.

## 📋 Step-by-Step Solution

### 1. Create MongoDB Database on Render

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Sign in to your account

2. **Create MongoDB Service**
   - Click "New" → "MongoDB"
   - Name: `coderoot-mongodb`
   - Region: `Oregon` (same as your web service)
   - Plan: `Starter` (free tier)
   - Click "Create Database"

3. **Get MongoDB Connection String**
   - Go to your MongoDB service
   - Click "Connect" tab
   - Copy the "External Database URL"
   - It will look like: `mongodb+srv://username:password@cluster.render.com/database`

### 2. Create Redis Database on Render

1. **Create Redis Service**
   - Click "New" → "Redis"
   - Name: `coderoot-redis`
   - Region: `Oregon` (same as your web service)
   - Plan: `Starter` (free tier)
   - Click "Create Redis"

2. **Get Redis Connection String**
   - Go to your Redis service
   - Click "Connect" tab
   - Copy the "External Database URL"
   - It will look like: `redis://username:password@cluster.render.com:6379`

### 3. Update Environment Variables

1. **Go to Your Web Service**
   - Navigate to your `coderoot-bot` web service
   - Click "Environment" tab

2. **Add/Update These Environment Variables:**

```bash
# Required Bot Configuration
BOT_TOKEN=7680510409:AAEHRgIrfH7FeuEa5qr2rFG6vGbfkVMxnVM
API_ID=17064702
API_HASH=f65880b9eededbee85346f874819bbc5
BOT_USERNAME=Code_Root_Bot

# Admin Configuration
ADMIN_USER_ID=7707164235
ADMIN_USERNAME=A4everr

# Database Configuration (REPLACE WITH YOUR ACTUAL CONNECTION STRINGS)
MONGO_URI=mongodb+srv://your-username:your-password@your-mongodb-cluster.render.com/database
REDIS_URL=redis://your-username:your-password@your-redis-cluster.render.com:6379
DATABASE_NAME=coderoot_bot

# Server Configuration
SERVER_PORT=8080
SERVER_HOST=0.0.0.0
PORT=8080

# Environment Configuration
ENVIRONMENT=production
DEMO_MODE=false
PRODUCTION_MODE=true
DOCKER_ENV=true
DEBUG=false

# Language and Logging
DEFAULT_LANGUAGE=fa
LOG_LEVEL=info
LOG_FILE=logs/app.log

# Payment Configuration
CARD_NUMBER=your_card_number
CARD_HOLDER_NAME=your_card_holder_name

# Channel Configuration
MAIN_CHANNEL_ID=your_main_channel_id
MAIN_CHANNEL_USERNAME=your_main_channel_username

# Pricing Configuration
PROFESSIONAL_PLAN_PRICE=50000
VIP_PLAN_PRICE=100000
COMMISSION_RATE=10

# Webhook Configuration
WEBHOOK_URL=https://your-domain.com/webhook
```

### 4. Alternative: Use External Database Services

If you prefer external services instead of Render's databases:

#### MongoDB Atlas (Free Tier)
1. Sign up at https://www.mongodb.com/atlas
2. Create a free cluster
3. Get connection string and use for `MONGO_URI`

#### Redis Cloud (Free Tier)
1. Sign up at https://redis.com/try-free/
2. Create a free database
3. Get connection string and use for `REDIS_URL`

### 5. Test Your Configuration

After setting up the databases and environment variables:

1. **Redeploy Your Service**
   - Go to your web service
   - Click "Manual Deploy" → "Deploy latest commit"

2. **Check Logs**
   - Monitor the deployment logs
   - Look for successful database connections

3. **Expected Success Messages**
   ```
   🔌 Attempting to connect to MongoDB...
   📍 MongoDB URI: mongodb+srv://username:***@cluster.render.com/database
   ✅ Connected to MongoDB: coderoot_bot
   
   🔌 Attempting to connect to Redis...
   📍 Redis URL: redis://username:***@cluster.render.com:6379
   ✅ Connected to Redis
   ```

### 6. Troubleshooting

#### Common Issues:

1. **"connection refused" error**
   - Make sure you're using the external connection strings, not localhost
   - Check that your database services are running on Render

2. **"authentication failed" error**
   - Verify your username and password in the connection strings
   - Make sure you copied the entire connection string correctly

3. **"timeout" error**
   - Check that your database services are in the same region as your web service
   - Verify network connectivity

4. **"invalid URI" error**
   - Make sure your connection strings are properly formatted
   - Check for any extra spaces or characters

### 7. Security Best Practices

1. **Use Environment Variables**
   - Never hardcode database credentials in your code
   - Use Render's environment variable system

2. **Mask Sensitive Data**
   - The updated code now masks passwords in logs
   - Only the username and host are shown in connection logs

3. **Regular Backups**
   - Set up automated backups for your databases
   - Test your backup and restore procedures

### 8. Monitoring

1. **Health Checks**
   - Your application includes health check endpoints
   - Monitor database connectivity regularly

2. **Logs**
   - Check Render logs for any connection issues
   - Set up alerts for database connection failures

## 🎯 Next Steps

1. Follow the steps above to create your cloud databases
2. Update your environment variables with the correct connection strings
3. Redeploy your application
4. Monitor the logs to ensure successful deployment
5. Test your bot functionality

## 📞 Support

If you encounter any issues:
1. Check the Render documentation: https://render.com/docs
2. Review your application logs for specific error messages
3. Ensure all environment variables are correctly set
4. Verify your database services are running and accessible

---

**Note:** The code has been updated with better error handling and connection retry logic to make deployment more reliable on cloud platforms like Render.
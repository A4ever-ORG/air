# Deploying CodeRoot Bot to Render

This guide will help you deploy the CodeRoot Telegram bot to Render.

## Prerequisites

1. A Render account (https://render.com)
2. A MongoDB Atlas account (for database) or MongoDB cloud service
3. Telegram Bot Token and API credentials
4. GitHub repository with your code

## Quick Deploy

### Step 1: Create MongoDB Database

Option A: MongoDB Atlas (Recommended)
1. Go to https://cloud.mongodb.com
2. Create a free cluster
3. Create a database user
4. Get the connection string

Option B: Use MongoDB cloud service of your choice

### Step 2: Deploy to Render

1. **Connect Repository**
   - Go to https://render.com/dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   ```
   Name: coderoot-bot
   Runtime: Docker
   Build Command: (leave empty)
   Start Command: (leave empty - uses Dockerfile CMD)
   ```

3. **Environment Variables**
   
   **Required:**
   ```
   BOT_TOKEN=your_telegram_bot_token
   API_ID=your_telegram_api_id
   API_HASH=your_telegram_api_hash
   ADMIN_USER_ID=your_telegram_user_id
   ADMIN_USERNAME=your_username
   MONGO_URI=your_mongodb_connection_string
   ```

   **Optional but Recommended:**
   ```
   DATABASE_NAME=coderoot_bot
   PRODUCTION_MODE=true
   LOG_LEVEL=INFO
   AI_ENABLED=true
   AI_BASE_URL=your_ai_service_url
   AI_API_KEY=your_ai_api_key
   MAIN_CHANNEL_USERNAME=your_channel
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your bot

## Environment Variables Reference

### Required Variables
- `BOT_TOKEN`: Your Telegram bot token from @BotFather
- `API_ID`: From https://my.telegram.org
- `API_HASH`: From https://my.telegram.org  
- `ADMIN_USER_ID`: Your Telegram user ID
- `ADMIN_USERNAME`: Your Telegram username
- `MONGO_URI`: MongoDB connection string

### Optional Variables
See `.env.example` for a complete list of configurable options.

## Monitoring

1. **Logs**: View logs in Render dashboard
2. **Health Check**: Bot includes health checks
3. **Alerts**: Configure alerts in Render for failures

## Scaling

For high traffic:
1. Upgrade to a higher Render plan
2. Consider Redis for caching (add Redis service)
3. Use MongoDB with replica sets

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check Dockerfile syntax
   - Ensure all dependencies are in requirements.txt

2. **Database Connection Error**
   - Verify MongoDB URI is correct
   - Check database credentials
   - Ensure MongoDB allows connections from Render IPs

3. **Bot Not Responding**
   - Check BOT_TOKEN is correct
   - Verify API_ID and API_HASH
   - Check logs for error messages

### Getting Help

1. Check Render logs for error details
2. Review bot logs in the dashboard
3. Test environment variables are set correctly

## Security Notes

1. **Never commit secrets** to your repository
2. **Use environment variables** for all sensitive data
3. **Regularly rotate** API keys and tokens
4. **Monitor access logs** for suspicious activity

## Production Optimizations

1. **Database Indexing**: Add indexes for frequently queried fields
2. **Caching**: Implement Redis for session data
3. **Monitoring**: Add application monitoring
4. **Backups**: Set up automated database backups

## Cost Optimization

1. Use **Starter plan** for development/testing
2. **Professional plan** for production use
3. Monitor **bandwidth usage**
4. Consider **auto-scaling** for variable loads
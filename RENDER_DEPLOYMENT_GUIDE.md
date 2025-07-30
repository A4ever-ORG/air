# CodeRoot Bot - Render Deployment Guide
دلیل کامل دپلومنت ربات CodeRoot روی Render

## 🚀 Quick Setup

### 1. Prerequisites
- Render account (render.com)
- Telegram Bot Token from @BotFather
- MongoDB Atlas account (or any MongoDB service)
- Your environment variables ready

### 2. Environment Variables
Add these environment variables in Render dashboard:

**Required:**
```
BOT_TOKEN=your_bot_token_from_botfather
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
ADMIN_USER_ID=your_telegram_user_id
```

**Database:**
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname
DATABASE_NAME=coderoot_production
REDIS_URL=redis://red-xxx:6379  # Get from Render Redis addon
```

**Optional but Recommended:**
```
PRODUCTION_MODE=true
DEMO_MODE=false
LOG_LEVEL=INFO
DEFAULT_LANGUAGE=fa
ADMIN_USERNAME=your_telegram_username
MAIN_CHANNEL_ID=-1001234567890
MAIN_CHANNEL_USERNAME=your_channel
```

### 3. Deployment Steps

1. **Fork/Clone Repository**
   ```bash
   git clone https://github.com/your-username/coderoot-bot.git
   cd coderoot-bot
   ```

2. **Connect to Render**
   - Go to render.com
   - Create new Web Service
   - Connect your GitHub repository
   - Choose branch: `main` or `new`

3. **Configure Service**
   - **Runtime:** Python 3
   - **Build Command:** `chmod +x build.sh && ./build.sh`
   - **Start Command:** `chmod +x start.sh && ./start.sh`
   - **Environment:** Add all environment variables above

4. **Add Database Services**
   - **MongoDB:** Use MongoDB Atlas (recommended) or Render's MongoDB addon
   - **Redis:** Add Render Redis addon for caching

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Check logs for any errors

## 🔧 Configuration Details

### File Structure
```
coderoot-bot/
├── bot.py              # Main bot file
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── build.sh           # Build script for Render
├── start.sh           # Start script for Render
├── render.yaml        # Render configuration
├── .env.example       # Environment variables template
├── database.py        # Database management
├── utils/             # Utility modules
├── services/          # Service modules
└── handlers/          # Message handlers
```

### Environment Variables Explanation

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BOT_TOKEN` | Telegram bot token from @BotFather | Yes | - |
| `API_ID` | Telegram API ID from my.telegram.org | Yes | - |
| `API_HASH` | Telegram API hash from my.telegram.org | Yes | - |
| `ADMIN_USER_ID` | Your Telegram user ID | Yes | - |
| `MONGO_URI` | MongoDB connection string | Yes | - |
| `DATABASE_NAME` | Database name | No | coderoot_production |
| `PRODUCTION_MODE` | Enable production mode | No | true |
| `DEMO_MODE` | Enable demo mode | No | false |
| `LOG_LEVEL` | Logging level | No | INFO |

## 🛠️ Troubleshooting

### Common Issues

1. **Bot not starting**
   - Check BOT_TOKEN is correct
   - Verify all required environment variables are set
   - Check build logs for dependency errors

2. **Database connection failed**
   - Verify MONGO_URI is correct
   - Check MongoDB Atlas IP whitelist (allow all: 0.0.0.0/0)
   - Ensure database user has read/write permissions

3. **Import errors**
   - Check requirements.txt has all dependencies
   - Verify Python version compatibility

4. **Health check failing**
   - Bot includes health endpoints at `/` and `/health`
   - Check if PORT environment variable is set correctly

### Logs and Monitoring

1. **Check Render Logs**
   - Go to your service dashboard
   - Click "Logs" tab
   - Look for startup messages and errors

2. **Bot Status Messages**
   ```
   ✅ Connected to MongoDB
   ✅ Connected to Redis  
   🏥 Health check server started on port 8000
   🤖 CodeRoot Bot is running...
   ```

3. **Test Bot**
   - Send `/start` to your bot
   - Check if it responds correctly
   - Test admin functions if you're the admin

## 🔄 Updating

### Automatic Deployment
- Push changes to your connected branch
- Render will automatically rebuild and deploy

### Manual Deployment
- Go to Render dashboard
- Click "Manual Deploy" -> "Deploy latest commit"

## 📊 Performance Tips

1. **Use MongoDB Atlas M0 (Free)**
   - Good for development and small-scale production
   - Upgrade to M2+ for better performance

2. **Redis for Caching**
   - Add Render Redis addon
   - Helps with session management and caching

3. **Monitor Resources**
   - Check memory usage in Render dashboard
   - Upgrade plan if needed

## 🔐 Security

1. **Environment Variables**
   - Never commit sensitive data to git
   - Use Render's environment variable system
   - Rotate tokens periodically

2. **Database Security**
   - Use strong passwords
   - Enable MongoDB Atlas security features
   - Whitelist only necessary IPs

3. **Bot Security**
   - Set up admin-only commands properly
   - Validate all user inputs
   - Use rate limiting for API calls

## 💡 Advanced Configuration

### Custom Domain
1. Add custom domain in Render dashboard
2. Update WEBHOOK_URL if using webhooks
3. Configure SSL (automatic with Render)

### Scaling
1. **Horizontal Scaling:**
   - Use Render's autoscaling features
   - Configure based on CPU/memory usage

2. **Database Scaling:**
   - Upgrade MongoDB Atlas cluster
   - Consider read replicas for heavy read operations

### Monitoring
1. **Health Checks:**
   - Built-in health endpoints
   - Configure alerting in Render

2. **Logging:**
   - Centralized logging with ELK stack
   - Export logs to external services

## 📞 Support

If you encounter issues:

1. Check this guide thoroughly
2. Review Render documentation
3. Check bot logs for specific errors
4. Test locally with same environment variables

## 🎉 Success Indicators

Your bot is successfully deployed when you see:
- ✅ Service shows "Live" in Render dashboard
- ✅ Health check returns 200 OK
- ✅ Bot responds to `/start` command
- ✅ No error messages in logs
- ✅ Database connections successful

---

**Happy Deploying! 🚀**

*CodeRoot Bot - Production Ready*
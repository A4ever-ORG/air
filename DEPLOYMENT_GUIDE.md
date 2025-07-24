# 🚀 CodeRoot Bot - Production Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ Prerequisites Verified
- [x] **Bot Token:** `7680510409:AAEHRgIrfH7FeuEa5qr2rFG6vGbfkVMxnVM`
- [x] **API Credentials:** Real credentials provided and tested
- [x] **Admin Access:** User ID `7707164235` configured
- [x] **Multi-language:** Persian, English, Arabic working
- [x] **Bot Username:** `@Code_Root_Bot`

### ✅ Server Requirements
- **OS:** Linux (Ubuntu 20.04+ recommended)
- **Python:** 3.9+ (tested with 3.13)
- **RAM:** Minimum 2GB (4GB recommended)
- **Storage:** 10GB+ available space
- **Network:** Stable internet connection

## 🛠️ Deployment Methods

### Method 1: Direct Server Deployment (Recommended)

#### Step 1: Prepare Server
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-venv python3-pip -y

# Install MongoDB
sudo apt install mongodb -y
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Install Redis
sudo apt install redis-server -y
sudo systemctl start redis
sudo systemctl enable redis
```

#### Step 2: Deploy Bot
```bash
# Create project directory
mkdir /opt/coderoot
cd /opt/coderoot

# Clone or upload bot files
# (Transfer all files from the 'default' branch)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install pyrogram tgcrypto python-dotenv

# Set permissions
chmod +x bot.py
```

#### Step 3: Configure Environment
```bash
# Edit .env file with your settings
nano .env
```

Ensure your `.env` contains:
```env
# Production Configuration
BOT_TOKEN=7680510409:AAEHRgIrfH7FeuEa5qr2rFG6vGbfkVMxnVM
API_ID=17064702
API_HASH=f65880b9eededbee85346f874819bbc5
ADMIN_USER_ID=7707164235

# Database
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=coderoot_production
REDIS_URL=redis://localhost:6379

# Channels (Update with your channel)
MAIN_CHANNEL_USERNAME=coderoot_channel

# Production Mode
DEMO_MODE=false
PRODUCTION_MODE=true
```

#### Step 4: Test Bot
```bash
# Test basic functionality
python test_minimal_bot.py

# If successful, run full bot
python bot.py
```

#### Step 5: Setup Service (Keep Running)
Create systemd service for auto-restart:

```bash
sudo nano /etc/systemd/system/coderoot.service
```

Service file content:
```ini
[Unit]
Description=CodeRoot Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/coderoot
Environment=PATH=/opt/coderoot/venv/bin
ExecStart=/opt/coderoot/venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable coderoot
sudo systemctl start coderoot
sudo systemctl status coderoot
```

### Method 2: Docker Deployment

#### Step 1: Install Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### Step 2: Use Docker Compose
```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f
```

## 🔧 Configuration Details

### 1. Channel Setup
```bash
# Create your Telegram channel
# Get channel ID and username
# Update in .env:
MAIN_CHANNEL_ID=-1001234567890
MAIN_CHANNEL_USERNAME=your_channel_name
```

### 2. Payment Configuration
```bash
# Update card details for manual payments
CARD_NUMBER=6037-9977-7766-5544
CARD_HOLDER_NAME=حادی
```

### 3. Email Service (Optional)
```bash
# For notifications
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

## 📊 Monitoring & Maintenance

### Check Bot Status
```bash
# Service status
sudo systemctl status coderoot

# View logs
sudo journalctl -u coderoot -f

# View bot logs
tail -f logs/coderoot.log
```

### Database Monitoring
```bash
# MongoDB status
sudo systemctl status mongodb

# Redis status
sudo systemctl status redis

# Connect to MongoDB
mongo
use coderoot_production
show collections
```

### Performance Monitoring
```bash
# Resource usage
htop

# Disk space
df -h

# Memory usage
free -h
```

## 🔐 Security Recommendations

### 1. Firewall Configuration
```bash
# Basic firewall setup
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
```

### 2. SSL Certificate (If using webhook)
```bash
# Install certbot
sudo apt install certbot

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com
```

### 3. Regular Backups
```bash
# Create backup script
#!/bin/bash
mongodump --db coderoot_production --out /backup/$(date +%Y%m%d)
tar -czf /backup/coderoot-$(date +%Y%m%d).tar.gz /opt/coderoot
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Bot Not Responding
```bash
# Check if bot is running
sudo systemctl status coderoot

# Check logs for errors
sudo journalctl -u coderoot -n 50

# Test token manually
python test_minimal_bot.py
```

#### 2. Database Connection Issues
```bash
# Check MongoDB
sudo systemctl status mongodb
mongo --eval "db.runCommand('ping')"

# Check Redis
redis-cli ping
```

#### 3. Permission Errors
```bash
# Fix file permissions
sudo chown -R root:root /opt/coderoot
sudo chmod +x /opt/coderoot/bot.py
```

#### 4. Memory Issues
```bash
# Check memory usage
free -h

# Restart services if needed
sudo systemctl restart coderoot
```

### Log Analysis
```bash
# Bot logs
tail -f logs/coderoot.log

# System logs
sudo journalctl -u coderoot -f

# Error only logs
sudo journalctl -u coderoot -p err
```

## 📈 Scaling Considerations

### When to Scale
- More than 1000 active users
- High message volume
- Database performance issues

### Scaling Options
1. **Vertical Scaling:** Increase server resources
2. **Horizontal Scaling:** Multiple bot instances
3. **Database Scaling:** MongoDB replica sets
4. **Caching:** Enhanced Redis configuration

## 🎯 Success Metrics

### Monitor These KPIs
- **User Registration Rate**
- **Shop Creation Rate**
- **Message Response Time**
- **Error Rate**
- **Server Resource Usage**

### Health Checks
```bash
# Create health check script
#!/bin/bash
curl -s http://localhost:8000/health || echo "Bot health check failed"
```

## 📞 Support & Maintenance

### Regular Tasks
- [ ] **Daily:** Check logs for errors
- [ ] **Weekly:** Monitor resource usage
- [ ] **Monthly:** Update dependencies
- [ ] **Quarterly:** Full backup and security review

### Emergency Contacts
- **Developer Support:** Available for critical issues
- **Server Provider:** Your hosting provider support
- **Telegram Support:** For API-related issues

## 🎉 Go Live Checklist

Before announcing your bot:

- [ ] ✅ Bot responds to `/start`
- [ ] ✅ Language selection works
- [ ] ✅ Shop creation workflow tested
- [ ] ✅ Admin panel accessible
- [ ] ✅ Channel join enforcement configured
- [ ] ✅ Payment information updated
- [ ] ✅ Error handling tested
- [ ] ✅ Backup system configured
- [ ] ✅ Monitoring tools active
- [ ] ✅ Documentation ready for users

**Your CodeRoot bot is ready to serve thousands of users! 🚀**

---

*Remember: This is a production-grade system capable of handling real business operations.*
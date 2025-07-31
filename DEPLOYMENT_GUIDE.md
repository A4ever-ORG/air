# 🚀 CodeRoot Bot - Complete Local Deployment Guide

This guide provides step-by-step instructions for deploying the CodeRoot Bot with **zero external dependencies** using vendored Go modules.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Detailed Setup](#detailed-setup)
4. [Configuration](#configuration)
5. [Deployment Options](#deployment-options)
6. [Troubleshooting](#troubleshooting)
7. [Production Tips](#production-tips)

## 🔧 Prerequisites

### Required Software
- **Go 1.21+** (for building only - not required on production server)
- **Git** (for cloning the repository)

### Required Services
- **MongoDB** (local or cloud instance)
- **Redis** (local or cloud instance)
- **Telegram Bot Token** (from @BotFather)

## ⚡ Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/A4ever-ORG/code-root-TGbot.git
cd code-root-TGbot

# Switch to the go branch
git checkout go

# Verify vendored dependencies exist
ls -la vendor/
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit configuration (see Configuration section below)
nano .env
```

### 3. Build and Deploy
```bash
# Build the application (creates vendored binary)
./deploy.sh

# Start the application
./start.sh
```

That's it! Your bot should now be running.

## 🔧 Detailed Setup

### Step 1: Repository Setup
```bash
# Clone with specific branch
git clone -b go https://github.com/A4ever-ORG/code-root-TGbot.git
cd code-root-TGbot

# Verify project structure
ls -la
# Should show: vendor/, go.mod, go.sum, deploy.sh, start.sh, etc.
```

### Step 2: Verify Vendored Dependencies
```bash
# Check vendor directory (should be ~32MB)
du -sh vendor/

# Verify all dependencies are present
cat vendor/modules.txt | head -20
```

### Step 3: Build Application
```bash
# Run the deployment script
./deploy.sh

# This will:
# - Use vendored dependencies (no internet required)
# - Create optimized binary (~13MB)
# - Verify build success
```

### Step 4: Configure Application
```bash
# Create environment file
cp .env.example .env

# Edit with your actual values
vim .env
```

### Step 5: Start Application
```bash
# Start with automatic checks
./start.sh

# Or start with specific command
./start.sh start
```

## ⚙️ Configuration

### Required Environment Variables

Edit your `.env` file with these **required** values:

```bash
# Telegram Bot (REQUIRED)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890

# Database (REQUIRED)
MONGO_URI=mongodb://localhost:27017/coderoot_bot
REDIS_URL=redis://localhost:6379

# Admin (REQUIRED)
ADMIN_USER_ID=123456789
ADMIN_USERNAME=yourusername
```

### Optional Configuration

```bash
# Server Settings
SERVER_PORT=8080
SERVER_HOST=0.0.0.0
ENVIRONMENT=production

# Payment Settings
CARD_NUMBER=1234-5678-9012-3456
CARD_HOLDER_NAME=Your Name

# Channel Settings
MAIN_CHANNEL_ID=-1001234567890
MAIN_CHANNEL_USERNAME=yourchannel

# Pricing
PROFESSIONAL_PLAN_PRICE=50000
VIP_PLAN_PRICE=100000
COMMISSION_RATE=10
```

## 🚀 Deployment Options

### Option 1: Local Development
```bash
# Build and run locally
./deploy.sh
./start.sh

# View logs
./start.sh logs

# Stop when done
./start.sh stop
```

### Option 2: Production Server
```bash
# Upload entire project directory to server
scp -r code-root-TGbot/ user@server:/opt/

# SSH to server
ssh user@server
cd /opt/code-root-TGbot

# Configure environment
cp .env.example .env
vim .env

# Deploy
./deploy.sh
./start.sh

# Setup as service (optional)
sudo ln -s /opt/code-root-TGbot/start.sh /usr/local/bin/coderoot-bot
```

### Option 3: Docker Deployment
```bash
# Create Dockerfile (if not exists)
cat > Dockerfile << 'EOF'
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -mod=vendor -tags netgo -ldflags '-s -w' -o app

FROM alpine:latest
RUN apk --no-cache add ca-certificates tzdata
WORKDIR /root/
COPY --from=builder /app/app .
COPY --from=builder /app/.env .
CMD ["./app"]
EOF

# Build and run
docker build -t coderoot-bot .
docker run -d --name coderoot-bot -p 8080:8080 coderoot-bot
```

### Option 4: Systemd Service
```bash
# Create service file
sudo tee /etc/systemd/system/coderoot-bot.service << 'EOF'
[Unit]
Description=CodeRoot Telegram Bot
After=network.target

[Service]
Type=forking
User=ubuntu
WorkingDirectory=/opt/code-root-TGbot
ExecStart=/opt/code-root-TGbot/start.sh start
ExecStop=/opt/code-root-TGbot/start.sh stop
ExecReload=/opt/code-root-TGbot/start.sh restart
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl enable coderoot-bot
sudo systemctl start coderoot-bot
sudo systemctl status coderoot-bot
```

## 🔍 Management Commands

### Application Control
```bash
./start.sh start    # Start the application
./start.sh stop     # Stop the application
./start.sh restart  # Restart the application
./start.sh status   # Check application status
./start.sh logs     # Follow application logs
```

### Build Commands
```bash
./deploy.sh         # Build application with vendored deps
go mod vendor       # Refresh vendored dependencies
go mod tidy         # Clean up go.mod and go.sum
```

### Monitoring
```bash
# View logs in real-time
tail -f logs/app.log

# Check application status
ps aux | grep ./app

# Monitor resource usage
top -p $(cat logs/app.pid)
```

## 🐛 Troubleshooting

### Common Issues

#### 1. "Binary not found" Error
```bash
# Solution: Build the application first
./deploy.sh
```

#### 2. "BOT_TOKEN not configured" Error
```bash
# Solution: Set your bot token in .env
echo "BOT_TOKEN=your_actual_token_here" >> .env
```

#### 3. "MongoDB connection failed"
```bash
# Check MongoDB is running
systemctl status mongod

# Test connection
mongo --eval "db.adminCommand('ismaster')"

# Update MONGO_URI in .env if needed
```

#### 4. "Redis connection failed"
```bash
# Check Redis is running
systemctl status redis

# Test connection
redis-cli ping

# Update REDIS_URL in .env if needed
```

#### 5. "Port already in use"
```bash
# Find process using port 8080
lsof -i :8080

# Kill the process or change SERVER_PORT in .env
```

### Log Analysis
```bash
# View recent errors
grep -i error logs/app.log | tail -10

# View startup logs
head -50 logs/app.log

# Monitor live logs
./start.sh logs
```

### Dependency Issues
```bash
# Refresh vendor directory
rm -rf vendor/
go mod vendor

# Rebuild application
./deploy.sh
```

## 🏭 Production Tips

### Security
- Change default passwords and tokens
- Use environment-specific `.env` files
- Restrict file permissions: `chmod 600 .env`
- Use HTTPS for webhooks
- Enable firewall rules

### Performance
- Monitor memory usage: `free -h`
- Monitor disk space: `df -h`
- Rotate logs: `logrotate`
- Use reverse proxy (nginx) for better performance

### Backup
```bash
# Backup configuration
cp .env .env.backup

# Backup logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/

# Backup database (MongoDB)
mongodump --uri="$MONGO_URI" --out=backup/
```

### Monitoring
```bash
# Setup health check endpoint
curl http://localhost:8080/health

# Monitor with systemd
journalctl -u coderoot-bot -f

# Setup log rotation
sudo tee /etc/logrotate.d/coderoot-bot << 'EOF'
/opt/code-root-TGbot/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
EOF
```

## 📊 Project Structure

```
code-root-TGbot/
├── vendor/                 # Vendored dependencies (32MB)
├── internal/              # Application source code
│   ├── app/              # Main application logic
│   ├── config/           # Configuration management
│   ├── database/         # Database layer
│   ├── handlers/         # Telegram handlers
│   ├── logger/           # Logging utilities
│   ├── models/           # Data models
│   └── ...
├── logs/                 # Application logs
├── go.mod               # Go module definition
├── go.sum               # Dependency checksums
├── main.go              # Application entry point
├── deploy.sh            # Deployment script
├── start.sh             # Production startup script
├── .env.example         # Environment template
└── DEPLOYMENT_GUIDE.md  # This guide
```

## ✅ Success Indicators

Your deployment is successful when you see:

1. **Build Success**: `./deploy.sh` completes without errors
2. **Startup Success**: `./start.sh` shows "Application started successfully!"
3. **Health Check**: `curl http://localhost:8080/health` returns status
4. **Telegram Response**: Your bot responds to `/start` command
5. **Logs**: `./start.sh logs` shows normal operation

## 🎉 Congratulations!

You now have a **zero-dependency**, **locally-vendored** CodeRoot Bot deployment that:

- ✅ Builds without internet access
- ✅ Runs without external Go dependencies
- ✅ Includes all necessary libraries locally
- ✅ Provides comprehensive management tools
- ✅ Supports multiple deployment scenarios

Your bot is ready for production! 🚀
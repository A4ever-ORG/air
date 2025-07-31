#!/bin/bash

# 🚀 Go Multi-Platform - Kali Linux Installation Script
# This script installs the application on Kali Linux with all optimizations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🚀 GO MULTI-PLATFORM 🚀                  ║"
echo "║                                                              ║"
echo "║  Kali Linux Installation Script                              ║"
echo "║  Version: 1.0.0                                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ This script should not be run as root${NC}"
   echo -e "${YELLOW}💡 Run as a regular user with sudo privileges${NC}"
   exit 1
fi

# Check if Kali Linux
if ! grep -q "kali" /etc/os-release 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Warning: This script is optimized for Kali Linux${NC}"
    echo -e "${YELLOW}   It may work on other Debian-based distributions${NC}"
    echo
fi

echo -e "${GREEN}🔧 Starting Kali Linux installation...${NC}"
echo

# Update system
echo -e "${BLUE}📦 Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y
echo -e "${GREEN}✅ System updated successfully${NC}"
echo

# Install Go
echo -e "${BLUE}🐹 Installing Go programming language...${NC}"
if ! command -v go &> /dev/null; then
    sudo apt install golang-go -y
    echo -e "${GREEN}✅ Go installed successfully${NC}"
else
    echo -e "${GREEN}✅ Go is already installed${NC}"
fi
echo

# Install additional Kali tools (optional)
echo -e "${BLUE}🔧 Installing additional Kali Linux tools...${NC}"
echo -e "${YELLOW}💡 This step is optional but recommended for full functionality${NC}"
read -p "Do you want to install additional Kali tools? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}📦 Installing Kali Linux tools...${NC}"
    sudo apt install -y nmap wireshark aircrack-ng john hashcat sqlmap nikto dirb gobuster hydra medusa ncrack
    echo -e "${GREEN}✅ Additional tools installed successfully${NC}"
else
    echo -e "${YELLOW}⏭️  Skipping additional tools installation${NC}"
fi
echo

# Clone repository
echo -e "${BLUE}📥 Cloning repository...${NC}"
if [ -d "go-multi-platform" ]; then
    echo -e "${YELLOW}📁 Repository already exists, updating...${NC}"
    cd go-multi-platform
    git pull origin main
else
    git clone https://github.com/awesome-project/go-multi-platform.git
    cd go-multi-platform
fi
echo -e "${GREEN}✅ Repository cloned/updated successfully${NC}"
echo

# Build application
echo -e "${BLUE}🔨 Building application...${NC}"
go mod tidy
go build -o go-multi-platform
echo -e "${GREEN}✅ Application built successfully${NC}"
echo

# Install system-wide
echo -e "${BLUE}📦 Installing application system-wide...${NC}"
sudo cp go-multi-platform /usr/local/bin/
sudo chmod +x /usr/local/bin/go-multi-platform
echo -e "${GREEN}✅ Application installed successfully${NC}"
echo

# Create desktop shortcut
echo -e "${BLUE}🖥️  Creating desktop shortcut...${NC}"
cat > ~/Desktop/go-multi-platform.desktop << EOF
[Desktop Entry]
Name=Go Multi-Platform
Comment=Advanced Multi-Platform Go Application
Exec=/usr/local/bin/go-multi-platform
Icon=terminal
Terminal=true
Type=Application
Categories=System;Security;
EOF
chmod +x ~/Desktop/go-multi-platform.desktop
echo -e "${GREEN}✅ Desktop shortcut created successfully${NC}"
echo

# Create application menu entry
echo -e "${BLUE}📋 Creating application menu entry...${NC}"
sudo tee /usr/share/applications/go-multi-platform.desktop > /dev/null << EOF
[Desktop Entry]
Name=Go Multi-Platform
Comment=Advanced Multi-Platform Go Application
Exec=/usr/local/bin/go-multi-platform
Icon=terminal
Terminal=true
Type=Application
Categories=System;Security;
EOF
echo -e "${GREEN}✅ Application menu entry created successfully${NC}"
echo

# Test installation
echo -e "${BLUE}🧪 Testing installation...${NC}"
if command -v go-multi-platform &> /dev/null; then
    echo -e "${GREEN}✅ Installation test successful${NC}"
else
    echo -e "${RED}❌ Installation test failed${NC}"
    exit 1
fi
echo

# Show success message
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🎉 INSTALLATION COMPLETE 🎉              ║"
echo "║                                                              ║"
echo "║  Go Multi-Platform has been successfully installed!         ║"
echo "║                                                              ║"
echo "║  You can now run: go-multi-platform                         ║"
echo "║  Or use the desktop shortcut                                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo

# Show available commands
echo -e "${CYAN}📋 Available commands:${NC}"
echo -e "${YELLOW}  • go-multi-platform system    - System information${NC}"
echo -e "${YELLOW}  • go-multi-platform network   - Network analysis tools${NC}"
echo -e "${YELLOW}  • go-multi-platform security  - Security analysis tools${NC}"
echo -e "${YELLOW}  • go-multi-platform kali      - Kali-specific tools${NC}"
echo -e "${YELLOW}  • go-multi-platform install   - Installation guide${NC}"
echo -e "${YELLOW}  • go-multi-platform demo      - Interactive demo${NC}"
echo

# Show next steps
echo -e "${CYAN}🚀 Next steps:${NC}"
echo -e "${YELLOW}  1. Run: go-multi-platform${NC}"
echo -e "${YELLOW}  2. Explore the interactive demo: go-multi-platform demo${NC}"
echo -e "${YELLOW}  3. Check Kali tools: go-multi-platform kali${NC}"
echo -e "${YELLOW}  4. View system info: go-multi-platform system${NC}"
echo

echo -e "${GREEN}🎉 Enjoy your Kali Linux optimized experience!${NC}"
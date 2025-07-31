#!/data/data/com.termux/files/usr/bin/bash

# 🚀 Go Multi-Platform - Termux Installation Script
# This script installs the application on Termux with all optimizations

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
echo "║  Termux Installation Script                                  ║"
echo "║  Version: 1.0.0                                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo -e "${RED}❌ This script is designed for Termux on Android${NC}"
    echo -e "${YELLOW}💡 Please run this script in Termux${NC}"
    exit 1
fi

echo -e "${GREEN}🔧 Starting Termux installation...${NC}"
echo

# Update Termux
echo -e "${BLUE}📦 Updating Termux packages...${NC}"
pkg update && pkg upgrade -y
echo -e "${GREEN}✅ Termux updated successfully${NC}"
echo

# Install essential packages
echo -e "${BLUE}🐹 Installing Go programming language...${NC}"
if ! command -v go &> /dev/null; then
    pkg install golang -y
    echo -e "${GREEN}✅ Go installed successfully${NC}"
else
    echo -e "${GREEN}✅ Go is already installed${NC}"
fi
echo

# Install additional tools (optional)
echo -e "${BLUE}🔧 Installing additional Termux tools...${NC}"
echo -e "${YELLOW}💡 This step is optional but recommended for full functionality${NC}"
read -p "Do you want to install additional Termux tools? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}📦 Installing Termux tools...${NC}"
    pkg install -y nmap curl wget openssh git
    pkg install -y hashcat john hydra sqlmap nikto dirb gobuster
    pkg install -y termux-api termux-tools termux-services
    echo -e "${GREEN}✅ Additional tools installed successfully${NC}"
else
    echo -e "${YELLOW}⏭️  Skipping additional tools installation${NC}"
fi
echo

# Create local bin directory
echo -e "${BLUE}📁 Creating local bin directory...${NC}"
mkdir -p ~/.local/bin
echo -e "${GREEN}✅ Local bin directory created successfully${NC}"
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

# Install locally
echo -e "${BLUE}📦 Installing application locally...${NC}"
cp go-multi-platform ~/.local/bin/
chmod +x ~/.local/bin/go-multi-platform
echo -e "${GREEN}✅ Application installed successfully${NC}"
echo

# Add to PATH
echo -e "${BLUE}🔗 Adding to PATH...${NC}"
if ! grep -q "~/.local/bin" ~/.bashrc; then
    echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
    echo -e "${GREEN}✅ PATH updated successfully${NC}"
else
    echo -e "${GREEN}✅ PATH already configured${NC}"
fi
echo

# Create desktop shortcut (Termux widget)
echo -e "${BLUE}🖥️  Creating Termux widget...${NC}"
cat > ~/go-multi-platform-widget.sh << EOF
#!/data/data/com.termux/files/usr/bin/bash
cd ~/go-multi-platform
./go-multi-platform
EOF
chmod +x ~/go-multi-platform-widget.sh
echo -e "${GREEN}✅ Termux widget created successfully${NC}"
echo

# Create quick access script
echo -e "${BLUE}⚡ Creating quick access script...${NC}"
cat > ~/go-multi-platform.sh << EOF
#!/data/data/com.termux/files/usr/bin/bash
export PATH=\$PATH:~/.local/bin
go-multi-platform "\$@"
EOF
chmod +x ~/go-multi-platform.sh
echo -e "${GREEN}✅ Quick access script created successfully${NC}"
echo

# Set up Termux API permissions
echo -e "${BLUE}🔧 Setting up Termux API permissions...${NC}"
echo -e "${YELLOW}💡 Please grant the following permissions in Android settings:${NC}"
echo -e "${YELLOW}   • Storage access${NC}"
echo -e "${YELLOW}   • Camera access${NC}"
echo -e "${YELLOW}   • Location access${NC}"
echo -e "${YELLOW}   • Microphone access${NC}"
echo -e "${YELLOW}   • Phone state access${NC}"
echo

# Test installation
echo -e "${BLUE}🧪 Testing installation...${NC}"
export PATH=$PATH:~/.local/bin
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
echo "║  Or use: ./go-multi-platform.sh                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo

# Show available commands
echo -e "${CYAN}📋 Available commands:${NC}"
echo -e "${YELLOW}  • go-multi-platform system    - System information${NC}"
echo -e "${YELLOW}  • go-multi-platform network   - Network analysis tools${NC}"
echo -e "${YELLOW}  • go-multi-platform security  - Security analysis tools${NC}"
echo -e "${YELLOW}  • go-multi-platform termux    - Termux-specific tools${NC}"
echo -e "${YELLOW}  • go-multi-platform install   - Installation guide${NC}"
echo -e "${YELLOW}  • go-multi-platform demo      - Interactive demo${NC}"
echo

# Show mobile optimizations
echo -e "${CYAN}📱 Mobile Optimizations:${NC}"
echo -e "${YELLOW}  • Touch-friendly interface${NC}"
echo -e "${YELLOW}  • Battery optimization${NC}"
echo -e "${YELLOW}  • Android API integration${NC}"
echo -e "${YELLOW}  • Offline capability${NC}"
echo -e "${YELLOW}  • Low-resource optimization${NC}"
echo

# Show next steps
echo -e "${CYAN}🚀 Next steps:${NC}"
echo -e "${YELLOW}  1. Restart Termux or run: source ~/.bashrc${NC}"
echo -e "${YELLOW}  2. Run: go-multi-platform${NC}"
echo -e "${YELLOW}  3. Explore the interactive demo: go-multi-platform demo${NC}"
echo -e "${YELLOW}  4. Check Termux tools: go-multi-platform termux${NC}"
echo -e "${YELLOW}  5. View system info: go-multi-platform system${NC}"
echo

# Show Termux-specific tips
echo -e "${CYAN}💡 Termux Tips:${NC}"
echo -e "${YELLOW}  • Use volume buttons for copy/paste${NC}"
echo -e "${YELLOW}  • Long press for context menu${NC}"
echo -e "${YELLOW}  • Swipe from left edge for keyboard${NC}"
echo -e "${YELLOW}  • Use Termux Widgets for quick access${NC}"
echo -e "${YELLOW}  • Enable battery optimization in Android settings${NC}"
echo

echo -e "${GREEN}🎉 Enjoy your Termux optimized experience!${NC}"
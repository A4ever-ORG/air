#!/bin/bash

# Kali Security Suite Installation Script
# Version: 2.0.0
# Optimized for Kali Linux

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
echo "║                    ⚔️ KALI SECURITY SUITE ⚔️                ║"
echo "║                                                              ║"
echo "║  Advanced Penetration Testing & Security Analysis           ║"
echo "║  Installation Script v2.0.0                                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to print status
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    print_warning "This script should not be run as root for security reasons"
    print_status "Creating non-root user for installation..."
    # Create kali user if it doesn't exist
    if ! id "kali" &>/dev/null; then
        useradd -m -s /bin/bash kali
        usermod -aG sudo kali
        print_success "Created kali user"
    fi
    # Switch to kali user
    exec su - kali "$0" "$@"
fi

# Update system
print_status "Updating Kali Linux system..."
sudo apt update && sudo apt upgrade -y
print_success "System updated successfully"

# Install essential packages
print_status "Installing essential packages..."
sudo apt install -y \
    git \
    curl \
    wget \
    build-essential \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common \
    apt-transport-https
print_success "Essential packages installed"

# Install Go
print_status "Installing Go programming language..."
if ! command -v go &> /dev/null; then
    # Download and install Go
    GO_VERSION="1.21.5"
    wget https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz
    sudo tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz
    rm go${GO_VERSION}.linux-amd64.tar.gz
    
    # Add Go to PATH
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    export PATH=$PATH:/usr/local/go/bin
    print_success "Go ${GO_VERSION} installed successfully"
else
    print_status "Go is already installed"
fi

# Install security tools
print_status "Installing security tools..."
sudo apt install -y \
    nmap \
    wireshark \
    aircrack-ng \
    metasploit-framework \
    sqlmap \
    nikto \
    dirb \
    hydra \
    john \
    hashcat \
    tcpdump \
    iptables \
    netcat \
    openssl \
    sslscan \
    testssl.sh \
    whatweb \
    gobuster \
    ffuf \
    amass \
    subfinder \
    masscan \
    zmap \
    tshark \
    ettercap-text-only \
    dsniff \
    macchanger \
    proxychains \
    tor \
    privoxy
print_success "Security tools installed"

# Install additional tools
print_status "Installing additional tools..."
sudo apt install -y \
    python3 \
    python3-pip \
    ruby \
    ruby-dev \
    nodejs \
    npm \
    docker.io \
    docker-compose \
    snapd
print_success "Additional tools installed"

# Install Python security tools
print_status "Installing Python security tools..."
pip3 install --user \
    requests \
    beautifulsoup4 \
    lxml \
    selenium \
    paramiko \
    scapy \
    cryptography \
    pycryptodome \
    colorama \
    tabulate \
    rich \
    click \
    typer
print_success "Python security tools installed"

# Install Node.js security tools
print_status "Installing Node.js security tools..."
npm install -g \
    npm-check-updates \
    audit \
    snyk \
    retire \
    eslint \
    prettier
print_success "Node.js security tools installed"

# Install Ruby security tools
print_status "Installing Ruby security tools..."
gem install \
    bundler \
    wpscan \
    arachni \
    metasploit-framework
print_success "Ruby security tools installed"

# Configure Docker
print_status "Configuring Docker..."
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker
print_success "Docker configured"

# Create application directory
print_status "Creating application directory..."
mkdir -p ~/kali-security-suite
cd ~/kali-security-suite
print_success "Application directory created"

# Clone repository (if not already present)
if [ ! -d ".git" ]; then
    print_status "Cloning Kali Security Suite repository..."
    git clone https://github.com/awesome-project/kali-security-suite.git .
    print_success "Repository cloned"
else
    print_status "Repository already exists, updating..."
    git pull origin main
    print_success "Repository updated"
fi

# Install Go dependencies
print_status "Installing Go dependencies..."
go mod download
go mod tidy
print_success "Go dependencies installed"

# Build the application
print_status "Building Kali Security Suite..."
go build -ldflags="-s -w" -o kali-security-suite .
chmod +x kali-security-suite
print_success "Application built successfully"

# Create configuration directory
print_status "Creating configuration files..."
mkdir -p ~/.config/kali-security-suite
cat > ~/.config/kali-security-suite/config.yaml << 'EOF'
security:
  mode: kali
  intensity: high
  auto_update: true
  scan_interval: 3600
  
network:
  scan_ports: true
  packet_capture: true
  wireless_scan: true
  bandwidth_monitoring: true
  
monitoring:
  real_time: true
  alerting: true
  logging: true
  log_level: info
  
reporting:
  format: pdf
  auto_generate: true
  email_notifications: false
  retention_days: 30
  
performance:
  max_threads: 4
  memory_limit: 2048
  cpu_limit: 80
EOF
print_success "Configuration files created"

# Create systemd service
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/kali-security-suite.service << EOF
[Unit]
Description=Kali Security Suite
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$HOME/kali-security-suite
ExecStart=$HOME/kali-security-suite/kali-security-suite monitor --daemon
Restart=always
RestartSec=10
Environment=SECURITY_MODE=kali
Environment=SCAN_INTENSITY=high
Environment=GOGC=50
Environment=GOMAXPROCS=4

[Install]
WantedBy=multi-user.target
EOF
print_success "Systemd service created"

# Enable and start service
print_status "Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable kali-security-suite
sudo systemctl start kali-security-suite
print_success "Service started successfully"

# Create desktop shortcut
print_status "Creating desktop shortcut..."
cat > ~/Desktop/Kali\ Security\ Suite.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Kali Security Suite
Comment=Advanced Security and Penetration Testing Suite
Exec=$HOME/kali-security-suite/kali-security-suite
Icon=security-high
Terminal=true
Categories=Security;System;
EOF
chmod +x ~/Desktop/Kali\ Security\ Suite.desktop
print_success "Desktop shortcut created"

# Set up environment variables
print_status "Setting up environment variables..."
echo 'export PATH=$PATH:$HOME/kali-security-suite' >> ~/.bashrc
echo 'export SECURITY_MODE=kali' >> ~/.bashrc
echo 'export SCAN_INTENSITY=high' >> ~/.bashrc
echo 'export GOGC=50' >> ~/.bashrc
echo 'export GOMAXPROCS=4' >> ~/.bashrc
print_success "Environment variables configured"

# Create aliases
print_status "Creating command aliases..."
echo 'alias kss="$HOME/kali-security-suite/kali-security-suite"' >> ~/.bashrc
echo 'alias kss-scan="kss scan"' >> ~/.bashrc
echo 'alias kss-network="kss network"' >> ~/.bashrc
echo 'alias kss-pentest="kss pentest"' >> ~/.bashrc
echo 'alias kss-harden="kss harden"' >> ~/.bashrc
echo 'alias kss-monitor="kss monitor"' >> ~/.bashrc
echo 'alias kss-report="kss report"' >> ~/.bashrc
print_success "Command aliases created"

# Set up logging
print_status "Setting up logging..."
sudo mkdir -p /var/log/kali-security-suite
sudo chown $USER:$USER /var/log/kali-security-suite
print_success "Logging configured"

# Create update script
print_status "Creating update script..."
cat > ~/kali-security-suite/update.sh << 'EOF'
#!/bin/bash
cd ~/kali-security-suite
git pull origin main
go mod download
go build -ldflags="-s -w" -o kali-security-suite .
sudo systemctl restart kali-security-suite
echo "Kali Security Suite updated successfully!"
EOF
chmod +x ~/kali-security-suite/update.sh
print_success "Update script created"

# Final setup
print_status "Performing final setup..."
sudo systemctl status kali-security-suite --no-pager
print_success "Installation completed successfully!"

# Display completion message
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ✅ INSTALLATION COMPLETE ✅               ║"
echo "║                                                              ║"
echo "║  Kali Security Suite has been successfully installed!       ║"
echo "║                                                              ║"
echo "║  Quick Start Commands:                                       ║"
echo "║  • kss --help              - Show all commands              ║"
echo "║  • kss scan                - Run security scan              ║"
echo "║  • kss network             - Network analysis               ║"
echo "║  • kss pentest             - Penetration testing            ║"
echo "║  • kss harden              - System hardening               ║"
echo "║  • kss monitor             - Real-time monitoring           ║"
echo "║  • kss report              - Generate reports               ║"
echo "║                                                              ║"
echo "║  Service Management:                                        ║"
echo "║  • sudo systemctl status kali-security-suite               ║"
echo "║  • sudo systemctl restart kali-security-suite              ║"
echo "║  • sudo systemctl stop kali-security-suite                 ║"
echo "║                                                              ║"
echo "║  Updates:                                                   ║"
echo "║  • ~/kali-security-suite/update.sh                        ║"
echo "║                                                              ║"
echo "║  Configuration:                                             ║"
echo "║  • ~/.config/kali-security-suite/config.yaml              ║"
echo "║                                                              ║"
echo "║  Logs:                                                      ║"
echo "║  • /var/log/kali-security-suite/                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Test the installation
print_status "Testing installation..."
if ./kali-security-suite --help &> /dev/null; then
    print_success "Installation test passed!"
else
    print_error "Installation test failed!"
    exit 1
fi

print_success "Kali Security Suite is ready for use!"
print_status "Please restart your terminal or run 'source ~/.bashrc' to load the new environment variables."
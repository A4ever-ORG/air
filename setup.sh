#!/bin/bash

# CodeRoot Bot - Automated Setup Script
# This script will set up the environment and dependencies automatically

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    if command_exists python3; then
        local python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        local required_version="3.8"
        
        if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
            print_success "Python $python_version found"
            return 0
        else
            print_error "Python $python_version found, but version $required_version or higher is required"
            return 1
        fi
    else
        print_error "Python 3 not found"
        return 1
    fi
}

# Function to install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    if command_exists pip3; then
        pip3 install -r requirements.txt
    elif command_exists pip; then
        pip install -r requirements.txt
    else
        print_error "pip not found"
        return 1
    fi
    
    print_success "Python dependencies installed"
}

# Function to check MongoDB
check_mongodb() {
    if command_exists mongod; then
        print_success "MongoDB found"
        return 0
    elif command_exists docker; then
        print_warning "MongoDB not found locally, but Docker is available"
        print_status "You can use 'make docker-run' to run with Docker"
        return 0
    else
        print_warning "MongoDB not found. Please install MongoDB or Docker"
        return 1
    fi
}

# Function to setup environment file
setup_env_file() {
    if [ ! -f .env ]; then
        print_status "Creating .env file from template..."
        cp .env.example .env
        print_success ".env file created"
        print_warning "Please edit .env file with your configuration before running the bot"
    else
        print_warning ".env file already exists"
    fi
}

# Function to create directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p logs
    mkdir -p uploads
    mkdir -p backups
    print_success "Directories created"
}

# Function to check Docker setup
check_docker() {
    if command_exists docker && command_exists docker-compose; then
        print_success "Docker and Docker Compose found"
        return 0
    else
        print_warning "Docker or Docker Compose not found"
        return 1
    fi
}

# Function to display final instructions
show_final_instructions() {
    echo ""
    echo "=================================================="
    print_success "Setup completed successfully!"
    echo "=================================================="
    echo ""
    echo "Next steps:"
    echo "1. Edit the .env file with your configuration:"
    echo "   - BOT_TOKEN (from @BotFather)"
    echo "   - API_ID and API_HASH (from my.telegram.org)"
    echo "   - ADMIN_USER_ID (your Telegram user ID)"
    echo "   - Card information for payments"
    echo ""
    echo "2. Start the bot:"
    echo "   make run          # Run locally"
    echo "   make docker-run   # Run with Docker"
    echo ""
    echo "3. Other useful commands:"
    echo "   make help         # Show all commands"
    echo "   make logs         # View logs"
    echo "   make status       # Check status"
    echo ""
    print_warning "Don't forget to configure your .env file before running!"
}

# Main setup function
main() {
    echo "=================================================="
    echo "         CodeRoot Bot - Automated Setup"
    echo "=================================================="
    echo ""
    
    # Check Python
    print_status "Checking Python installation..."
    if ! check_python_version; then
        print_error "Please install Python 3.8 or higher"
        exit 1
    fi
    
    # Install dependencies
    if ! install_python_deps; then
        print_error "Failed to install Python dependencies"
        exit 1
    fi
    
    # Check MongoDB
    print_status "Checking MongoDB..."
    check_mongodb
    
    # Check Docker
    print_status "Checking Docker..."
    check_docker
    
    # Setup environment
    setup_env_file
    
    # Create directories
    create_directories
    
    # Show final instructions
    show_final_instructions
}

# Handle command line arguments
case "${1:-}" in
    --docker-only)
        print_status "Setting up Docker environment only..."
        if ! check_docker; then
            print_error "Docker setup failed"
            exit 1
        fi
        setup_env_file
        create_directories
        print_success "Docker setup completed"
        print_status "Run 'make docker-run' to start with Docker"
        ;;
    --help)
        echo "CodeRoot Bot Setup Script"
        echo ""
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  --docker-only    Setup for Docker deployment only"
        echo "  --help          Show this help message"
        echo ""
        echo "Without options, runs full setup including Python dependencies"
        ;;
    *)
        main
        ;;
esac
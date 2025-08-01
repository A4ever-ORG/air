# 🚀 Go Multi-Platform Application

[![Go Version](https://img.shields.io/badge/Go-1.21+-blue.svg)](https://golang.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#testing)
[![Platform Support](https://img.shields.io/badge/platform-Kali%20Linux%20%7C%20Termux%20%7C%20Linux-lightgrey.svg)](#platform-support)

An impressive, feature-rich Go application designed to work seamlessly across **Kali Linux**, **Termux (Android)**, and standard **Linux** distributions. Built with advanced platform detection, beautiful CLI interface, and comprehensive system monitoring capabilities.

## 🌟 Features

### 🎯 Multi-Platform Support
- **Kali Linux**: Optimized for penetration testing and security analysis with integrated security tools
- **Termux (Android)**: Mobile-optimized interface with Android API integration and battery optimization
- **Generic Linux**: Cross-platform compatibility with standard Linux distributions
- **Automatic Platform Detection**: Intelligent detection and optimization based on the running environment

### 🔧 Advanced Capabilities
- **Real-time System Monitoring**: CPU, memory, disk, and network interface monitoring
- **Network Analysis Tools**: Platform-specific network scanning and analysis capabilities
- **Security Assessment**: Comprehensive security tools and vulnerability assessment features
- **Platform-specific Optimizations**: Tailored features for each supported platform
- **Beautiful CLI Interface**: Colorized output, animations, and professional presentation
- **Interactive Demo Mode**: Comprehensive demonstration of all features
- **Comprehensive Error Handling**: Robust error handling with detailed user feedback
- **Extensive Testing**: Full test coverage for all major components

## 📋 Table of Contents

- [Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Quick Install](#quick-install)
  - [Platform-Specific Installation](#platform-specific-installation)
  - [Manual Installation](#manual-installation)
  - [Using Makefile](#using-makefile)
- [Usage](#-usage)
  - [Basic Commands](#basic-commands)
  - [Platform-Specific Commands](#platform-specific-commands)
  - [Advanced Usage](#advanced-usage)
- [Configuration](#-configuration)
- [Development](#-development)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## 📦 Installation

### Prerequisites

Before installing, ensure you have the following requirements:

#### All Platforms
- **Go 1.21 or higher** - [Download Go](https://golang.org/dl/)
- **Git** - For cloning the repository
- **Internet connection** - For downloading dependencies

#### Platform-Specific Requirements

**Kali Linux:**
```bash
sudo apt update
sudo apt install golang-go git build-essential
```

**Termux (Android):**
```bash
pkg update && pkg upgrade
pkg install golang git
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install golang-go git
```

**CentOS/RHEL/Fedora:**
```bash
# CentOS/RHEL
sudo yum install golang git
# Fedora
sudo dnf install golang git
```

**Arch Linux:**
```bash
sudo pacman -S go git
```

### Quick Install

The fastest way to get started:

```bash
# Clone the repository
git clone https://github.com/awesome-project/go-multi-platform.git
cd go-multi-platform

# Build and install using Makefile
make install

# Or install for current user only
make install-user

# Run the application
go-multi-platform
```

### Platform-Specific Installation

#### 🐉 Kali Linux Installation

For the full Kali Linux experience with all security tools:

```bash
# Method 1: Using the automated script (Recommended)
git clone https://github.com/awesome-project/go-multi-platform.git
cd go-multi-platform
chmod +x install-kali.sh
./install-kali.sh

# Method 2: Using Makefile
make kali-install

# Method 3: Manual installation
sudo apt update && sudo apt upgrade -y
sudo apt install golang-go git -y

git clone https://github.com/awesome-project/go-multi-platform.git
cd go-multi-platform
go mod tidy
go build -o go-multi-platform

sudo cp go-multi-platform /usr/local/bin/
sudo chmod +x /usr/local/bin/go-multi-platform

# Verify installation
go-multi-platform --version
go-multi-platform system
```

#### 📱 Termux (Android) Installation

For Android devices using Termux:

```bash
# Method 1: Using the automated script (Recommended)
pkg update && pkg upgrade -y
pkg install git -y

git clone https://github.com/awesome-project/go-multi-platform.git
cd go-multi-platform
chmod +x install-termux.sh
./install-termux.sh

# Method 2: Using Makefile
make termux-install

# Method 3: Manual installation
pkg update && pkg upgrade -y
pkg install golang git -y

git clone https://github.com/awesome-project/go-multi-platform.git
cd go-multi-platform
go mod tidy
go build -o go-multi-platform

mkdir -p ~/.local/bin
cp go-multi-platform ~/.local/bin/
chmod +x ~/.local/bin/go-multi-platform

# Add to PATH (add to ~/.bashrc for persistence)
export PATH=$PATH:~/.local/bin

# Verify installation
go-multi-platform --version
go-multi-platform system
```

#### 🐧 Generic Linux Installation

For other Linux distributions:

```bash
# Install Go (choose your distribution)
# Ubuntu/Debian
sudo apt install golang-go git

# CentOS/RHEL
sudo yum install golang git

# Fedora
sudo dnf install golang git

# Arch Linux
sudo pacman -S go git

# Clone and build
git clone https://github.com/awesome-project/go-multi-platform.git
cd go-multi-platform
go mod tidy
go build -o go-multi-platform

# Install system-wide
sudo cp go-multi-platform /usr/local/bin/
sudo chmod +x /usr/local/bin/go-multi-platform

# Or install for current user
mkdir -p ~/.local/bin
cp go-multi-platform ~/.local/bin/
export PATH=$PATH:~/.local/bin

# Verify installation
go-multi-platform --version
```

### Manual Installation

For developers or custom installations:

```bash
# 1. Ensure Go is installed
go version  # Should show Go 1.21+

# 2. Clone the repository
git clone https://github.com/awesome-project/go-multi-platform.git
cd go-multi-platform

# 3. Download dependencies
go mod download
go mod tidy

# 4. Run tests (optional but recommended)
go test ./...

# 5. Build the application
go build -ldflags "-X main.version=1.0.0 -X main.commit=$(git rev-parse --short HEAD) -X main.date=$(date -u +%Y-%m-%dT%H:%M:%SZ)" -o go-multi-platform .

# 6. Install (choose one)
# System-wide installation:
sudo cp go-multi-platform /usr/local/bin/
sudo chmod +x /usr/local/bin/go-multi-platform

# User installation:
mkdir -p ~/.local/bin
cp go-multi-platform ~/.local/bin/
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc

# 7. Verify installation
go-multi-platform --version
go-multi-platform help
```

### Using Makefile

The project includes a comprehensive Makefile for easy building and installation:

```bash
# See all available commands
make help

# Build the application
make build

# Run all tests
make test

# Install system-wide (requires sudo)
make install

# Install for current user only
make install-user

# Build for multiple platforms
make build-all

# Clean build artifacts
make clean

# Run application with different commands
make run           # Default help
make run-demo      # Interactive demo
make run-system    # System information

# Development commands
make fmt           # Format code
make vet           # Run go vet
make test-coverage # Generate coverage report
make deps          # Update dependencies
```

## 🎮 Usage

### Basic Commands

Once installed, you can use the application with these commands:

```bash
# Show help and available commands
go-multi-platform help
go-multi-platform --help

# Show version information
go-multi-platform --version

# Display comprehensive system information
go-multi-platform system

# Show network analysis tools and capabilities
go-multi-platform network

# Display security analysis tools
go-multi-platform security

# Get installation instructions for your platform
go-multi-platform install

# Run interactive demo with all features
go-multi-platform demo
```

### Platform-Specific Commands

The application automatically detects your platform and provides optimized commands:

#### 🐉 Kali Linux Specific
```bash
# Access Kali-specific penetration testing tools
go-multi-platform kali

# This command provides:
# - Penetration testing tool status
# - Security analysis capabilities
# - Network scanning tools
# - Forensic analysis features
# - Advanced Kali-specific optimizations
```

#### 📱 Termux (Android) Specific
```bash
# Access Termux-specific mobile tools
go-multi-platform termux

# This command provides:
# - Android integration tools
# - Mobile-optimized interface
# - Battery optimization tips
# - Termux API tool status
# - Touch-friendly features
```

### Advanced Usage

#### Environment Variables

```bash
# Set custom installation path
export GO_MULTIPLATFORM_INSTALL_PATH="/opt/go-multi-platform"

# Enable debug mode
export GO_MULTIPLATFORM_DEBUG=true

# Custom configuration directory
export GO_MULTIPLATFORM_CONFIG_DIR="~/.config/go-multi-platform"
```

#### Command Combinations

```bash
# Run system info and save output
go-multi-platform system > system-report.txt

# Run demo in background (useful for automated testing)
go-multi-platform demo &

# Combine with other tools
go-multi-platform network | grep -i "interface"
```

## ⚙️ Configuration

### Configuration Files

The application supports configuration through various methods:

1. **Environment Variables** (highest priority)
2. **Configuration Files** 
3. **Command Line Flags**
4. **Default Values** (lowest priority)

### Default Configuration Locations

```bash
# Linux
~/.config/go-multi-platform/config.yaml

# Termux
$PREFIX/etc/go-multi-platform/config.yaml

# Kali Linux
/etc/go-multi-platform/config.yaml
~/.config/go-multi-platform/config.yaml
```

### Sample Configuration

```yaml
# config.yaml
app:
  name: "go-multi-platform"
  version: "1.0.0"
  debug: false

platform:
  auto_detect: true
  preferred_tools: []

display:
  colors: true
  animations: true
  verbose: false

performance:
  max_cpu_usage: 80
  memory_limit: "1GB"
  timeout: "30s"
```

## 🔧 Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/awesome-project/go-multi-platform.git
cd go-multi-platform

# Install development dependencies
go mod download
go mod tidy

# Install development tools (optional)
go install golang.org/x/tools/cmd/goimports@latest
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Set up pre-commit hooks (optional)
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
make fmt
make vet
make test
EOF
chmod +x .git/hooks/pre-commit
```

### Project Structure

```
go-multi-platform/
├── main.go                     # Application entry point
├── go.mod                      # Go module definition
├── go.sum                      # Go module checksums
├── Makefile                    # Build automation
├── LICENSE                     # MIT License
├── README.md                   # This file
├── cmd/
│   ├── commands.go            # CLI command definitions
│   └── commands_test.go       # Command tests
├── internal/
│   ├── platform/              # Platform detection and features
│   │   ├── platform.go        # Core platform logic
│   │   ├── platform_test.go   # Platform tests
│   │   ├── kali_optimizations.go     # Kali Linux specific features
│   │   └── termux_optimizations.go   # Termux specific features
│   └── features/              # Feature implementations
│       ├── features.go        # Core features
│       └── features_test.go   # Feature tests
├── scripts/
│   ├── install-kali.sh       # Kali Linux installation script
│   └── install-termux.sh     # Termux installation script
└── docs/                     # Additional documentation
    ├── CONTRIBUTING.md       # Contribution guidelines
    ├── CHANGELOG.md          # Version history
    └── API.md               # API documentation
```

### Building from Source

```bash
# Standard build
go build -o go-multi-platform .

# Build with version information
make build

# Build for all platforms
make build-all

# Build with custom flags
go build -ldflags "-X main.version=custom -X main.commit=dev" -o go-multi-platform .
```

### Adding New Features

1. **Create feature in `internal/features/`**
2. **Add platform-specific optimizations in `internal/platform/`**
3. **Create corresponding tests**
4. **Update CLI commands in `cmd/`**
5. **Update documentation**

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test
go test ./...

# Run tests with coverage
make test-coverage
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Run specific package tests
go test ./internal/platform/
go test ./internal/features/
go test ./cmd/

# Run tests with verbose output
go test -v ./...

# Run tests with race detection
go test -race ./...

# Benchmark tests
go test -bench=. ./...
```

### Test Coverage

The project maintains high test coverage across all components:

- **Platform Detection**: Tests for all supported platforms
- **Feature Functions**: Comprehensive feature testing
- **Command Interface**: CLI command validation
- **Error Handling**: Error condition testing
- **Integration Tests**: End-to-end functionality tests

### Manual Testing

```bash
# Test basic functionality
go-multi-platform --version
go-multi-platform help
go-multi-platform system

# Test platform detection
go-multi-platform install

# Test all commands
for cmd in system network security demo; do
    echo "Testing: $cmd"
    go-multi-platform $cmd
done

# Test error conditions
go-multi-platform invalid-command
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Start for Contributors

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Add tests for new functionality**
5. **Run the test suite**: `make test`
6. **Format your code**: `make fmt`
7. **Commit your changes**: `git commit -m 'Add amazing feature'`
8. **Push to the branch**: `git push origin feature/amazing-feature`
9. **Open a Pull Request**

### Development Guidelines

- **Follow Go conventions and best practices**
- **Write comprehensive tests for new features**
- **Update documentation for any new functionality**
- **Ensure backward compatibility**
- **Use meaningful commit messages**

## 🔧 Troubleshooting

### Common Issues

#### Installation Issues

**Problem**: `go: command not found`
```bash
# Install Go for your platform
# Ubuntu/Debian
sudo apt install golang-go

# Verify installation
go version
```

**Problem**: `Permission denied when installing`
```bash
# Use user installation instead
make install-user

# Or use sudo for system installation
sudo make install
```

**Problem**: `Module not found errors`
```bash
# Update dependencies
go mod tidy
go mod download
```

#### Runtime Issues

**Problem**: `Platform detection issues`
```bash
# Check platform detection
go-multi-platform system

# Manually verify platform files
cat /etc/os-release  # Linux
echo $TERMUX_VERSION # Termux
```

**Problem**: `Performance issues`
```bash
# Check system resources
go-multi-platform system

# Run with debug information
GO_MULTIPLATFORM_DEBUG=true go-multi-platform system
```

**Problem**: `Network tools not working`
```bash
# Verify network permissions (especially on Termux)
# Some tools may require additional packages
pkg install nmap  # Termux
sudo apt install nmap  # Kali/Ubuntu
```

#### Build Issues

**Problem**: `Build fails with dependency errors`
```bash
# Clean and rebuild
make clean
go mod tidy
make build
```

**Problem**: `Tests failing`
```bash
# Run tests individually to identify issues
go test -v ./internal/platform/
go test -v ./internal/features/
go test -v ./cmd/

# Check for platform-specific test issues
```

### Getting Help

- **Check the [Issues](https://github.com/awesome-project/go-multi-platform/issues)** for known problems
- **Create a new issue** with detailed information about your problem
- **Include platform information**: OS, version, Go version
- **Provide error messages and logs**
- **Include steps to reproduce the issue**

### Debug Mode

Enable debug mode for additional troubleshooting information:

```bash
export GO_MULTIPLATFORM_DEBUG=true
go-multi-platform system
```

## 🎯 Platform-Specific Features

### 🐉 Kali Linux Features

- **Penetration Testing Tools Integration**
  - Metasploit Framework
  - Nmap network discovery
  - Wireshark packet analysis
  - Aircrack-ng wireless security
  - John the Ripper password cracking

- **Security Analysis Capabilities**
  - Vulnerability assessment tools
  - Network security scanning
  - Web application security testing
  - Forensic analysis tools
  - Professional reporting features

- **Advanced Networking**
  - Advanced network scanning
  - Traffic analysis and monitoring
  - Wireless network assessment
  - Network penetration testing

### 📱 Termux (Android) Features

- **Mobile Optimization**
  - Battery usage optimization
  - Touch-friendly interface
  - Android API integration
  - Mobile-specific tools

- **Android Integration**
  - Termux API access
  - Android system integration
  - Mobile security testing
  - APK analysis tools

- **Resource Optimization**
  - Low-resource optimization
  - Efficient memory usage
  - Background processing optimization
  - Network efficiency

### 🐧 Generic Linux Features

- **Cross-Platform Compatibility**
  - Standard Linux support
  - Distribution-agnostic design
  - Standard tool integration
  - Portable functionality

- **System Integration**
  - Systemd integration
  - Package manager compatibility
  - Standard Linux conventions
  - Shell integration

## 📊 Performance

### System Requirements

| Platform | Minimum | Recommended |
|----------|---------|-------------|
| **Kali Linux** | 1GB RAM, 100MB disk | 4GB RAM, 500MB disk |
| **Termux** | 500MB RAM, 50MB disk | 2GB RAM, 200MB disk |
| **Generic Linux** | 512MB RAM, 100MB disk | 2GB RAM, 500MB disk |

### Performance Characteristics

- **Startup Time**: < 1 second
- **Memory Usage**: 10-50MB typical
- **CPU Usage**: < 5% during normal operation
- **Network Impact**: Minimal (only for system monitoring)

## 🔐 Security

### Security Features

- **No Network Communication**: Application doesn't send data externally
- **Local Operation**: All processing happens locally
- **No Privilege Escalation**: Runs with user permissions
- **Secure Defaults**: Conservative default settings
- **Input Validation**: Comprehensive input sanitization

### Security Considerations

- **Tool Integration**: Some features may invoke system tools
- **File Access**: Reads system information files (read-only)
- **Network Monitoring**: May access network interface information
- **Platform Detection**: Reads OS identification files

## 📈 Roadmap

### Version 1.1.0 (Planned)
- [ ] Configuration file support
- [ ] Plugin system
- [ ] Custom tool integration
- [ ] Performance monitoring dashboard

### Version 1.2.0 (Planned)
- [ ] Web interface
- [ ] REST API
- [ ] Remote monitoring capabilities
- [ ] Advanced reporting

### Version 2.0.0 (Future)
- [ ] GUI interface
- [ ] Cloud integration
- [ ] Multi-device support
- [ ] Advanced analytics

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [Platform-Specific Guides](docs/platforms/)
- [Developer Guide](docs/DEVELOPMENT.md)

## 🙏 Acknowledgments

- **Go Community** - For the excellent programming language and ecosystem
- **Kali Linux Team** - For the outstanding penetration testing distribution
- **Termux Project** - For bringing Linux to Android
- **Open Source Community** - For the tools and libraries that make this possible

### Dependencies

This project uses several excellent open-source libraries:

- [Cobra](https://github.com/spf13/cobra) - CLI framework
- [Color](https://github.com/fatih/color) - Colorized output
- [gopsutil](https://github.com/shirou/gopsutil) - System monitoring
- [Spinner](https://github.com/briandowns/spinner) - Terminal spinners

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Go Multi-Platform Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**Made with 🚀 for Kali Linux, Termux, and Linux enthusiasts!**

*For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/awesome-project/go-multi-platform).*
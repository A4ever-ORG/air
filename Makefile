# 🚀 Go Multi-Platform Makefile
# Advanced Go application for Kali Linux and Termux

BINARY_NAME=go-multi-platform
VERSION=1.0.0
BUILD_DIR=build
INSTALL_PATH=/usr/local/bin

# Go parameters
GOCMD=go
GOBUILD=$(GOCMD) build
GOCLEAN=$(GOCMD) clean
GOTEST=$(GOCMD) test
GOGET=$(GOCMD) get
GOMOD=$(GOCMD) mod

# Build flags
LDFLAGS=-ldflags "-X main.version=$(VERSION) -X main.commit=$(shell git rev-parse --short HEAD 2>/dev/null || echo 'dev') -X main.date=$(shell date -u +%Y-%m-%dT%H:%M:%SZ)"

.PHONY: all build clean test deps help install uninstall run

all: clean deps test build

## Build Commands
build: ## Build the application
	@echo "🔨 Building $(BINARY_NAME)..."
	$(GOBUILD) $(LDFLAGS) -o $(BINARY_NAME) .
	@echo "✅ Build completed: $(BINARY_NAME)"

build-all: ## Build for all platforms
	@echo "🔨 Building for multiple platforms..."
	@mkdir -p $(BUILD_DIR)
	GOOS=linux GOARCH=amd64 $(GOBUILD) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME)-linux-amd64 .
	GOOS=linux GOARCH=arm64 $(GOBUILD) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME)-linux-arm64 .
	GOOS=android GOARCH=arm64 $(GOBUILD) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME)-android-arm64 .
	GOOS=darwin GOARCH=amd64 $(GOBUILD) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME)-darwin-amd64 .
	GOOS=darwin GOARCH=arm64 $(GOBUILD) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME)-darwin-arm64 .
	@echo "✅ Multi-platform build completed in $(BUILD_DIR)/"

## Development Commands
test: ## Run tests
	@echo "🧪 Running tests..."
	$(GOTEST) -v ./...
	@echo "✅ Tests completed"

test-coverage: ## Run tests with coverage
	@echo "🧪 Running tests with coverage..."
	$(GOTEST) -v -coverprofile=coverage.out ./...
	$(GOCMD) tool cover -html=coverage.out -o coverage.html
	@echo "✅ Coverage report generated: coverage.html"

deps: ## Download dependencies
	@echo "📦 Downloading dependencies..."
	$(GOMOD) download
	$(GOMOD) tidy
	@echo "✅ Dependencies updated"

vet: ## Run go vet
	@echo "🔍 Running go vet..."
	$(GOCMD) vet ./...
	@echo "✅ Vet completed"

fmt: ## Format code
	@echo "✨ Formatting code..."
	$(GOCMD) fmt ./...
	@echo "✅ Code formatted"

lint: ## Run golangci-lint (requires golangci-lint to be installed)
	@echo "🔍 Running golangci-lint..."
	@if command -v golangci-lint >/dev/null 2>&1; then \
		golangci-lint run; \
	else \
		echo "⚠️  golangci-lint not installed. Install with: curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b \$$(go env GOPATH)/bin v1.54.2"; \
	fi

## Installation Commands
install: build ## Install the application system-wide
	@echo "📦 Installing $(BINARY_NAME) to $(INSTALL_PATH)..."
	@if [ "$(shell id -u)" = "0" ]; then \
		cp $(BINARY_NAME) $(INSTALL_PATH)/; \
		chmod +x $(INSTALL_PATH)/$(BINARY_NAME); \
		echo "✅ $(BINARY_NAME) installed to $(INSTALL_PATH)"; \
	else \
		echo "🔒 Installing to $(INSTALL_PATH) requires sudo:"; \
		sudo cp $(BINARY_NAME) $(INSTALL_PATH)/; \
		sudo chmod +x $(INSTALL_PATH)/$(BINARY_NAME); \
		echo "✅ $(BINARY_NAME) installed to $(INSTALL_PATH)"; \
	fi

install-user: build ## Install the application for current user
	@echo "📦 Installing $(BINARY_NAME) to ~/.local/bin..."
	@mkdir -p ~/.local/bin
	cp $(BINARY_NAME) ~/.local/bin/
	chmod +x ~/.local/bin/$(BINARY_NAME)
	@echo "✅ $(BINARY_NAME) installed to ~/.local/bin"
	@echo "💡 Make sure ~/.local/bin is in your PATH"

uninstall: ## Uninstall the application
	@echo "🗑️  Uninstalling $(BINARY_NAME)..."
	@if [ -f "$(INSTALL_PATH)/$(BINARY_NAME)" ]; then \
		if [ "$(shell id -u)" = "0" ]; then \
			rm -f $(INSTALL_PATH)/$(BINARY_NAME); \
		else \
			sudo rm -f $(INSTALL_PATH)/$(BINARY_NAME); \
		fi; \
		echo "✅ $(BINARY_NAME) uninstalled from $(INSTALL_PATH)"; \
	else \
		echo "ℹ️  $(BINARY_NAME) not found in $(INSTALL_PATH)"; \
	fi
	@if [ -f "~/.local/bin/$(BINARY_NAME)" ]; then \
		rm -f ~/.local/bin/$(BINARY_NAME); \
		echo "✅ $(BINARY_NAME) uninstalled from ~/.local/bin"; \
	fi

## Utility Commands
clean: ## Clean build artifacts
	@echo "🧹 Cleaning build artifacts..."
	$(GOCLEAN)
	rm -f $(BINARY_NAME)
	rm -rf $(BUILD_DIR)
	rm -f coverage.out coverage.html
	rm -f test-binary
	@echo "✅ Cleanup completed"

run: build ## Build and run the application
	@echo "🚀 Running $(BINARY_NAME)..."
	./$(BINARY_NAME)

run-demo: build ## Build and run demo
	@echo "🎮 Running demo..."
	./$(BINARY_NAME) demo

run-system: build ## Build and run system info
	@echo "🔍 Running system info..."
	./$(BINARY_NAME) system

## Platform-specific commands
kali-install: ## Install with Kali Linux script
	@echo "⚔️ Running Kali Linux installation..."
	@if [ -f "install-kali.sh" ]; then \
		chmod +x install-kali.sh; \
		./install-kali.sh; \
	else \
		echo "❌ install-kali.sh not found"; \
	fi

termux-install: ## Install with Termux script
	@echo "📱 Running Termux installation..."
	@if [ -f "install-termux.sh" ]; then \
		chmod +x install-termux.sh; \
		./install-termux.sh; \
	else \
		echo "❌ install-termux.sh not found"; \
	fi

## Help
help: ## Show this help message
	@echo "🚀 Go Multi-Platform - Build System"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Examples:"
	@echo "  make build          - Build the application"
	@echo "  make test           - Run all tests"
	@echo "  make install        - Install system-wide"
	@echo "  make install-user   - Install for current user"
	@echo "  make run-demo       - Build and run demo"
	@echo ""

# Default target
.DEFAULT_GOAL := help
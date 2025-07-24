# CodeRoot Bot Makefile
# Common commands for development and deployment

.PHONY: help install setup run clean test docker-build docker-run docker-stop logs

# Default target
help:
	@echo "CodeRoot Bot - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  install     - Install Python dependencies"
	@echo "  setup       - Setup environment and configuration"
	@echo "  run         - Run the bot locally"
	@echo "  clean       - Clean temporary files and cache"
	@echo "  test        - Run tests (if available)"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run with Docker Compose"
	@echo "  docker-stop  - Stop Docker containers"
	@echo "  docker-logs  - View Docker logs"
	@echo ""
	@echo "Utilities:"
	@echo "  logs        - View bot logs"
	@echo "  backup      - Backup database"
	@echo "  restore     - Restore database"
	@echo ""

# Development commands
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed successfully!"

setup:
	@echo "🔧 Setting up environment..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "📝 .env file created. Please edit it with your configuration."; \
	else \
		echo "⚠️  .env file already exists."; \
	fi
	@mkdir -p logs
	@echo "✅ Setup completed!"

run:
	@echo "🚀 Starting CodeRoot Bot..."
	python run.py

clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	find . -name ".coverage" -delete
	find . -name "*.cover" -delete
	find . -name "*.log" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	@echo "✅ Cleanup completed!"

test:
	@echo "🧪 Running tests..."
	@if [ -f tests/test_*.py ]; then \
		python -m pytest tests/ -v; \
	else \
		echo "⚠️  No tests found. Create tests in tests/ directory."; \
	fi

# Docker commands
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t coderoot-bot .
	@echo "✅ Docker image built successfully!"

docker-run:
	@echo "🐳 Starting with Docker Compose..."
	docker-compose up -d
	@echo "✅ Services started! Use 'make docker-logs' to view logs."

docker-stop:
	@echo "🛑 Stopping Docker containers..."
	docker-compose down
	@echo "✅ Containers stopped!"

docker-logs:
	@echo "📋 Viewing Docker logs..."
	docker-compose logs -f coderoot_bot

# Utility commands
logs:
	@echo "📋 Viewing bot logs..."
	@if [ -f logs/bot.log ]; then \
		tail -f logs/bot.log; \
	else \
		echo "⚠️  No log file found. Run the bot first."; \
	fi

backup:
	@echo "💾 Creating database backup..."
	@mkdir -p backups
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	if command -v mongodump >/dev/null 2>&1; then \
		mongodump --host localhost:27017 --db coderoot_bot --out backups/backup_$$timestamp; \
		echo "✅ Backup created: backups/backup_$$timestamp"; \
	else \
		echo "❌ mongodump not found. Please install MongoDB tools."; \
	fi

restore:
	@echo "📥 Restoring database..."
	@if [ -z "$(BACKUP_PATH)" ]; then \
		echo "❌ Please specify BACKUP_PATH. Usage: make restore BACKUP_PATH=backups/backup_20231201_120000"; \
	else \
		if command -v mongorestore >/dev/null 2>&1; then \
			mongorestore --host localhost:27017 --db coderoot_bot --drop $(BACKUP_PATH)/coderoot_bot; \
			echo "✅ Database restored from $(BACKUP_PATH)"; \
		else \
			echo "❌ mongorestore not found. Please install MongoDB tools."; \
		fi \
	fi

# Environment check
check-env:
	@echo "🔍 Checking environment..."
	@python -c "import os; missing = [var for var in ['BOT_TOKEN', 'API_ID', 'API_HASH', 'ADMIN_USER_ID'] if not os.getenv(var)]; print('❌ Missing variables:', missing) if missing else print('✅ Environment configured correctly')"

# Install development dependencies
dev-install:
	@echo "🛠️  Installing development dependencies..."
	pip install pytest pytest-asyncio black flake8 mypy
	@echo "✅ Development dependencies installed!"

# Format code
format:
	@echo "🎨 Formatting code..."
	black --line-length 100 .
	@echo "✅ Code formatted!"

# Lint code
lint:
	@echo "🔍 Linting code..."
	flake8 --max-line-length=100 --ignore=E203,W503 .
	@echo "✅ Linting completed!"

# Type checking
typecheck:
	@echo "🔎 Type checking..."
	mypy --ignore-missing-imports .
	@echo "✅ Type checking completed!"

# Show project status
status:
	@echo "📊 Project Status:"
	@echo "=================="
	@echo "🐍 Python Version: $$(python --version)"
	@echo "📦 Dependencies: $$(pip list | wc -l) packages installed"
	@if [ -f .env ]; then echo "⚙️  Environment: Configured"; else echo "⚙️  Environment: Not configured"; fi
	@if [ -d logs ]; then echo "📋 Logs: Available in logs/"; else echo "📋 Logs: No logs directory"; fi
	@echo "🐳 Docker: $$(if command -v docker >/dev/null 2>&1; then echo 'Available'; else echo 'Not installed'; fi)"
	@echo "💾 MongoDB: $$(if command -v mongod >/dev/null 2>&1; then echo 'Available'; else echo 'Not installed'; fi)"
package config

import (
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

// Config holds all configuration for the application
type Config struct {
	// Telegram Bot Configuration
	BotToken string
	APIId    int64
	APIHash  string

	// Admin Configuration
	AdminUserID   int64
	AdminUsername string

	// Mode Configuration
	DemoMode       bool
	ProductionMode bool

	// Database Configuration
	MongoURI     string
	DatabaseName string
	RedisURL     string

	// Server Configuration
	ServerPort string
	ServerHost string

	// Payment Configuration
	CardNumber     string
	CardHolderName string

	// Channel Configuration
	MainChannelID       int64
	MainChannelUsername string

	// Pricing Configuration
	ProfessionalPlanPrice int
	VIPPlanPrice          int
	CommissionRate        int

	// Bot Settings
	BotUsername string
	WebhookURL  string

	// Sub-bot Creation
	BotFatherToken string
	SubBotPrefix   string

	// Backup and Logging
	BackupEnabled bool
	LogLevel      string
	LogFile       string

	// Security
	SecretKey string

	// Default Settings
	DefaultLanguage     string
	MaxShopsPerUser     int
	SessionTimeout      int
	MaxConcurrentUsers  int
	RateLimitPerMinute  int
}

// Load loads configuration from environment variables
func Load() (*Config, error) {
	// Load .env file if it exists
	_ = godotenv.Load()

	cfg := &Config{
		// Telegram Bot Configuration
		BotToken: getEnv("BOT_TOKEN", ""),
		APIId:    getEnvInt64("API_ID", 0),
		APIHash:  getEnv("API_HASH", ""),

		// Admin Configuration
		AdminUserID:   getEnvInt64("ADMIN_USER_ID", 0),
		AdminUsername: getEnv("ADMIN_USERNAME", ""),

		// Mode Configuration
		DemoMode:       getEnvBool("DEMO_MODE", false),
		ProductionMode: getEnvBool("PRODUCTION_MODE", true),

		// Database Configuration
		MongoURI:     getEnv("MONGO_URI", "mongodb://localhost:27017/"),
		DatabaseName: getEnv("DATABASE_NAME", "coderoot_production"),
		RedisURL:     getEnv("REDIS_URL", "redis://localhost:6379"),

		// Server Configuration
		ServerPort: getEnv("SERVER_PORT", "8080"),
		ServerHost: getEnv("SERVER_HOST", "0.0.0.0"),

		// Payment Configuration
		CardNumber:     getEnv("CARD_NUMBER", "6037-9977-7766-5544"),
		CardHolderName: getEnv("CARD_HOLDER_NAME", "حادی"),

		// Channel Configuration
		MainChannelID:       getEnvInt64("MAIN_CHANNEL_ID", -1001234567890),
		MainChannelUsername: getEnv("MAIN_CHANNEL_USERNAME", "coderoot_channel"),

		// Pricing Configuration
		ProfessionalPlanPrice: getEnvInt("PROFESSIONAL_PLAN_PRICE", 20000),
		VIPPlanPrice:          getEnvInt("VIP_PLAN_PRICE", 60000),
		CommissionRate:        getEnvInt("COMMISSION_RATE", 5),

		// Bot Settings
		BotUsername: getEnv("BOT_USERNAME", "coderoot_main_bot"),
		WebhookURL:  getEnv("WEBHOOK_URL", ""),

		// Sub-bot Creation
		BotFatherToken: getEnv("BOTFATHER_TOKEN", ""),
		SubBotPrefix:   getEnv("SUB_BOT_PREFIX", "shop_"),

		// Backup and Logging
		BackupEnabled: getEnvBool("BACKUP_ENABLED", true),
		LogLevel:      getEnv("LOG_LEVEL", "INFO"),
		LogFile:       getEnv("LOG_FILE", "logs/coderoot.log"),

		// Security
		SecretKey: getEnv("SECRET_KEY", "your_secret_key_here"),

		// Default Settings
		DefaultLanguage:     getEnv("DEFAULT_LANGUAGE", "fa"),
		MaxShopsPerUser:     getEnvInt("MAX_SHOPS_PER_USER", 3),
		SessionTimeout:      getEnvInt("SESSION_TIMEOUT", 3600),
		MaxConcurrentUsers:  getEnvInt("MAX_CONCURRENT_USERS", 1000),
		RateLimitPerMinute:  getEnvInt("RATE_LIMIT_PER_MINUTE", 60),
	}

	return cfg, nil
}

// Helper functions
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if i, err := strconv.Atoi(value); err == nil {
			return i
		}
	}
	return defaultValue
}

func getEnvInt64(key string, defaultValue int64) int64 {
	if value := os.Getenv(key); value != "" {
		if i, err := strconv.ParseInt(value, 10, 64); err == nil {
			return i
		}
	}
	return defaultValue
}

func getEnvBool(key string, defaultValue bool) bool {
	if value := os.Getenv(key); value != "" {
		if b, err := strconv.ParseBool(value); err == nil {
			return b
		}
	}
	return defaultValue
}
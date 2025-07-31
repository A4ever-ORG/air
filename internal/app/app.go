package app

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"

	"coderoot-bot/internal/config"
	"coderoot-bot/internal/database"
	"coderoot-bot/internal/handlers"
	"coderoot-bot/internal/logger"
	"coderoot-bot/internal/services"
	"coderoot-bot/internal/utils"
)

// App represents the main application
type App struct {
	config   *config.Config
	logger   *logger.Logger
	db       *database.Database
	bot      *tgbotapi.BotAPI
	server   *http.Server
	handlers *handlers.Handler
	services *services.Services
	utils    *utils.Utils
}

// New creates a new application instance
func New(cfg *config.Config, logger *logger.Logger) (*App, error) {
	app := &App{
		config: cfg,
		logger: logger,
	}

	// Initialize database
	if err := app.initDatabase(); err != nil {
		return nil, fmt.Errorf("failed to initialize database: %w", err)
	}

	// Initialize Telegram bot
	if err := app.initBot(); err != nil {
		return nil, fmt.Errorf("failed to initialize bot: %w", err)
	}

	// Initialize services
	if err := app.initServices(); err != nil {
		return nil, fmt.Errorf("failed to initialize services: %w", err)
	}

	// Initialize utils
	app.utils = utils.New(cfg, logger)

	// Initialize handlers
	app.handlers = handlers.New(cfg, logger, app.db, app.services, app.utils)

	// Initialize HTTP server
	if err := app.initServer(); err != nil {
		return nil, fmt.Errorf("failed to initialize server: %w", err)
	}

	logger.Info("✅ Application initialized successfully")
	return app, nil
}

// Start starts the application
func (a *App) Start(ctx context.Context) error {
	a.logger.Info("🚀 Starting CodeRoot Bot application...")

	// Create database indexes
	if err := a.db.CreateIndexes(ctx); err != nil {
		return fmt.Errorf("failed to create database indexes: %w", err)
	}

	// Start HTTP server for health checks
	go func() {
		addr := fmt.Sprintf("%s:%s", a.config.ServerHost, a.config.ServerPort)
		a.logger.Info("🌐 Starting HTTP server on %s", addr)

		if err := a.server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			a.logger.Error("❌ HTTP server error: %v", err)
		}
	}()

	// Start bot polling
	if err := a.startBot(ctx); err != nil {
		return fmt.Errorf("failed to start bot: %w", err)
	}

	return nil
}

// Stop stops the application gracefully
func (a *App) Stop() error {
	a.logger.Info("🔄 Stopping application...")

	// Stop bot
	a.bot.StopReceivingUpdates()

	// Stop HTTP server
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := a.server.Shutdown(ctx); err != nil {
		a.logger.Error("❌ Error shutting down HTTP server: %v", err)
	}

	// Close database connections
	if err := a.db.Close(ctx); err != nil {
		a.logger.Error("❌ Error closing database: %v", err)
		return err
	}

	a.logger.Info("✅ Application stopped successfully")
	return nil
}

// initDatabase initializes database connections
func (a *App) initDatabase() error {
	db, err := database.New(a.config, a.logger)
	if err != nil {
		return err
	}
	a.db = db
	return nil
}

// initBot initializes Telegram bot
func (a *App) initBot() error {
	if a.config.BotToken == "" {
		return fmt.Errorf("bot token is required")
	}

	bot, err := tgbotapi.NewBotAPI(a.config.BotToken)
	if err != nil {
		return err
	}

	bot.Debug = !a.config.ProductionMode
	a.bot = bot

	a.logger.Info("✅ Connected to Telegram Bot: @%s", bot.Self.UserName)
	return nil
}

// initServices initializes all services
func (a *App) initServices() error {
	services, err := services.New(a.config, a.logger, a.db)
	if err != nil {
		return err
	}
	a.services = services
	return nil
}

// initServer initializes HTTP server for health checks
func (a *App) initServer() error {
	gin.SetMode(gin.ReleaseMode)
	router := gin.New()
	router.Use(gin.Recovery())

	// Health check endpoint
	router.GET("/health", a.healthCheck)
	router.GET("/", a.healthCheck)

	// Metrics endpoint
	router.GET("/metrics", a.metricsHandler)

	a.server = &http.Server{
		Addr:    fmt.Sprintf("%s:%s", a.config.ServerHost, a.config.ServerPort),
		Handler: router,
	}

	return nil
}

// startBot starts the Telegram bot
func (a *App) startBot(ctx context.Context) error {
	// Configure update config
	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60

	updates := a.bot.GetUpdatesChan(u)

	// Handle updates
	go func() {
		for {
			select {
			case <-ctx.Done():
				a.logger.Info("🛑 Bot polling stopped")
				return
			case update := <-updates:
				// Process update in goroutine to avoid blocking
				go a.handleUpdate(update)
			}
		}
	}()

	a.logger.Info("🤖 Bot polling started successfully")
	return nil
}

// handleUpdate handles incoming Telegram updates
func (a *App) handleUpdate(update tgbotapi.Update) {
	defer func() {
		if r := recover(); r != nil {
			a.logger.Error("❌ Panic in update handler: %v", r)
		}
	}()

	ctx := context.Background()

	// Handle different update types
	if update.Message != nil {
		a.handlers.HandleMessage(ctx, a.bot, update.Message)
	} else if update.CallbackQuery != nil {
		a.handlers.HandleCallbackQuery(ctx, a.bot, update.CallbackQuery)
	} else if update.InlineQuery != nil {
		a.handlers.HandleInlineQuery(ctx, a.bot, update.InlineQuery)
	}
}

// healthCheck handles health check requests
func (a *App) healthCheck(c *gin.Context) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// Check database health
	if err := a.db.Health(ctx); err != nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{
			"status": "unhealthy",
			"error":  err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "healthy",
		"time":   time.Now().UTC(),
		"bot":    a.bot.Self.UserName,
	})
}

// metricsHandler handles metrics requests
func (a *App) metricsHandler(c *gin.Context) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Get user stats
	userStats, err := a.db.Users.GetUserStats(ctx)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to get user stats",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"users": userStats,
		"time":  time.Now().UTC(),
	})
}

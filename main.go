package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"syscall"

	"coderoot-bot/internal/app"
	"coderoot-bot/internal/config"
	"coderoot-bot/internal/logger"
)

func main() {
	// Initialize logger
	logger := logger.New()
	
	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("❌ Failed to load config: %v", err)
	}
	
	logger.Info("🚀 Starting CodeRoot Bot...")
	
	// Create application
	application, err := app.New(cfg, logger)
	if err != nil {
		logger.Fatal("❌ Failed to create application: %v", err)
	}
	
	// Create context for graceful shutdown
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	
	// Start the application
	go func() {
		if err := application.Start(ctx); err != nil {
			logger.Error("❌ Application error: %v", err)
			cancel()
		}
	}()
	
	logger.Info("🤖 CodeRoot Bot is running...")
	logger.Info("Press Ctrl+C to stop")
	
	// Wait for interrupt signal
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	
	select {
	case <-sigChan:
		logger.Info("🛑 Received shutdown signal")
	case <-ctx.Done():
		logger.Info("🛑 Context cancelled")
	}
	
	// Graceful shutdown
	logger.Info("🔄 Shutting down gracefully...")
	if err := application.Stop(); err != nil {
		logger.Error("❌ Error during shutdown: %v", err)
	}
	
	logger.Info("✅ CodeRoot Bot stopped")
}
package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"runtime"
	"syscall"
	"time"

	"coderoot-bot/internal/app"
	"coderoot-bot/internal/config"
	"coderoot-bot/internal/health"
	"coderoot-bot/internal/logger"
	"coderoot-bot/internal/monitoring"
)

var (
	version = "2.0.0"
	commit  = "liara-optimized"
	date    = time.Now().Format("2006-01-02")
)

func main() {
	// Initialize logger with enhanced configuration
	logger := logger.New()

	// Load configuration with validation
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("❌ Failed to load config: %v", err)
	}

	// Validate configuration
	if err := cfg.Validate(); err != nil {
		log.Fatalf("❌ Invalid configuration: %v", err)
	}

	// Set runtime optimizations for Liara
	setLiaraOptimizations()

	logger.Info("🚀 Starting CodeRoot Bot v%s...", version)
	logger.Info("📍 Environment: %s", os.Getenv("ENVIRONMENT"))
	logger.Info("🔧 Go Version: %s", runtime.Version())
	logger.Info("💾 Memory: %d MB", runtime.MemStats{}.Alloc/1024/1024)

	// Create application with enhanced error handling
	application, err := app.New(cfg, logger)
	if err != nil {
		logger.Fatal("❌ Failed to create application: %v", err)
	}

	// Initialize monitoring
	monitor := monitoring.New(logger)
	go monitor.Start()

	// Initialize health check server
	healthServer := health.NewServer(logger)
	go func() {
		if err := healthServer.Start(":8080"); err != nil && err != http.ErrServerClosed {
			logger.Error("❌ Health server error: %v", err)
		}
	}()

	// Create context for graceful shutdown
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Start the application with enhanced monitoring
	go func() {
		if err := application.Start(ctx); err != nil {
			logger.Error("❌ Application error: %v", err)
			cancel()
		}
	}()

	logger.Info("🤖 CodeRoot Bot is running on Liara...")
	logger.Info("📊 Health check available at: http://localhost:8080/health")
	logger.Info("📈 Metrics available at: http://localhost:8080/metrics")
	logger.Info("🔄 Press Ctrl+C to stop")

	// Wait for interrupt signal with timeout
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	select {
	case <-sigChan:
		logger.Info("🛑 Received shutdown signal")
	case <-ctx.Done():
		logger.Info("🛑 Context cancelled")
	case <-time.After(24 * time.Hour): // Auto-restart after 24 hours for Liara
		logger.Info("🔄 Auto-restart after 24 hours")
	}

	// Graceful shutdown with timeout
	logger.Info("🔄 Shutting down gracefully...")

	// Stop health server
	if err := healthServer.Stop(); err != nil {
		logger.Error("❌ Error stopping health server: %v", err)
	}

	// Stop monitoring
	monitor.Stop()

	// Stop application
	if err := application.Stop(); err != nil {
		logger.Error("❌ Error during shutdown: %v", err)
	}

	logger.Info("✅ CodeRoot Bot stopped gracefully")
}

func setLiaraOptimizations() {
	// Set environment variables for Liara optimization
	os.Setenv("GOMAXPROCS", fmt.Sprintf("%d", runtime.NumCPU()))
	os.Setenv("GOGC", "50")  // Optimize garbage collection
	os.Setenv("GORACE", "0") // Disable race detection in production

	// Set Liara-specific environment variables
	if os.Getenv("ENVIRONMENT") == "" {
		os.Setenv("ENVIRONMENT", "production")
	}

	// Optimize for cloud deployment
	os.Setenv("TZ", "UTC")
	os.Setenv("LANG", "en_US.UTF-8")

	// Set memory limits for Liara
	os.Setenv("GOMEMLIMIT", "512MiB")

	// Enable HTTP/2 for better performance
	os.Setenv("GODEBUG", "http2server=1")
}

// Health check endpoint for Liara
func healthCheck(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, `{
		"status": "healthy",
		"version": "%s",
		"timestamp": "%s",
		"uptime": "%v",
		"memory": {
			"alloc": "%d MB",
			"total": "%d MB",
			"sys": "%d MB"
		},
		"goroutines": %d,
		"environment": "%s"
	}`, version, time.Now().Format(time.RFC3339), time.Since(startTime),
		runtime.MemStats{}.Alloc/1024/1024,
		runtime.MemStats{}.TotalAlloc/1024/1024,
		runtime.MemStats{}.Sys/1024/1024,
		runtime.NumGoroutine(),
		os.Getenv("ENVIRONMENT"))
}

var startTime = time.Now()

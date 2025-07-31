package health

import (
	"context"
	"encoding/json"
	"net/http"
	"runtime"
	"time"

	"coderoot-bot/internal/logger"
)

type Server struct {
	logger *logger.Logger
	server *http.Server
}

func NewServer(logger *logger.Logger) *Server {
	return &Server{
		logger: logger,
	}
}

func (s *Server) Start(addr string) error {
	mux := http.NewServeMux()

	// Health check endpoint
	mux.HandleFunc("/health", s.healthHandler)

	// Metrics endpoint
	mux.HandleFunc("/metrics", s.metricsHandler)

	// Status endpoint
	mux.HandleFunc("/status", s.statusHandler)

	// Root endpoint
	mux.HandleFunc("/", s.rootHandler)

	s.server = &http.Server{
		Addr:         addr,
		Handler:      mux,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  30 * time.Second,
	}

	s.logger.Info("🏥 Health server starting on %s", addr)
	return s.server.ListenAndServe()
}

func (s *Server) Stop() error {
	if s.server != nil {
		s.logger.Info("🏥 Stopping health server...")
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		return s.server.Shutdown(ctx)
	}
	return nil
}

func (s *Server) healthHandler(w http.ResponseWriter, r *http.Request) {
	var memStats runtime.MemStats
	runtime.ReadMemStats(&memStats)

	healthData := map[string]interface{}{
		"status":      "healthy",
		"timestamp":   time.Now().Format(time.RFC3339),
		"uptime":      time.Since(startTime).String(),
		"version":     "2.0.0",
		"environment": "production",
		"memory": map[string]interface{}{
			"alloc_mb":       memStats.Alloc / 1024 / 1024,
			"total_alloc_mb": memStats.TotalAlloc / 1024 / 1024,
			"sys_mb":         memStats.Sys / 1024 / 1024,
			"heap_alloc_mb":  memStats.HeapAlloc / 1024 / 1024,
			"heap_sys_mb":    memStats.HeapSys / 1024 / 1024,
		},
		"runtime": map[string]interface{}{
			"goroutines": runtime.NumGoroutine(),
			"cpu_count":  runtime.NumCPU(),
			"go_version": runtime.Version(),
		},
		"system": map[string]interface{}{
			"os":   runtime.GOOS,
			"arch": runtime.GOARCH,
		},
	}

	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Cache-Control", "no-cache")
	w.WriteHeader(http.StatusOK)

	json.NewEncoder(w).Encode(healthData)
}

func (s *Server) metricsHandler(w http.ResponseWriter, r *http.Request) {
	var memStats runtime.MemStats
	runtime.ReadMemStats(&memStats)

	metrics := map[string]interface{}{
		"timestamp":      time.Now().Format(time.RFC3339),
		"uptime_seconds": time.Since(startTime).Seconds(),
		"memory": map[string]interface{}{
			"alloc_bytes":         memStats.Alloc,
			"total_alloc_bytes":   memStats.TotalAlloc,
			"sys_bytes":           memStats.Sys,
			"heap_alloc_bytes":    memStats.HeapAlloc,
			"heap_sys_bytes":      memStats.HeapSys,
			"heap_idle_bytes":     memStats.HeapIdle,
			"heap_inuse_bytes":    memStats.HeapInuse,
			"heap_released_bytes": memStats.HeapReleased,
			"heap_objects":        memStats.HeapObjects,
		},
		"gc": map[string]interface{}{
			"num_gc":         memStats.NumGC,
			"pause_ns":       memStats.PauseNs,
			"pause_total_ns": memStats.PauseTotalNs,
		},
		"runtime": map[string]interface{}{
			"goroutines": runtime.NumGoroutine(),
			"cpu_count":  runtime.NumCPU(),
		},
	}

	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Cache-Control", "no-cache")
	w.WriteHeader(http.StatusOK)

	json.NewEncoder(w).Encode(metrics)
}

func (s *Server) statusHandler(w http.ResponseWriter, r *http.Request) {
	status := map[string]interface{}{
		"status":     "running",
		"service":    "coderoot-bot",
		"version":    "2.0.0",
		"deployment": "liara",
		"timestamp":  time.Now().Format(time.RFC3339),
		"uptime":     time.Since(startTime).String(),
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	json.NewEncoder(w).Encode(status)
}

func (s *Server) rootHandler(w http.ResponseWriter, r *http.Request) {
	info := map[string]interface{}{
		"service":    "CodeRoot Bot",
		"version":    "2.0.0",
		"deployment": "Liara",
		"endpoints": map[string]string{
			"health":  "/health",
			"metrics": "/metrics",
			"status":  "/status",
		},
		"description": "Enterprise-grade Telegram bot for creating and managing online stores",
		"features": []string{
			"Multi-store Management",
			"Product Catalog",
			"Order Processing",
			"Payment Integration",
			"Admin Dashboard",
			"Real-time Monitoring",
			"Health Checks",
			"Performance Metrics",
		},
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	json.NewEncoder(w).Encode(info)
}

var startTime = time.Now()

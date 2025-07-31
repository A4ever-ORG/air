package monitoring

import (
	"context"
	"runtime"
	"time"

	"coderoot-bot/internal/logger"
)

type Monitor struct {
	logger    logger.Logger
	ctx       context.Context
	cancel    context.CancelFunc
	metrics   *Metrics
	interval  time.Duration
}

type Metrics struct {
	StartTime     time.Time
	Uptime        time.Duration
	MemoryUsage   MemoryStats
	CPUUsage      float64
	Goroutines    int
	Requests      int64
	Errors        int64
	LastUpdate    time.Time
}

type MemoryStats struct {
	Alloc      uint64
	TotalAlloc uint64
	Sys        uint64
	NumGC      uint32
	HeapAlloc  uint64
	HeapSys    uint64
}

func New(logger logger.Logger) *Monitor {
	ctx, cancel := context.WithCancel(context.Background())
	return &Monitor{
		logger:   logger,
		ctx:      ctx,
		cancel:   cancel,
		metrics:  &Metrics{StartTime: time.Now()},
		interval: 30 * time.Second, // Update every 30 seconds
	}
}

func (m *Monitor) Start() {
	m.logger.Info("📊 Starting monitoring system...")
	
	go m.collectMetrics()
	go m.reportMetrics()
}

func (m *Monitor) Stop() {
	m.logger.Info("📊 Stopping monitoring system...")
	m.cancel()
}

func (m *Monitor) collectMetrics() {
	ticker := time.NewTicker(m.interval)
	defer ticker.Stop()

	for {
		select {
		case <-m.ctx.Done():
			return
		case <-ticker.C:
			m.updateMetrics()
		}
	}
}

func (m *Monitor) updateMetrics() {
	var memStats runtime.MemStats
	runtime.ReadMemStats(&memStats)

	m.metrics.Uptime = time.Since(m.metrics.StartTime)
	m.metrics.MemoryUsage = MemoryStats{
		Alloc:      memStats.Alloc,
		TotalAlloc: memStats.TotalAlloc,
		Sys:        memStats.Sys,
		NumGC:      memStats.NumGC,
		HeapAlloc:  memStats.HeapAlloc,
		HeapSys:    memStats.HeapSys,
	}
	m.metrics.Goroutines = runtime.NumGoroutine()
	m.metrics.LastUpdate = time.Now()
}

func (m *Monitor) reportMetrics() {
	ticker := time.NewTicker(5 * time.Minute) // Report every 5 minutes
	defer ticker.Stop()

	for {
		select {
		case <-m.ctx.Done():
			return
		case <-ticker.C:
			m.logMetrics()
		}
	}
}

func (m *Monitor) logMetrics() {
	metrics := m.metrics
	
	m.logger.Info("📊 System Metrics Report:")
	m.logger.Info("⏱️  Uptime: %v", metrics.Uptime)
	m.logger.Info("💾 Memory Alloc: %d MB", metrics.MemoryUsage.Alloc/1024/1024)
	m.logger.Info("💾 Memory Total: %d MB", metrics.MemoryUsage.TotalAlloc/1024/1024)
	m.logger.Info("💾 Memory Sys: %d MB", metrics.MemoryUsage.Sys/1024/1024)
	m.logger.Info("🔄 Goroutines: %d", metrics.Goroutines)
	m.logger.Info("🗑️  GC Count: %d", metrics.MemoryUsage.NumGC)
	m.logger.Info("📈 Requests: %d", metrics.Requests)
	m.logger.Info("❌ Errors: %d", metrics.Errors)
}

func (m *Monitor) GetMetrics() *Metrics {
	return m.metrics
}

func (m *Monitor) IncrementRequests() {
	m.metrics.Requests++
}

func (m *Monitor) IncrementErrors() {
	m.metrics.Errors++
}

// Health check data
func (m *Monitor) GetHealthData() map[string]interface{} {
	metrics := m.metrics
	return map[string]interface{}{
		"status":     "healthy",
		"uptime":     metrics.Uptime.String(),
		"memory_mb":  metrics.MemoryUsage.Alloc / 1024 / 1024,
		"goroutines": metrics.Goroutines,
		"requests":   metrics.Requests,
		"errors":     metrics.Errors,
		"last_update": metrics.LastUpdate.Format(time.RFC3339),
	}
}
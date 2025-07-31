package logger

import (
	"os"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

// Logger wraps zap logger with convenience methods
type Logger struct {
	*zap.SugaredLogger
}

// New creates a new logger instance
func New() *Logger {
	// Create logs directory if it doesn't exist
	_ = os.MkdirAll("logs", 0755)

	// Configure encoder
	encoderConfig := zap.NewProductionEncoderConfig()
	encoderConfig.TimeKey = "timestamp"
	encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	encoderConfig.EncodeLevel = zapcore.CapitalColorLevelEncoder

	// Configure console output
	consoleEncoder := zapcore.NewConsoleEncoder(encoderConfig)
	consoleCore := zapcore.NewCore(
		consoleEncoder,
		zapcore.AddSync(os.Stdout),
		zapcore.InfoLevel,
	)

	// Configure file output
	fileEncoder := zapcore.NewJSONEncoder(encoderConfig)
	logFile, err := os.OpenFile("logs/coderoot.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err == nil {
		fileCore := zapcore.NewCore(
			fileEncoder,
			zapcore.AddSync(logFile),
			zapcore.InfoLevel,
		)
		
		// Combine console and file outputs
		core := zapcore.NewTee(consoleCore, fileCore)
		logger := zap.New(core, zap.AddCaller(), zap.AddStacktrace(zapcore.ErrorLevel))
		return &Logger{logger.Sugar()}
	}

	// Fallback to console only
	logger := zap.New(consoleCore, zap.AddCaller(), zap.AddStacktrace(zapcore.ErrorLevel))
	return &Logger{logger.Sugar()}
}

// Info logs an info message
func (l *Logger) Info(msg string, args ...interface{}) {
	l.SugaredLogger.Infof(msg, args...)
}

// Error logs an error message
func (l *Logger) Error(msg string, args ...interface{}) {
	l.SugaredLogger.Errorf(msg, args...)
}

// Warn logs a warning message
func (l *Logger) Warn(msg string, args ...interface{}) {
	l.SugaredLogger.Warnf(msg, args...)
}

// Debug logs a debug message
func (l *Logger) Debug(msg string, args ...interface{}) {
	l.SugaredLogger.Debugf(msg, args...)
}

// Fatal logs a fatal message and exits
func (l *Logger) Fatal(msg string, args ...interface{}) {
	l.SugaredLogger.Fatalf(msg, args...)
}

// With adds structured context to the logger
func (l *Logger) With(fields ...interface{}) *Logger {
	return &Logger{l.SugaredLogger.With(fields...)}
}

// WithUserID adds user ID to the logger context
func (l *Logger) WithUserID(userID int64) *Logger {
	return &Logger{l.SugaredLogger.With("user_id", userID)}
}

// WithShopID adds shop ID to the logger context
func (l *Logger) WithShopID(shopID string) *Logger {
	return &Logger{l.SugaredLogger.With("shop_id", shopID)}
}

// WithAction adds action to the logger context
func (l *Logger) WithAction(action string) *Logger {
	return &Logger{l.SugaredLogger.With("action", action)}
}
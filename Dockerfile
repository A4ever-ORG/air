# Multi-stage build for Render deployment with vendored dependencies
FROM golang:1.21-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    git \
    ca-certificates \
    tzdata \
    && update-ca-certificates

# Set working directory
WORKDIR /app

# Copy all source code (including vendor directory)
COPY . .

# Verify vendor directory exists
RUN ls -la vendor/ || (echo "ERROR: vendor/ directory not found. Run 'go mod vendor' first." && exit 1)

# Build the application using vendored dependencies
RUN CGO_ENABLED=0 GOOS=linux go build \
    -mod=vendor \
    -a -installsuffix cgo \
    -tags netgo \
    -ldflags="-w -s -extldflags '-static' -X main.version=2.0.0 -X main.commit=render-optimized" \
    -o app .

# Verify binary was created
RUN ls -la app && chmod +x app

# Final stage - Minimal runtime image
FROM alpine:latest

# Install runtime dependencies
RUN apk --no-cache add \
    ca-certificates \
    curl \
    tzdata \
    && rm -rf /var/cache/apk/*

# Create non-root user for security
RUN addgroup -g 1001 -S appuser && \
    adduser -S -D -H -u 1001 -h /app -s /sbin/nologin -G appuser -g appuser appuser

# Set working directory
WORKDIR /app

# Copy binary from builder stage
COPY --from=builder /app/app .

# Create necessary directories
RUN mkdir -p logs data tmp \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port for Render (Render will set PORT environment variable)
EXPOSE 8080

# Set environment variables for Render optimization
ENV ENVIRONMENT=production \
    GOMAXPROCS=0 \
    GOGC=50 \
    GOMEMLIMIT=512MiB \
    GODEBUG=http2server=1 \
    TZ=UTC \
    LANG=en_US.UTF-8

# Health check for Render
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

# Run the application
ENTRYPOINT ["./app"]
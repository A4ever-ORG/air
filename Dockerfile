# Multi-stage build for Kali Security Suite
FROM golang:1.21-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    git \
    ca-certificates \
    tzdata \
    && update-ca-certificates

# Set working directory
WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the application with optimizations
RUN CGO_ENABLED=0 GOOS=linux go build \
    -a -installsuffix cgo \
    -ldflags="-w -s -extldflags '-static'" \
    -o kali-security-suite .

# Security scanning stage
FROM alpine:latest AS security-scanner

# Install security tools
RUN apk add --no-cache \
    nmap \
    tcpdump \
    iptables \
    netcat-openbsd \
    curl \
    wget \
    && rm -rf /var/cache/apk/*

# Final stage
FROM debian:bullseye-slim

# Install runtime dependencies and security tools
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    wget \
    nmap \
    tcpdump \
    iptables \
    netcat \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r kali && useradd -r -g kali kali

# Set working directory
WORKDIR /app

# Copy binary from builder stage
COPY --from=builder /app/kali-security-suite .

# Copy security tools from scanner stage
COPY --from=security-scanner /usr/bin/nmap /usr/bin/
COPY --from=security-scanner /usr/bin/tcpdump /usr/bin/
COPY --from=security-scanner /usr/bin/iptables /usr/bin/
COPY --from=security-scanner /usr/bin/netcat /usr/bin/

# Create necessary directories
RUN mkdir -p /app/logs /app/reports /app/config \
    && chown -R kali:kali /app

# Switch to non-root user
USER kali

# Expose ports for monitoring
EXPOSE 8080 9090

# Set environment variables
ENV SECURITY_MODE=kali \
    SCAN_INTENSITY=high \
    GOGC=50 \
    GOMAXPROCS=4

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
ENTRYPOINT ["./kali-security-suite"]

# Default command
CMD ["monitor", "--daemon"]
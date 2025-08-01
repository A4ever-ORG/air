package database

import (
	"context"
	"strings"
	"time"

	"github.com/redis/go-redis/v9"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"coderoot-bot/internal/config"
	"coderoot-bot/internal/logger"
)

// Database manages database connections and repositories
type Database struct {
	MongoDB *mongo.Database
	RedisDB *redis.Client
	logger  *logger.Logger

	// Repositories
	Users     *UserRepository
	Shops     *ShopRepository
	Products  *ProductRepository
	Orders    *OrderRepository
	Payments  *PaymentRepository
	Analytics *AnalyticsRepository
	Settings  *SettingsRepository
}

// New creates a new database instance
func New(cfg *config.Config, logger *logger.Logger) (*Database, error) {
	db := &Database{
		logger: logger,
	}

	// Connect to MongoDB
	if err := db.connectMongoDB(cfg); err != nil {
		return nil, err
	}

	// Connect to Redis
	if err := db.connectRedis(cfg); err != nil {
		return nil, err
	}

	// Initialize repositories
	db.initRepositories()

	logger.Info("✅ Database connections established successfully")
	return db, nil
}

// connectMongoDB establishes MongoDB connection
func (d *Database) connectMongoDB(cfg *config.Config) error {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	d.logger.Info("🔌 Attempting to connect to MongoDB...")
	d.logger.Info("📍 MongoDB URI: %s", maskURI(cfg.MongoURI))

	clientOptions := options.Client().ApplyURI(cfg.MongoURI)

	// Configure connection pool for cloud databases
	clientOptions.SetMaxPoolSize(50)
	clientOptions.SetMinPoolSize(2)
	clientOptions.SetMaxConnIdleTime(60 * time.Second)
	clientOptions.SetServerSelectionTimeout(10 * time.Second)
	clientOptions.SetConnectTimeout(10 * time.Second)

	client, err := mongo.Connect(ctx, clientOptions)
	if err != nil {
		d.logger.Error("❌ Failed to connect to MongoDB: %v", err)
		d.logger.Error("💡 Make sure your MONGO_URI is correct and the database is accessible")
		return err
	}

	// Test the connection with retry
	for i := 0; i < 3; i++ {
		if err := client.Ping(ctx, nil); err != nil {
			d.logger.Error("❌ Failed to ping MongoDB (attempt %d/3): %v", i+1, err)
			if i == 2 {
				d.logger.Error("💡 Check if your MongoDB service is running and accessible")
				return err
			}
			time.Sleep(2 * time.Second)
		} else {
			break
		}
	}

	d.MongoDB = client.Database(cfg.DatabaseName)
	d.logger.Info("✅ Connected to MongoDB: %s", cfg.DatabaseName)

	return nil
}

// connectRedis establishes Redis connection
func (d *Database) connectRedis(cfg *config.Config) error {
	d.logger.Info("🔌 Attempting to connect to Redis...")
	d.logger.Info("📍 Redis URL: %s", maskURI(cfg.RedisURL))

	opts, err := redis.ParseURL(cfg.RedisURL)
	if err != nil {
		d.logger.Error("❌ Failed to parse Redis URL: %v", err)
		d.logger.Error("💡 Make sure your REDIS_URL is in the correct format")
		return err
	}

	// Configure Redis options for cloud databases
	opts.PoolSize = 20
	opts.MinIdleConns = 2
	opts.ConnMaxIdleTime = 60 * time.Second
	opts.DialTimeout = 10 * time.Second
	opts.ReadTimeout = 10 * time.Second
	opts.WriteTimeout = 10 * time.Second

	d.RedisDB = redis.NewClient(opts)

	// Test the connection with retry
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	for i := 0; i < 3; i++ {
		if err := d.RedisDB.Ping(ctx).Err(); err != nil {
			d.logger.Error("❌ Failed to connect to Redis (attempt %d/3): %v", i+1, err)
			if i == 2 {
				d.logger.Error("💡 Check if your Redis service is running and accessible")
				return err
			}
			time.Sleep(2 * time.Second)
		} else {
			break
		}
	}

	d.logger.Info("✅ Connected to Redis")
	return nil
}

// initRepositories initializes all repositories
func (d *Database) initRepositories() {
	d.Users = NewUserRepository(d.MongoDB, d.RedisDB, d.logger)
	d.Shops = NewShopRepository(d.MongoDB, d.RedisDB, d.logger)
	d.Products = NewProductRepository(d.MongoDB, d.RedisDB, d.logger)
	d.Orders = NewOrderRepository(d.MongoDB, d.RedisDB, d.logger)
	d.Payments = NewPaymentRepository(d.MongoDB, d.RedisDB, d.logger)
	d.Analytics = NewAnalyticsRepository(d.MongoDB, d.RedisDB, d.logger)
	d.Settings = NewSettingsRepository(d.MongoDB, d.RedisDB, d.logger)
}

// CreateIndexes creates necessary database indexes
func (d *Database) CreateIndexes(ctx context.Context) error {
	d.logger.Info("🔧 Creating database indexes...")

	// Create indexes for each collection
	if err := d.Users.CreateIndexes(ctx); err != nil {
		return err
	}

	if err := d.Shops.CreateIndexes(ctx); err != nil {
		return err
	}

	if err := d.Products.CreateIndexes(ctx); err != nil {
		return err
	}

	if err := d.Orders.CreateIndexes(ctx); err != nil {
		return err
	}

	if err := d.Payments.CreateIndexes(ctx); err != nil {
		return err
	}

	if err := d.Analytics.CreateIndexes(ctx); err != nil {
		return err
	}

	d.logger.Info("✅ Database indexes created successfully")
	return nil
}

// Health checks database connections
func (d *Database) Health(ctx context.Context) error {
	// Check MongoDB
	if err := d.MongoDB.Client().Ping(ctx, nil); err != nil {
		d.logger.Error("❌ MongoDB health check failed: %v", err)
		return err
	}

	// Check Redis
	if err := d.RedisDB.Ping(ctx).Err(); err != nil {
		d.logger.Error("❌ Redis health check failed: %v", err)
		return err
	}

	return nil
}

// Close closes all database connections
func (d *Database) Close(ctx context.Context) error {
	d.logger.Info("🔄 Closing database connections...")

	// Close MongoDB
	if d.MongoDB != nil {
		if err := d.MongoDB.Client().Disconnect(ctx); err != nil {
			d.logger.Error("❌ Error closing MongoDB: %v", err)
			return err
		}
	}

	// Close Redis
	if d.RedisDB != nil {
		if err := d.RedisDB.Close(); err != nil {
			d.logger.Error("❌ Error closing Redis: %v", err)
			return err
		}
	}

	d.logger.Info("✅ Database connections closed successfully")
	return nil
}

// maskURI masks sensitive information in connection strings for logging
func maskURI(uri string) string {
	if uri == "" {
		return "empty"
	}
	
	// For MongoDB URIs
	if strings.Contains(uri, "mongodb") {
		// Mask password in MongoDB URI
		if strings.Contains(uri, "@") {
			parts := strings.Split(uri, "@")
			if len(parts) == 2 {
				authPart := parts[0]
				hostPart := parts[1]
				
				// Mask password if present
				if strings.Contains(authPart, ":") {
					authParts := strings.Split(authPart, ":")
					if len(authParts) >= 3 {
						// Format: mongodb://username:password@host
						return authParts[0] + ":***@" + hostPart
					}
				}
			}
		}
		return uri
	}
	
	// For Redis URIs
	if strings.Contains(uri, "redis") {
		// Mask password in Redis URI
		if strings.Contains(uri, "@") {
			parts := strings.Split(uri, "@")
			if len(parts) == 2 {
				authPart := parts[0]
				hostPart := parts[1]
				
				// Mask password if present
				if strings.Contains(authPart, ":") {
					authParts := strings.Split(authPart, ":")
					if len(authParts) >= 3 {
						// Format: redis://username:password@host
						return authParts[0] + ":***@" + hostPart
					}
				}
			}
		}
		return uri
	}
	
	return "***"
}

package database

import (
	"context"
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
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	clientOptions := options.Client().ApplyURI(cfg.MongoURI)

	// Configure connection pool
	clientOptions.SetMaxPoolSize(100)
	clientOptions.SetMinPoolSize(5)
	clientOptions.SetMaxConnIdleTime(30 * time.Second)

	client, err := mongo.Connect(ctx, clientOptions)
	if err != nil {
		d.logger.Error("❌ Failed to connect to MongoDB: %v", err)
		return err
	}

	// Test the connection
	if err := client.Ping(ctx, nil); err != nil {
		d.logger.Error("❌ Failed to ping MongoDB: %v", err)
		return err
	}

	d.MongoDB = client.Database(cfg.DatabaseName)
	d.logger.Info("✅ Connected to MongoDB: %s", cfg.DatabaseName)

	return nil
}

// connectRedis establishes Redis connection
func (d *Database) connectRedis(cfg *config.Config) error {
	opts, err := redis.ParseURL(cfg.RedisURL)
	if err != nil {
		d.logger.Error("❌ Failed to parse Redis URL: %v", err)
		return err
	}

	// Configure Redis options
	opts.PoolSize = 10
	opts.MinIdleConns = 5
	opts.ConnMaxIdleTime = 30 * time.Second

	d.RedisDB = redis.NewClient(opts)

	// Test the connection
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := d.RedisDB.Ping(ctx).Err(); err != nil {
		d.logger.Error("❌ Failed to connect to Redis: %v", err)
		return err
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

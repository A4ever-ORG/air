package database

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"github.com/redis/go-redis/v9"
	"github.com/google/uuid"

	"coderoot-bot/internal/models"
	"coderoot-bot/internal/logger"
)

// UserRepository handles user data operations
type UserRepository struct {
	collection *mongo.Collection
	redis      *redis.Client
	logger     *logger.Logger
}

// NewUserRepository creates a new user repository
func NewUserRepository(db *mongo.Database, redis *redis.Client, logger *logger.Logger) *UserRepository {
	return &UserRepository{
		collection: db.Collection("users"),
		redis:      redis,
		logger:     logger,
	}
}

// CreateIndexes creates indexes for the users collection
func (r *UserRepository) CreateIndexes(ctx context.Context) error {
	indexes := []mongo.IndexModel{
		{
			Keys: bson.D{{Key: "user_id", Value: 1}},
			Options: options.Index().SetUnique(true),
		},
		{
			Keys: bson.D{{Key: "username", Value: 1}},
			Options: options.Index().SetSparse(true),
		},
		{
			Keys: bson.D{{Key: "referral_code", Value: 1}},
			Options: options.Index().SetUnique(true).SetSparse(true),
		},
		{
			Keys: bson.D{{Key: "created_at", Value: -1}},
		},
		{
			Keys: bson.D{{Key: "last_activity", Value: -1}},
		},
	}

	_, err := r.collection.Indexes().CreateMany(ctx, indexes)
	if err != nil {
		r.logger.Error("Failed to create user indexes: %v", err)
		return err
	}

	return nil
}

// Create creates a new user
func (r *UserRepository) Create(ctx context.Context, user *models.User) error {
	now := time.Now()
	user.CreatedAt = now
	user.UpdatedAt = now
	user.LastActivity = now
	user.IsActive = true

	// Generate referral code if not provided
	if user.ReferralCode == "" {
		user.ReferralCode = generateReferralCode()
	}

	result, err := r.collection.InsertOne(ctx, user)
	if err != nil {
		r.logger.Error("Failed to create user: %v", err)
		return err
	}

	user.ID = result.InsertedID.(primitive.ObjectID)

	// Cache the user
	if err := r.cacheUser(ctx, user); err != nil {
		r.logger.Warn("Failed to cache user: %v", err)
	}

	r.logger.WithUserID(user.UserID).Info("User created successfully")
	return nil
}

// GetByUserID retrieves a user by Telegram user ID
func (r *UserRepository) GetByUserID(ctx context.Context, userID int64) (*models.User, error) {
	// Try cache first
	if user, err := r.getCachedUser(ctx, userID); err == nil {
		return user, nil
	}

	var user models.User
	err := r.collection.FindOne(ctx, bson.M{"user_id": userID}).Decode(&user)
	if err != nil {
		if err == mongo.ErrNoDocuments {
			return nil, nil // User not found
		}
		r.logger.Error("Failed to get user by ID: %v", err)
		return nil, err
	}

	// Cache the user
	if err := r.cacheUser(ctx, &user); err != nil {
		r.logger.Warn("Failed to cache user: %v", err)
	}

	return &user, nil
}

// GetByReferralCode retrieves a user by referral code
func (r *UserRepository) GetByReferralCode(ctx context.Context, referralCode string) (*models.User, error) {
	var user models.User
	err := r.collection.FindOne(ctx, bson.M{"referral_code": referralCode}).Decode(&user)
	if err != nil {
		if err == mongo.ErrNoDocuments {
			return nil, nil // User not found
		}
		r.logger.Error("Failed to get user by referral code: %v", err)
		return nil, err
	}

	return &user, nil
}

// Update updates user information
func (r *UserRepository) Update(ctx context.Context, userID int64, update bson.M) error {
	update["updated_at"] = time.Now()

	_, err := r.collection.UpdateOne(
		ctx,
		bson.M{"user_id": userID},
		bson.M{"$set": update},
	)
	if err != nil {
		r.logger.Error("Failed to update user: %v", err)
		return err
	}

	// Invalidate cache
	if err := r.invalidateUserCache(ctx, userID); err != nil {
		r.logger.Warn("Failed to invalidate user cache: %v", err)
	}

	r.logger.WithUserID(userID).Info("User updated successfully")
	return nil
}

// UpdateLastActivity updates user's last activity timestamp
func (r *UserRepository) UpdateLastActivity(ctx context.Context, userID int64) error {
	_, err := r.collection.UpdateOne(
		ctx,
		bson.M{"user_id": userID},
		bson.M{"$set": bson.M{"last_activity": time.Now()}},
	)
	if err != nil {
		r.logger.Error("Failed to update user last activity: %v", err)
		return err
	}

	return nil
}

// GetActiveUsers returns a list of active users with pagination
func (r *UserRepository) GetActiveUsers(ctx context.Context, page, limit int) ([]*models.User, int64, error) {
	skip := (page - 1) * limit

	// Get total count
	total, err := r.collection.CountDocuments(ctx, bson.M{"is_active": true})
	if err != nil {
		r.logger.Error("Failed to count active users: %v", err)
		return nil, 0, err
	}

	// Get users
	opts := options.Find().
		SetSort(bson.D{{Key: "last_activity", Value: -1}}).
		SetSkip(int64(skip)).
		SetLimit(int64(limit))

	cursor, err := r.collection.Find(ctx, bson.M{"is_active": true}, opts)
	if err != nil {
		r.logger.Error("Failed to find active users: %v", err)
		return nil, 0, err
	}
	defer cursor.Close(ctx)

	var users []*models.User
	if err := cursor.All(ctx, &users); err != nil {
		r.logger.Error("Failed to decode active users: %v", err)
		return nil, 0, err
	}

	return users, total, nil
}

// GetUserStats returns user statistics
func (r *UserRepository) GetUserStats(ctx context.Context) (map[string]int64, error) {
	pipeline := mongo.Pipeline{
		{{Key: "$group", Value: bson.D{
			{Key: "_id", Value: nil},
			{Key: "total", Value: bson.D{{Key: "$sum", Value: 1}}},
			{Key: "active", Value: bson.D{{Key: "$sum", Value: bson.D{{Key: "$cond", Value: []interface{}{"$is_active", 1, 0}}}}}},
			{Key: "premium", Value: bson.D{{Key: "$sum", Value: bson.D{{Key: "$cond", Value: []interface{}{"$is_premium", 1, 0}}}}}},
		}}},
	}

	cursor, err := r.collection.Aggregate(ctx, pipeline)
	if err != nil {
		r.logger.Error("Failed to get user stats: %v", err)
		return nil, err
	}
	defer cursor.Close(ctx)

	var result []bson.M
	if err := cursor.All(ctx, &result); err != nil {
		r.logger.Error("Failed to decode user stats: %v", err)
		return nil, err
	}

	stats := make(map[string]int64)
	if len(result) > 0 {
		data := result[0]
		stats["total"] = getInt64FromBSON(data, "total")
		stats["active"] = getInt64FromBSON(data, "active")
		stats["premium"] = getInt64FromBSON(data, "premium")
	}

	return stats, nil
}

// Delete soft deletes a user
func (r *UserRepository) Delete(ctx context.Context, userID int64) error {
	_, err := r.collection.UpdateOne(
		ctx,
		bson.M{"user_id": userID},
		bson.M{"$set": bson.M{
			"is_active":  false,
			"updated_at": time.Now(),
		}},
	)
	if err != nil {
		r.logger.Error("Failed to delete user: %v", err)
		return err
	}

	// Invalidate cache
	if err := r.invalidateUserCache(ctx, userID); err != nil {
		r.logger.Warn("Failed to invalidate user cache: %v", err)
	}

	r.logger.WithUserID(userID).Info("User deleted successfully")
	return nil
}

// Cache operations

func (r *UserRepository) cacheUser(ctx context.Context, user *models.User) error {
	data, err := json.Marshal(user)
	if err != nil {
		return err
	}

	key := fmt.Sprintf("user:%d", user.UserID)
	return r.redis.Set(ctx, key, data, 1*time.Hour).Err()
}

func (r *UserRepository) getCachedUser(ctx context.Context, userID int64) (*models.User, error) {
	key := fmt.Sprintf("user:%d", userID)
	data, err := r.redis.Get(ctx, key).Result()
	if err != nil {
		return nil, err
	}

	var user models.User
	if err := json.Unmarshal([]byte(data), &user); err != nil {
		return nil, err
	}

	return &user, nil
}

func (r *UserRepository) invalidateUserCache(ctx context.Context, userID int64) error {
	key := fmt.Sprintf("user:%d", userID)
	return r.redis.Del(ctx, key).Err()
}

// Helper functions

func generateReferralCode() string {
	return uuid.New().String()[:8]
}

func getInt64FromBSON(data bson.M, key string) int64 {
	if val, ok := data[key]; ok {
		switch v := val.(type) {
		case int:
			return int64(v)
		case int32:
			return int64(v)
		case int64:
			return v
		}
	}
	return 0
}
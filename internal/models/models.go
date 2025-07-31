package models

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

// User represents a bot user
type User struct {
	ID           primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	UserID       int64              `bson:"user_id" json:"user_id"`
	Username     string             `bson:"username" json:"username"`
	FirstName    string             `bson:"first_name" json:"first_name"`
	LastName     string             `bson:"last_name" json:"last_name"`
	Language     string             `bson:"language" json:"language"`
	IsActive     bool               `bson:"is_active" json:"is_active"`
	IsPremium    bool               `bson:"is_premium" json:"is_premium"`
	ReferredBy   int64              `bson:"referred_by,omitempty" json:"referred_by,omitempty"`
	ReferralCode string             `bson:"referral_code" json:"referral_code"`
	CreatedAt    time.Time          `bson:"created_at" json:"created_at"`
	UpdatedAt    time.Time          `bson:"updated_at" json:"updated_at"`
	LastActivity time.Time          `bson:"last_activity" json:"last_activity"`
}

// Shop represents a user's shop
type Shop struct {
	ID          primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	OwnerID     int64              `bson:"owner_id" json:"owner_id"`
	Name        string             `bson:"name" json:"name"`
	Description string             `bson:"description" json:"description"`
	IsActive    bool               `bson:"is_active" json:"is_active"`
	BotToken    string             `bson:"bot_token,omitempty" json:"bot_token,omitempty"`
	BotUsername string             `bson:"bot_username,omitempty" json:"bot_username,omitempty"`
	Category    string             `bson:"category" json:"category"`
	Settings    ShopSettings       `bson:"settings" json:"settings"`
	Stats       ShopStats          `bson:"stats" json:"stats"`
	CreatedAt   time.Time          `bson:"created_at" json:"created_at"`
	UpdatedAt   time.Time          `bson:"updated_at" json:"updated_at"`
}

// ShopSettings represents shop configuration
type ShopSettings struct {
	Currency           string `bson:"currency" json:"currency"`
	PaymentMethod      string `bson:"payment_method" json:"payment_method"`
	AutoReply          bool   `bson:"auto_reply" json:"auto_reply"`
	NotifyNewOrders    bool   `bson:"notify_new_orders" json:"notify_new_orders"`
	RequireJoinChannel bool   `bson:"require_join_channel" json:"require_join_channel"`
}

// ShopStats represents shop statistics
type ShopStats struct {
	TotalProducts int `bson:"total_products" json:"total_products"`
	TotalOrders   int `bson:"total_orders" json:"total_orders"`
	TotalRevenue  int `bson:"total_revenue" json:"total_revenue"`
	TotalUsers    int `bson:"total_users" json:"total_users"`
}

// Product represents a shop product
type Product struct {
	ID          primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	ShopID      primitive.ObjectID `bson:"shop_id" json:"shop_id"`
	Name        string             `bson:"name" json:"name"`
	Description string             `bson:"description" json:"description"`
	Price       int                `bson:"price" json:"price"`
	Currency    string             `bson:"currency" json:"currency"`
	Category    string             `bson:"category" json:"category"`
	Images      []string           `bson:"images" json:"images"`
	IsActive    bool               `bson:"is_active" json:"is_active"`
	Stock       int                `bson:"stock" json:"stock"`
	IsDigital   bool               `bson:"is_digital" json:"is_digital"`
	FileURL     string             `bson:"file_url,omitempty" json:"file_url,omitempty"`
	CreatedAt   time.Time          `bson:"created_at" json:"created_at"`
	UpdatedAt   time.Time          `bson:"updated_at" json:"updated_at"`
}

// Order represents a customer order
type Order struct {
	ID            primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	OrderNumber   string             `bson:"order_number" json:"order_number"`
	ShopID        primitive.ObjectID `bson:"shop_id" json:"shop_id"`
	UserID        int64              `bson:"user_id" json:"user_id"`
	ProductID     primitive.ObjectID `bson:"product_id" json:"product_id"`
	Quantity      int                `bson:"quantity" json:"quantity"`
	TotalAmount   int                `bson:"total_amount" json:"total_amount"`
	Currency      string             `bson:"currency" json:"currency"`
	Status        OrderStatus        `bson:"status" json:"status"`
	PaymentMethod string             `bson:"payment_method" json:"payment_method"`
	PaymentStatus PaymentStatus      `bson:"payment_status" json:"payment_status"`
	ShippingInfo  ShippingInfo       `bson:"shipping_info,omitempty" json:"shipping_info,omitempty"`
	Notes         string             `bson:"notes,omitempty" json:"notes,omitempty"`
	CreatedAt     time.Time          `bson:"created_at" json:"created_at"`
	UpdatedAt     time.Time          `bson:"updated_at" json:"updated_at"`
}

// OrderStatus represents order status
type OrderStatus string

const (
	OrderStatusPending    OrderStatus = "pending"
	OrderStatusConfirmed  OrderStatus = "confirmed"
	OrderStatusProcessing OrderStatus = "processing"
	OrderStatusShipped    OrderStatus = "shipped"
	OrderStatusDelivered  OrderStatus = "delivered"
	OrderStatusCancelled  OrderStatus = "cancelled"
)

// PaymentStatus represents payment status
type PaymentStatus string

const (
	PaymentStatusPending   PaymentStatus = "pending"
	PaymentStatusPaid      PaymentStatus = "paid"
	PaymentStatusFailed    PaymentStatus = "failed"
	PaymentStatusRefunded  PaymentStatus = "refunded"
	PaymentStatusCancelled PaymentStatus = "cancelled"
)

// ShippingInfo represents shipping information
type ShippingInfo struct {
	Name         string `bson:"name" json:"name"`
	Phone        string `bson:"phone" json:"phone"`
	Address      string `bson:"address" json:"address"`
	City         string `bson:"city" json:"city"`
	Province     string `bson:"province" json:"province"`
	PostalCode   string `bson:"postal_code" json:"postal_code"`
	TrackingCode string `bson:"tracking_code,omitempty" json:"tracking_code,omitempty"`
}

// Payment represents a payment transaction
type Payment struct {
	ID            primitive.ObjectID     `bson:"_id,omitempty" json:"id"`
	OrderID       primitive.ObjectID     `bson:"order_id" json:"order_id"`
	UserID        int64                  `bson:"user_id" json:"user_id"`
	Amount        int                    `bson:"amount" json:"amount"`
	Currency      string                 `bson:"currency" json:"currency"`
	Method        string                 `bson:"method" json:"method"`
	Status        PaymentStatus          `bson:"status" json:"status"`
	TransactionID string                 `bson:"transaction_id,omitempty" json:"transaction_id,omitempty"`
	GatewayData   map[string]interface{} `bson:"gateway_data,omitempty" json:"gateway_data,omitempty"`
	CreatedAt     time.Time              `bson:"created_at" json:"created_at"`
	UpdatedAt     time.Time              `bson:"updated_at" json:"updated_at"`
}

// UserSession represents user session data
type UserSession struct {
	UserID    int64                  `json:"user_id"`
	State     string                 `json:"state"`
	Data      map[string]interface{} `json:"data"`
	ExpiresAt time.Time              `json:"expires_at"`
}

// Analytics represents analytics data
type Analytics struct {
	ID           primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	Date         time.Time          `bson:"date" json:"date"`
	TotalUsers   int                `bson:"total_users" json:"total_users"`
	NewUsers     int                `bson:"new_users" json:"new_users"`
	ActiveUsers  int                `bson:"active_users" json:"active_users"`
	TotalShops   int                `bson:"total_shops" json:"total_shops"`
	NewShops     int                `bson:"new_shops" json:"new_shops"`
	TotalOrders  int                `bson:"total_orders" json:"total_orders"`
	TotalRevenue int                `bson:"total_revenue" json:"total_revenue"`
	MessagesSent int                `bson:"messages_sent" json:"messages_sent"`
	CommandsUsed map[string]int     `bson:"commands_used" json:"commands_used"`
	ErrorsCount  int                `bson:"errors_count" json:"errors_count"`
}

// BotSettings represents bot configuration
type BotSettings struct {
	ID                 primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	MaintenanceMode    bool               `bson:"maintenance_mode" json:"maintenance_mode"`
	MaintenanceMessage string             `bson:"maintenance_message" json:"maintenance_message"`
	WelcomeMessage     map[string]string  `bson:"welcome_message" json:"welcome_message"`
	MaxShopsPerUser    int                `bson:"max_shops_per_user" json:"max_shops_per_user"`
	RequireChannelJoin bool               `bson:"require_channel_join" json:"require_channel_join"`
	AutoBackup         bool               `bson:"auto_backup" json:"auto_backup"`
	BackupInterval     int                `bson:"backup_interval" json:"backup_interval"`
	RateLimitPerMinute int                `bson:"rate_limit_per_minute" json:"rate_limit_per_minute"`
	EnabledFeatures    []string           `bson:"enabled_features" json:"enabled_features"`
	UpdatedAt          time.Time          `bson:"updated_at" json:"updated_at"`
}

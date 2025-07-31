package services

import (
	"coderoot-bot/internal/config"
	"coderoot-bot/internal/database"
	"coderoot-bot/internal/logger"
)

// Services contains all business logic services
type Services struct {
	User    *UserService
	Shop    *ShopService
	Payment *PaymentService
	Auth    *AuthService
}

// New creates a new services instance
func New(cfg *config.Config, logger *logger.Logger, db *database.Database) (*Services, error) {
	return &Services{
		User:    NewUserService(cfg, logger, db),
		Shop:    NewShopService(cfg, logger, db),
		Payment: NewPaymentService(cfg, logger, db),
		Auth:    NewAuthService(cfg, logger, db),
	}, nil
}

// UserService handles user-related business logic
type UserService struct {
	config *config.Config
	logger *logger.Logger
	db     *database.Database
}

// NewUserService creates a new user service
func NewUserService(cfg *config.Config, logger *logger.Logger, db *database.Database) *UserService {
	return &UserService{
		config: cfg,
		logger: logger,
		db:     db,
	}
}

// ShopService handles shop-related business logic
type ShopService struct {
	config *config.Config
	logger *logger.Logger
	db     *database.Database
}

// NewShopService creates a new shop service
func NewShopService(cfg *config.Config, logger *logger.Logger, db *database.Database) *ShopService {
	return &ShopService{
		config: cfg,
		logger: logger,
		db:     db,
	}
}

// PaymentService handles payment-related business logic
type PaymentService struct {
	config *config.Config
	logger *logger.Logger
	db     *database.Database
}

// NewPaymentService creates a new payment service
func NewPaymentService(cfg *config.Config, logger *logger.Logger, db *database.Database) *PaymentService {
	return &PaymentService{
		config: cfg,
		logger: logger,
		db:     db,
	}
}

// AuthService handles authentication and authorization
type AuthService struct {
	config *config.Config
	logger *logger.Logger
	db     *database.Database
}

// NewAuthService creates a new auth service
func NewAuthService(cfg *config.Config, logger *logger.Logger, db *database.Database) *AuthService {
	return &AuthService{
		config: cfg,
		logger: logger,
		db:     db,
	}
}

// IsAdmin checks if user is admin
func (s *AuthService) IsAdmin(userID int64) bool {
	return userID == s.config.AdminUserID
}

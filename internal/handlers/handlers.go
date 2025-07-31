package handlers

import (
	"context"
	"fmt"
	"strings"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"

	"coderoot-bot/internal/config"
	"coderoot-bot/internal/database"
	"coderoot-bot/internal/logger"
	"coderoot-bot/internal/models"
	"coderoot-bot/internal/services"
	"coderoot-bot/internal/utils"
)

// Handler handles Telegram updates
type Handler struct {
	config   *config.Config
	logger   *logger.Logger
	db       *database.Database
	services *services.Services
	utils    *utils.Utils
}

// New creates a new handler instance
func New(cfg *config.Config, logger *logger.Logger, db *database.Database, services *services.Services, utils *utils.Utils) *Handler {
	return &Handler{
		config:   cfg,
		logger:   logger,
		db:       db,
		services: services,
		utils:    utils,
	}
}

// HandleMessage handles incoming text messages
func (h *Handler) HandleMessage(ctx context.Context, bot *tgbotapi.BotAPI, message *tgbotapi.Message) {
	userID := message.From.ID
	h.logger.WithUserID(userID).Info("Received message: %s", message.Text)

	// Update user activity
	if err := h.updateUserActivity(ctx, message.From); err != nil {
		h.logger.Error("Failed to update user activity: %v", err)
	}

	// Handle commands
	if message.IsCommand() {
		h.handleCommand(ctx, bot, message)
		return
	}

	// Handle text messages based on user state
	h.handleTextMessage(ctx, bot, message)
}

// HandleCallbackQuery handles inline keyboard callbacks
func (h *Handler) HandleCallbackQuery(ctx context.Context, bot *tgbotapi.BotAPI, query *tgbotapi.CallbackQuery) {
	userID := query.From.ID
	h.logger.WithUserID(userID).Info("Received callback: %s", query.Data)

	// Answer callback query to remove loading state
	callback := tgbotapi.NewCallback(query.ID, "")
	if _, err := bot.Request(callback); err != nil {
		h.logger.Error("Failed to answer callback query: %v", err)
	}

	// Update user activity
	if err := h.updateUserActivity(ctx, query.From); err != nil {
		h.logger.Error("Failed to update user activity: %v", err)
	}

	// Route callback based on data
	parts := strings.Split(query.Data, ":")
	action := parts[0]

	switch action {
	case "language":
		h.handleLanguageSelection(ctx, bot, query)
	case "shop":
		h.handleShopAction(ctx, bot, query)
	case "admin":
		h.handleAdminAction(ctx, bot, query)
	case "start":
		h.handleMainMenu(ctx, bot, query.Message.Chat.ID, userID)
	default:
		h.logger.Warn("Unknown callback action: %s", action)
	}
}

// HandleInlineQuery handles inline queries
func (h *Handler) HandleInlineQuery(ctx context.Context, bot *tgbotapi.BotAPI, query *tgbotapi.InlineQuery) {
	userID := query.From.ID
	h.logger.WithUserID(userID).Info("Received inline query: %s", query.Query)

	// Create empty result for now
	result := tgbotapi.InlineConfig{
		InlineQueryID: query.ID,
		Results:       []interface{}{},
	}

	if _, err := bot.Request(result); err != nil {
		h.logger.Error("Failed to answer inline query: %v", err)
	}
}

// handleCommand handles bot commands
func (h *Handler) handleCommand(ctx context.Context, bot *tgbotapi.BotAPI, message *tgbotapi.Message) {
	command := message.Command()
	userID := message.From.ID

	switch command {
	case "start":
		h.handleStart(ctx, bot, message)
	case "help":
		h.handleHelp(ctx, bot, message)
	case "admin":
		if userID == h.config.AdminUserID {
			h.handleAdminPanel(ctx, bot, message)
		} else {
			h.sendMessage(bot, message.Chat.ID, "❌ شما دسترسی ادمین ندارید")
		}
	case "stats":
		if userID == h.config.AdminUserID {
			h.handleStats(ctx, bot, message)
		}
	case "shops":
		h.handleMyShops(ctx, bot, message)
	default:
		h.handleUnknownCommand(ctx, bot, message)
	}
}

// handleStart handles /start command
func (h *Handler) handleStart(ctx context.Context, bot *tgbotapi.BotAPI, message *tgbotapi.Message) {
	userID := message.From.ID

	// Get or create user
	user, err := h.db.Users.GetByUserID(ctx, userID)
	if err != nil {
		h.logger.Error("Failed to get user: %v", err)
		h.sendMessage(bot, message.Chat.ID, "❌ خطا در دریافت اطلاعات کاربر")
		return
	}

	if user == nil {
		// Create new user
		user = &models.User{
			UserID:    userID,
			Username:  message.From.UserName,
			FirstName: message.From.FirstName,
			LastName:  message.From.LastName,
			Language:  h.config.DefaultLanguage,
		}

		// Handle referral
		args := strings.Fields(message.Text)
		if len(args) > 1 && strings.HasPrefix(args[1], "ref_") {
			referralCode := strings.TrimPrefix(args[1], "ref_")
			referrer, err := h.db.Users.GetByReferralCode(ctx, referralCode)
			if err == nil && referrer != nil {
				user.ReferredBy = referrer.UserID
			}
		}

		if err := h.db.Users.Create(ctx, user); err != nil {
			h.logger.Error("Failed to create user: %v", err)
			h.sendMessage(bot, message.Chat.ID, "❌ خطا در ایجاد کاربر")
			return
		}
	}

	// Show main menu
	h.handleMainMenu(ctx, bot, message.Chat.ID, userID)
}

// handleMainMenu shows the main menu
func (h *Handler) handleMainMenu(ctx context.Context, bot *tgbotapi.BotAPI, chatID int64, userID int64) {
	text := h.utils.GetText("main_menu", h.config.DefaultLanguage)
	keyboard := h.utils.GetMainMenuKeyboard(h.config.DefaultLanguage)

	msg := tgbotapi.NewMessage(chatID, text)
	msg.ReplyMarkup = keyboard

	if _, err := bot.Send(msg); err != nil {
		h.logger.Error("Failed to send main menu: %v", err)
	}
}

// handleHelp handles /help command
func (h *Handler) handleHelp(ctx context.Context, bot *tgbotapi.BotAPI, message *tgbotapi.Message) {
	helpText := `🤖 راهنمای ربات CodeRoot

📋 دستورات اصلی:
/start - شروع مجدد ربات
/help - نمایش این راهنما
/shops - مدیریت فروشگاه‌های من
/admin - پنل ادمین (فقط ادمین)

💡 ویژگی‌ها:
• ایجاد و مدیریت فروشگاه
• پشتیبانی چند زبانه
• سیستم پرداخت
• پنل ادمین کامل

🆘 پشتیبانی: @` + h.config.AdminUsername

	h.sendMessage(bot, message.Chat.ID, helpText)
}

// handleTextMessage handles regular text messages
func (h *Handler) handleTextMessage(ctx context.Context, bot *tgbotapi.BotAPI, message *tgbotapi.Message) {
	// For now, just echo back or show help
	response := "لطفاً از منوی اصلی استفاده کنید یا دستور /help را بزنید"
	h.sendMessage(bot, message.Chat.ID, response)
}

// handleLanguageSelection handles language selection callback
func (h *Handler) handleLanguageSelection(ctx context.Context, bot *tgbotapi.BotAPI, query *tgbotapi.CallbackQuery) {
	parts := strings.Split(query.Data, ":")
	if len(parts) < 2 {
		return
	}

	language := parts[1]
	userID := query.From.ID

	// Update user language
	err := h.db.Users.Update(ctx, userID, map[string]interface{}{
		"language": language,
	})
	if err != nil {
		h.logger.Error("Failed to update user language: %v", err)
		return
	}

	// Show main menu in selected language
	h.handleMainMenu(ctx, bot, query.Message.Chat.ID, userID)
}

// handleShopAction handles shop-related callbacks
func (h *Handler) handleShopAction(ctx context.Context, bot *tgbotapi.BotAPI, query *tgbotapi.CallbackQuery) {
	// Implement shop actions
	h.sendMessage(bot, query.Message.Chat.ID, "🏪 بخش فروشگاه در حال توسعه...")
}

// handleAdminAction handles admin-related callbacks
func (h *Handler) handleAdminAction(ctx context.Context, bot *tgbotapi.BotAPI, query *tgbotapi.CallbackQuery) {
	userID := query.From.ID
	if userID != h.config.AdminUserID {
		return
	}

	// Implement admin actions
	h.sendMessage(bot, query.Message.Chat.ID, "⚙️ پنل ادمین در حال توسعه...")
}

// handleAdminPanel shows admin panel
func (h *Handler) handleAdminPanel(ctx context.Context, bot *tgbotapi.BotAPI, message *tgbotapi.Message) {
	text := "⚙️ پنل مدیریت\n\nگزینه مورد نظر را انتخاب کنید:"
	keyboard := h.utils.GetAdminKeyboard(h.config.DefaultLanguage)

	msg := tgbotapi.NewMessage(message.Chat.ID, text)
	msg.ReplyMarkup = keyboard

	if _, err := bot.Send(msg); err != nil {
		h.logger.Error("Failed to send admin panel: %v", err)
	}
}

// handleStats shows bot statistics
func (h *Handler) handleStats(ctx context.Context, bot *tgbotapi.BotAPI, message *tgbotapi.Message) {
	stats, err := h.db.Users.GetUserStats(ctx)
	if err != nil {
		h.logger.Error("Failed to get stats: %v", err)
		h.sendMessage(bot, message.Chat.ID, "❌ خطا در دریافت آمار")
		return
	}

	text := "📊 آمار ربات:\n\n"
	text += "👥 کل کاربران: %d\n"
	text += "✅ کاربران فعال: %d\n"
	text += "⭐ کاربران پریمیوم: %d"

	responseText := fmt.Sprintf(text, stats["total"], stats["active"], stats["premium"])
	h.sendMessage(bot, message.Chat.ID, responseText)
}

// handleMyShops shows user's shops
func (h *Handler) handleMyShops(ctx context.Context, bot *tgbotapi.BotAPI, message *tgbotapi.Message) {
	text := "🏪 فروشگاه‌های من\n\nشما هنوز فروشگاهی ندارید.\nبرای ایجاد فروشگاه جدید دکمه زیر را بزنید."
	keyboard := h.utils.GetShopsKeyboard(h.config.DefaultLanguage)

	msg := tgbotapi.NewMessage(message.Chat.ID, text)
	msg.ReplyMarkup = keyboard

	if _, err := bot.Send(msg); err != nil {
		h.logger.Error("Failed to send shops menu: %v", err)
	}
}

// handleUnknownCommand handles unknown commands
func (h *Handler) handleUnknownCommand(ctx context.Context, bot *tgbotapi.BotAPI, message *tgbotapi.Message) {
	text := "❓ دستور ناشناخته\n\nلطفاً از دستورات موجود استفاده کنید یا /help را بزنید."
	h.sendMessage(bot, message.Chat.ID, text)
}

// Helper methods

// updateUserActivity updates user's last activity
func (h *Handler) updateUserActivity(ctx context.Context, user *tgbotapi.User) error {
	return h.db.Users.UpdateLastActivity(ctx, user.ID)
}

// sendMessage sends a message to chat
func (h *Handler) sendMessage(bot *tgbotapi.BotAPI, chatID int64, text string) {
	msg := tgbotapi.NewMessage(chatID, text)
	if _, err := bot.Send(msg); err != nil {
		h.logger.Error("Failed to send message: %v", err)
	}
}

package utils

import (
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"

	"coderoot-bot/internal/config"
	"coderoot-bot/internal/logger"
)

// Utils contains utility functions
type Utils struct {
	config *config.Config
	logger *logger.Logger
	texts  map[string]map[string]string
}

// New creates a new utils instance
func New(cfg *config.Config, logger *logger.Logger) *Utils {
	utils := &Utils{
		config: cfg,
		logger: logger,
		texts:  make(map[string]map[string]string),
	}

	utils.loadTexts()
	return utils
}

// loadTexts loads all text messages
func (u *Utils) loadTexts() {
	u.texts = map[string]map[string]string{
		"main_menu": {
			"fa": "🏠 منوی اصلی\n\nخوش آمدید! گزینه مورد نظر را انتخاب کنید:",
			"en": "🏠 Main Menu\n\nWelcome! Please select an option:",
			"ar": "🏠 القائمة الرئيسية\n\nمرحباً! يرجى اختيار خيار:",
		},
		"welcome": {
			"fa": "🎉 به ربات CodeRoot خوش آمدید!\n\nاین ربات برای ایجاد و مدیریت فروشگاه‌های آنلاین طراحی شده است.",
			"en": "🎉 Welcome to CodeRoot Bot!\n\nThis bot is designed for creating and managing online stores.",
			"ar": "🎉 مرحباً بك في بوت CodeRoot!\n\nتم تصميم هذا البوت لإنشاء وإدارة المتاجر الإلكترونية.",
		},
	}
}

// GetText returns text in specified language
func (u *Utils) GetText(key, language string) string {
	if texts, exists := u.texts[key]; exists {
		if text, exists := texts[language]; exists {
			return text
		}
		// Fallback to default language
		if text, exists := texts[u.config.DefaultLanguage]; exists {
			return text
		}
	}
	return key // Return key if text not found
}

// GetMainMenuKeyboard returns main menu keyboard
func (u *Utils) GetMainMenuKeyboard(language string) tgbotapi.InlineKeyboardMarkup {
	var buttons [][]tgbotapi.InlineKeyboardButton

	switch language {
	case "en":
		buttons = [][]tgbotapi.InlineKeyboardButton{
			{
				tgbotapi.NewInlineKeyboardButtonData("🏪 My Shops", "shop:list"),
				tgbotapi.NewInlineKeyboardButtonData("➕ Create Shop", "shop:create"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("📊 Statistics", "stats:user"),
				tgbotapi.NewInlineKeyboardButtonData("⚙️ Settings", "settings:main"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("🆘 Support", "support:main"),
				tgbotapi.NewInlineKeyboardButtonData("ℹ️ Help", "help:main"),
			},
		}
	case "ar":
		buttons = [][]tgbotapi.InlineKeyboardButton{
			{
				tgbotapi.NewInlineKeyboardButtonData("🏪 متاجري", "shop:list"),
				tgbotapi.NewInlineKeyboardButtonData("➕ إنشاء متجر", "shop:create"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("📊 الإحصائيات", "stats:user"),
				tgbotapi.NewInlineKeyboardButtonData("⚙️ الإعدادات", "settings:main"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("🆘 الدعم", "support:main"),
				tgbotapi.NewInlineKeyboardButtonData("ℹ️ المساعدة", "help:main"),
			},
		}
	default: // Persian (fa)
		buttons = [][]tgbotapi.InlineKeyboardButton{
			{
				tgbotapi.NewInlineKeyboardButtonData("🏪 فروشگاه‌های من", "shop:list"),
				tgbotapi.NewInlineKeyboardButtonData("➕ ایجاد فروشگاه", "shop:create"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("📊 آمار", "stats:user"),
				tgbotapi.NewInlineKeyboardButtonData("⚙️ تنظیمات", "settings:main"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("🆘 پشتیبانی", "support:main"),
				tgbotapi.NewInlineKeyboardButtonData("ℹ️ راهنما", "help:main"),
			},
		}
	}

	return tgbotapi.NewInlineKeyboardMarkup(buttons...)
}

// GetAdminKeyboard returns admin keyboard
func (u *Utils) GetAdminKeyboard(language string) tgbotapi.InlineKeyboardMarkup {
	var buttons [][]tgbotapi.InlineKeyboardButton

	switch language {
	case "en":
		buttons = [][]tgbotapi.InlineKeyboardButton{
			{
				tgbotapi.NewInlineKeyboardButtonData("👥 Users", "admin:users"),
				tgbotapi.NewInlineKeyboardButtonData("🏪 Shops", "admin:shops"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("📊 Statistics", "admin:stats"),
				tgbotapi.NewInlineKeyboardButtonData("⚙️ Settings", "admin:settings"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("📢 Broadcast", "admin:broadcast"),
				tgbotapi.NewInlineKeyboardButtonData("💾 Backup", "admin:backup"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("🏠 Main Menu", "start"),
			},
		}
	default: // Persian (fa)
		buttons = [][]tgbotapi.InlineKeyboardButton{
			{
				tgbotapi.NewInlineKeyboardButtonData("👥 کاربران", "admin:users"),
				tgbotapi.NewInlineKeyboardButtonData("🏪 فروشگاه‌ها", "admin:shops"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("📊 آمار", "admin:stats"),
				tgbotapi.NewInlineKeyboardButtonData("⚙️ تنظیمات", "admin:settings"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("📢 ارسال عمومی", "admin:broadcast"),
				tgbotapi.NewInlineKeyboardButtonData("💾 پشتیبان‌گیری", "admin:backup"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("🏠 منوی اصلی", "start"),
			},
		}
	}

	return tgbotapi.NewInlineKeyboardMarkup(buttons...)
}

// GetShopsKeyboard returns shops management keyboard
func (u *Utils) GetShopsKeyboard(language string) tgbotapi.InlineKeyboardMarkup {
	var buttons [][]tgbotapi.InlineKeyboardButton

	switch language {
	case "en":
		buttons = [][]tgbotapi.InlineKeyboardButton{
			{
				tgbotapi.NewInlineKeyboardButtonData("➕ Create New Shop", "shop:create"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("📋 My Shops", "shop:list"),
				tgbotapi.NewInlineKeyboardButtonData("📊 Shop Stats", "shop:stats"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("🏠 Main Menu", "start"),
			},
		}
	default: // Persian (fa)
		buttons = [][]tgbotapi.InlineKeyboardButton{
			{
				tgbotapi.NewInlineKeyboardButtonData("➕ ایجاد فروشگاه جدید", "shop:create"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("📋 فروشگاه‌های من", "shop:list"),
				tgbotapi.NewInlineKeyboardButtonData("📊 آمار فروشگاه", "shop:stats"),
			},
			{
				tgbotapi.NewInlineKeyboardButtonData("🏠 منوی اصلی", "start"),
			},
		}
	}

	return tgbotapi.NewInlineKeyboardMarkup(buttons...)
}

// GetLanguageKeyboard returns language selection keyboard
func (u *Utils) GetLanguageKeyboard() tgbotapi.InlineKeyboardMarkup {
	buttons := [][]tgbotapi.InlineKeyboardButton{
		{
			tgbotapi.NewInlineKeyboardButtonData("🇮🇷 فارسی", "language:fa"),
			tgbotapi.NewInlineKeyboardButtonData("🇺🇸 English", "language:en"),
		},
		{
			tgbotapi.NewInlineKeyboardButtonData("🇸🇦 العربية", "language:ar"),
		},
	}

	return tgbotapi.NewInlineKeyboardMarkup(buttons...)
}

// FormatPrice formats price with currency
func (u *Utils) FormatPrice(amount int, currency string) string {
	switch currency {
	case "IRR":
		return formatNumberWithCommas(amount) + " تومان"
	case "USD":
		return "$" + formatNumberWithCommas(amount)
	case "EUR":
		return "€" + formatNumberWithCommas(amount)
	default:
		return formatNumberWithCommas(amount) + " " + currency
	}
}

// formatNumberWithCommas adds commas to numbers for better readability
func formatNumberWithCommas(n int) string {
	str := ""
	num := n
	for num > 0 {
		if len(str) > 0 && len(str)%4 == 3 {
			str = "," + str
		}
		str = string(rune('0'+num%10)) + str
		num /= 10
	}
	if str == "" {
		str = "0"
	}
	return str
}

// IsValidLanguage checks if language is supported
func (u *Utils) IsValidLanguage(lang string) bool {
	validLanguages := []string{"fa", "en", "ar"}
	for _, validLang := range validLanguages {
		if lang == validLang {
			return true
		}
	}
	return false
}
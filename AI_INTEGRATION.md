# 🤖 AI Support Integration for CodeRoot Bot

## Overview
The CodeRoot bot now includes an advanced AI support system powered by **Gemini 2.0 Flash** via Liara AI API. This system provides intelligent, context-aware customer support in three languages: Persian, English, and Arabic.

## 🎯 Features

### 1. Multi-Language AI Support
- **Persian (فارسی)**: Native support with Persian context
- **English**: Full English language support  
- **Arabic (العربية)**: Complete Arabic language support

### 2. Natural Language Processing
- **Question Detection**: Automatically detects user questions
- **Intent Analysis**: Understands user intent and urgency
- **Context Awareness**: Uses user profile and shop information

### 3. AI Commands

#### `/support` Command
```
/support                    # Show support menu
/support how to create shop # Direct AI question
/support چطور فروشگاه بسازم؟  # Persian question
/support كيف أنشئ متجر؟      # Arabic question
```

#### Natural Language Questions
Users can ask questions directly without commands:
- "چطور محصول اضافه کنم؟"
- "How do I upgrade my plan?"
- "ما هي أسعار الخطط؟"

### 4. Support Callbacks
- `support_contact`: Show AI support interface
- `support_faq`: AI-powered FAQ responses
- `support_quick_help`: Contextual help based on user state

## 🔧 Technical Implementation

### AI Service Architecture
```
services/ai_support.py
├── AISupport (Core AI class)
│   ├── get_ai_response()
│   ├── analyze_user_intent()
│   ├── generate_faq_response()
│   └── get_contextual_help()
└── AISupportManager (Integration layer)
    ├── handle_support_request()
    ├── get_quick_help()
    └── search_faq()
```

### Configuration
```env
# AI Support Configuration
AI_ENABLED=true
AI_BASE_URL=https://ai.liara.ir/api/v1/687e3da1990c24f61dae6d13
AI_API_KEY=your_api_key_here
AI_MODEL=google/gemini-2.0-flash-001
AI_MAX_TOKENS=1000
AI_TEMPERATURE=0.7
```

### Dependencies
```
openai>=1.0.0  # OpenAI-compatible client for Liara AI
```

## 🎓 AI Training Context

### System Context (Persian)
The AI is trained with comprehensive knowledge about:
- CodeRoot features and functionality
- Subscription plans (Free, Professional, VIP)
- Payment methods and pricing
- Common issues and solutions
- Bot commands and navigation

### User Context Integration
The AI receives contextual information:
```python
context = {
    'user_id': user_id,
    'language': user_lang,
    'has_shop': bool(user.get('shop_id')),
    'plan': user.get('subscription_plan', 'free')
}
```

## 🚀 Usage Examples

### 1. Direct Support Command
```
User: /support چطور پلن خودم رو ارتقا بدم؟
Bot: 🤖 پاسخ هوشمند:

برای ارتقای پلن خود این مراحل رو انجام بدید:

1️⃣ وارد منوی اصلی شوید
2️⃣ روی "فروشگاه من" کلیک کنید
3️⃣ "تمدید/ارتقای پلن" را انتخاب کنید
...
```

### 2. Natural Language Detection
```
User: مشکل دارم با پرداخت
Bot: 🤖 پاسخ هوشمند:

برای حل مشکل پرداخت:
- رسید پرداخت را به @hadi_admin ارسال کنید
- شماره کارت: 6037-9977-7766-5544
...
```

### 3. Multi-Language Support
```
User: How much does the VIP plan cost?
Bot: 🤖 Smart Response:

VIP Plan pricing:
💰 Price: 60,000 Toman/month
✨ Features: Unlimited products, no commission, dedicated gateway
...
```

## 📊 Analytics Integration

The AI system logs interactions for analytics:
```python
await db_manager.analytics.record_event('ai_support_used', user_id)
await db_manager.analytics.record_event('ai_question_answered', user_id)
```

## 🔒 Security & Error Handling

### Fallback Mechanisms
- If AI is disabled: Falls back to human support contact
- If API fails: Provides graceful error messages
- If no context: Uses default CodeRoot information

### Rate Limiting
- Built-in request throttling
- User session management
- Context caching for performance

## 🎯 Benefits for HADI's Business

### 1. 24/7 Support
- Instant responses to user questions
- Reduced support workload
- Higher user satisfaction

### 2. Multi-Language Reach
- Supports Persian, English, and Arabic users
- Expands market reach
- Localized support experience

### 3. Intelligent Assistance
- Context-aware responses
- Reduces repetitive support queries
- Improves user onboarding

### 4. Scalability
- Handles unlimited concurrent users
- No additional staffing needed
- Consistent support quality

## 🔮 Future Enhancements

### Phase 2 Features
- **Voice Support**: Audio message processing
- **Image Analysis**: Visual support for screenshots
- **Conversation Memory**: Multi-turn conversation context
- **Admin Analytics**: AI support performance metrics

### Advanced Training
- **Custom Fine-tuning**: Domain-specific model training
- **User Feedback Loop**: Continuous improvement based on user ratings
- **Integration with CRM**: Customer history awareness

## 📞 Human Fallback

When AI cannot help or user requests human support:
- Direct contact: `@hadi_admin`
- Automatic escalation for complex issues
- Seamless handoff from AI to human support

---

**Note**: The AI system enhances but doesn't replace human support. For complex business decisions and sensitive issues, users are directed to human administrators.
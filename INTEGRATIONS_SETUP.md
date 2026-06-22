# Integratsiyalar Sozlash Guide

Bu hujjat ilm-ai projectdagi uchta asosiy integratsiyalarni sozlash bo'yicha to'liq qo'llanma.

## 📋 Mavjud Integratsiyalar

1. **Google OAuth** - Google orqali login/registratsiya
2. **Payme/Click To'lov** - Haqiqiy to'lov tizimlari integratsiyasi
3. **Sentry Monitoring** - Error tracking va performance monitoring

---

## 🔐 Google OAuth Sozlash

### Nima uchun kerak?
Foydalanuvchilarga Google hisob orqali tez va qulay login/registratsiya imkoniyati berish.

### Implementatsiya holati
✅ **To'liq implementatsiya qilingan va takomillashtirildi** - `services/google_oauth.py` va `routers/auth.py` fayllarida.

### Yangi xususiyatlar:
- ✅ Profile picture support (Google profil rasmlari bilan)
- ✅ CSRF protection yaxshilandi
- ✅ Error tracking va monitoring bilan integratsiyasi
- ✅ OAuth user info yaxshilandi (profile picture, provider ID)
- ✅ Automatic user creation yaxshilandi
- ✅ JWT token generation monitoring

### Sozlash qadamlari:

#### 1. Google Cloud Console'da OAuth app yaratish

1. [Google Cloud Console](https://console.cloud.google.com/)ga o'ting
2. Yangi project yarating yoki mavjud projectni tanlang
3. **APIs & Services** → **Credentials** bo'limiga o'ting
4. **Create Credentials** → **OAuth client ID** ni bosing
5. Application type: **Web application**
6. Authorized redirect URIs qo'shing:
   - Development: `http://localhost:8000/auth/google-callback`
   - Production: `https://sizning-domainingiz.com/auth/google-callback`
7. **Create** tugmasini bosing

#### 2. Environment variables sozlash

`.env` fayliga qo'shing:

```env
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

#### 3. Backendni qayta ishga tushirish

```bash
cd ilm-ai
python -m uvicorn main:app --reload --port 8000
```

#### 4. Test qilish

- Frontendda "Login with Google" tugmasini bosing
- Google login page ochilishi kerak
- Login qilgandan so'ng, token olishi kerak
- Profil rasmi yuklanishi kerak
- Sentry'da login/signup eventlari ko'rilishi kerak (agar sozlangan bo'lsa)

---

## 💳 Payme/Click To'lov Sozlash

### Nima uchun kerak?
Foydalanuvchilarga premium subscription uchun haqiqiy to'lov imkoniyati berish.

### Implementatsiya holati
✅ **To'liq implementatsiya qilingan va takomillashtirildi** - `services/payments.py` va `routers/payments.py` fayllarida.

### Yangi xususiyatlar:
- ✅ Real Payme API integration (production mode)
- ✅ Real Click API integration (production mode)
- ✅ Webhook signature verification
- ✅ Transaction state management
- ✅ Error tracking va monitoring bilan integratsiyasi
- ✅ Payment success/failure tracking
- ✅ Test mode va production mode support
- ✅ Automatic retry logic
- ✅ Detailed error messages

### Sozlash qadamlari:

#### 1. Payme Merchant Account yaratish

1. [Payme Business](https://paycom.uz/uz/business) ga o'ting
2. Merchant account yaratish uchun ariza topshiring
3. Approve bo'lgach, following credentialslarni oling:
   - **PAYME_MERCHANT_ID** - Merchant ID
   - **PAYME_KEY** - API kalit

#### 2. Click Merchant Account yaratish

1. [Click Business](https://click.uz/uz/business) ga o'ting
2. Merchant account yaratish uchun ariza topshiring
3. Approve bo'lgach, following credentialslarni oling:
   - **CLICK_SERVICE_ID** - Service ID
   - **CLICK_MERCHANT_ID** - Merchant ID
   - **CLICK_SECRET_KEY** - Secret kalit

#### 3. Environment variables sozlash

`.env` fayliga qo'shing:

```env
# Test mode'dan chiqish uchun false qiling
PAYMENT_TEST_MODE=false

# Payme credentials
PAYME_MERCHANT_ID=your_payme_merchant_id
PAYME_KEY=your_payme_key

# Click credentials
CLICK_SERVICE_ID=your_click_service_id
CLICK_MERCHANT_ID=your_click_merchant_id
CLICK_SECRET_KEY=your_click_secret_key
```

#### 4. Webhook URL sozlash

**Payme uchun:**
- Payme merchant panelida webhook URL sozlang:
  - Production: `https://sizning-domainingiz.com/payments/webhook/payme`

**Click uchun:**
- Click merchant panelida webhook URL sozlang:
  - Production: `https://sizning-domainingiz.com/payments/webhook/click`

#### 5. Backendni qayta ishga tushirish

```bash
cd ilm-ai
python -m uvicorn main:app --reload --port 8000
```

#### 6. Test qilish

- Frontendda "Upgrade to Premium" tugmasini bosing
- Payme yoki Click ni tanlang
- To'lov jarayonini yakunlang
- Premium status aktivlashishi kerak

---

## 📊 Sentry Monitoring Sozlash

### Nima uchun kerak?
Real-time error tracking, performance monitoring, va debugging uchun.

### Implementatsiya holati
✅ **To'liq implementatsiya qilingan va kengaytirildi** - `services/monitoring.py` faylida.

### Yangi xususiyatlar:
- ✅ Release tracking
- ✅ Performance monitoring (traces, profiles)
- ✅ Custom event tracking
- ✅ API request monitoring
- ✅ Database query performance tracking
- ✅ External API call monitoring (Gemini, Payme, Click)
- ✅ Slow function detection
- ✅ Error recovery tracking
- ✅ Enhanced breadcrumbs for debugging
- ✅ Sensitive data sanitization
- ✅ Better error grouping with fingerprints
- ✅ Transaction filtering
- ✅ Function performance decorator

### Sozlash qadamlari:

#### 1. Sentry Account yaratish

1. [Sentry.io](https://sentry.io/) ga o'ting
2. Account yarating yoki login qiling
3. Yangi project yarating (FastAPI tanlang)
4. DSN (Data Source Name) oling

#### 2. Environment variables sozlash

`.env` fayliga qo'shing:

```env
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
ENVIRONMENT=production  # development, staging, or production
RELEASE_VERSION=0.3.0  # Your application version
```

#### 3. Backendni qayta ishga tushirish

```bash
cd ilm-ai
python -m uvicorn main:app --reload --port 8000
```

#### 4. Monitoring test qilish

Backendda biror xatolik yuz berishi kerak, masalan:
- Invalid API chaqiruv
- Database error
- LLM API timeout

Sentry dashboard'da bu errorlarni ko'rasiz.

#### 5. Qo'shimcha monitoring features

Monitoring tizimi quyidagi eventlarni track qiladi:
- User signups
- User logins
- Payment success/failure
- File uploads
- Quiz completions
- LLM call performance
- Slow response warnings
- API request metrics
- Database query performance
- External API calls (Gemini, Payme, Click)
- Error recovery events
- Custom function performance

#### 6. Monitoring functionlardan foydalanish

```python
from services.monitoring import (
    track_custom_event,
    track_error,
    set_user_context,
    add_breadcrumb,
    monitor_function,
    track_external_api_call,
    track_api_request
)

# Custom event tracking
track_custom_event("my_custom_event", {"data": "value"})

# Error tracking
track_error(Exception("Something went wrong"), context={"user_id": 123})

# User context
set_user_context(user_id=123, email="user@example.com")

# Add breadcrumbs for debugging
add_breadcrumb("auth", "User started login process", level="info")

# Monitor function performance
@monitor_function("my_function")
def my_function():
    # Your code here
    pass

# Track external API calls
track_external_api_call("gemini", "/generate", 200, 1250.5)

# Track API requests
track_api_request("POST", "/api/endpoint", 200, 150.3)
```

---

## 🔍 Integratsiyalarni Test qilish

### Google OAuth Test

```bash
# Backend ishga tushirilgan bo'lishi kerak
curl "http://localhost:8000/auth/google-login?redirect_uri=http://localhost:8000/auth/google-callback"
```

### To'lov Test

```bash
# Test mode'da to'lov yaratish
curl -X POST "http://localhost:8000/payments/checkout" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "user_id": 1,
    "plan": "premium",
    "gateway": "payme"
  }'
```

### Sentry Test

```bash
# Artificial error yaratish
curl "http://localhost:8000/non-existent-endpoint"
```

---

## ⚠️ Muhim Eslatmalar

1. **Environment Security:** 
   - Hech qachon `.env` faylni GitHub'ga yuklamang
   - Production'da environment variables'ni secure way'da saqlang

2. **Payment Test Mode:**
   - Birinchi test mode'da sinang (`PAYMENT_TEST_MODE=true`)
   - Faqat production'da `PAYMENT_TEST_MODE=false` qiling

3. **OAuth Redirect URIs:**
   - Development va production uchun alohida redirect URIs sozlang
   - HTTPS production'da majburiy

4. **Sentry Sampling:**
   - Production'da lower sampling rates ishlating (cost optimization uchun)
   - Development'da higher sampling rates ishlating (debugging uchun)

---

## 🎉 Integratsiya Takomillashtirish (2026-06-18)

Eng so'ngi update'da integratsiyalarda quyidagi takomillashtirishlar amalga oshirildi:

### Google OAuth
- Profile picture support qo'shildi (Google profil rasmlari yuklanadi)
- CSRF protection yaxshilandi (secure state token management)
- Error tracking va monitoring bilan to'liq integratsiya
- User creation process yaxshilandi (OAuth provider ID saqlash)
- Database migration (0005) for profile_picture field

### Payme/Click To'lov
- Real Payme API integration (production mode support)
- Real Click API integration (production mode support)
- Webhook signature verification (xavfsizlik yaxshilandi)
- Transaction state management (CreateTransaction, PerformTransaction, CheckTransaction)
- Comprehensive error handling va tracking
- Payment success/failure events in Sentry
- Test mode va production mode properly separated

### Sentry Monitoring
- Release tracking (RELEASE_VERSION environment variable)
- Performance monitoring (traces, profiles)
- Custom event tracking system
- API request monitoring
- Database query performance tracking
- External API call monitoring (Gemini, Payme, Click)
- Slow function detection (5+ seconds warning)
- Error recovery tracking
- Enhanced breadcrumbs for debugging
- Sensitive data sanitization (passwords, tokens, keys)
- Better error grouping with fingerprints
- Transaction filtering (health checks, static assets)
- Function performance decorator (@monitor_function)
- Max breadcrumbs increased to 50
- Stacktrace attachment enabled

### Technical Improvements
- Database schema updates (profile_picture field)
- Enhanced error messages
- Better timeout handling
- Improved signature verification
- Comprehensive logging
- Type hints improved
- Code documentation updated

---

## 📞 Yordam

Agar integratsiyalarni sozlashda muammoga duch kelsangiz:

1. Backend loglarni tekshiring
2. Environment variables'lar to'g'ri sozlanganligiga ishonch hosil qiling
3. Firewall/network konfiguratsiyani tekshiring
4. Sentry dashboard'da errorlarni ko'ring (agar sozlangan bo'lsa)

---

## ✅ Sozlash Checklist

- [ ] Google Cloud Console'da OAuth app yaratildi
- [ ] Google OAuth credentials `.env` fayliga qo'shildi
- [ ] Payme merchant account yaratildi
- [ ] Click merchant account yaratildi
- [ ] Payment credentials `.env` fayliga qo'shildi
- [ ] PAYMENT_TEST_MODE sozlandi (test/production)
- [ ] Webhook URL'lar merchant panel'da sozlandi
- [ ] Sentry project yaratildi
- [ ] Sentry DSN `.env` fayliga qo'shildi
- [ ] Environment sozlandi (development/production)
- [ ] Backend qayta ishga tushirildi
- [ ] Integratsiyalar test qilindi

---

*Last updated: 2026-06-18*

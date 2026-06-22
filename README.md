# 🎓 Ilm AI — Personal AI Learning Companion
 

>
> Ilm AI is a RAG-based intelligent learning platform that turns your documents into a personal tutor. Upload your materials and let AI quiz you, explain your mistakes, detect your knowledge gaps, and build a personalized learning plan.
 
---
 
## 🌐 Live Demo
 
- **Frontend:** *(https://github.com/UMIDABDURAZZOQOV/ilm-ai-frontend)*
- **Backend API Docs:** *(http://127.0.0.1:8000/docs)*
---
 
## 📸 Screenshots
 
### 🏠 Frontend
 
<img width="1538" height="759" alt="project5" src="https://github.com/user-attachments/assets/6fc5ed50-12dc-4b90-abe1-350bbced02a4" />
<img width="1565" height="757" alt="project1" src="https://github.com/user-attachments/assets/1044172b-e296-47ca-9da5-e6889e61711b" />
<img width="1562" height="750" alt="project2" src="https://github.com/user-attachments/assets/93fdd955-40a1-49a4-86df-7007493794b9" />
<img width="1560" height="769" alt="project3" src="https://github.com/user-attachments/assets/df9197e1-b7ba-4d6b-bdd7-90c01adae89b" />
<img width="1540" height="766" alt="project4" src="https://github.com/user-attachments/assets/edb64623-2d38-4359-b389-0f617df51d27" />


 
## ✨ Features
 
- 📄 **Document Upload** — Upload PDF, DOCX, TXT files and train your AI tutor
- 💬 **RAG Chat** — Answers strictly grounded in your uploaded materials, with citations
- 🧠 **Quiz Mode** — 3 difficulty levels (easy / medium / hard), with explanations after each answer
- 📈 **Knowledge Gap Detection** — Identifies concepts you consistently struggle with across sessions
- 📅 **Learning Plan Generator** — Creates a day-by-day study plan based on your goal and deadline
- 📱 **Telegram Bot** — Daily reminders, on-demand quizzes, streak notifications
- 💳 **Payment** — Premium subscription via Payme / Click
- 🌐 **Multilingual** — Uzbek, Russian, English
---


### 🔐 Authentication
 
<img width="1569" height="772" alt="project7" src="https://github.com/user-attachments/assets/fdb799c4-0b2d-45ea-aa68-337420a118e1" />
<img width="1566" height="774" alt="project6" src="https://github.com/user-attachments/assets/465f7381-656c-45cd-bd9f-65f81df08254" />

 
## � Integrations

The project includes three major integrations for production deployment:

### 🔐 Google OAuth
- **Status:** ✅ Fully implemented
- **Location:** `services/google_oauth.py`, `routers/auth.py`
- **Setup:** See [INTEGRATIONS_SETUP.md](INTEGRATIONS_SETUP.md#-google-oauth-sozlash)
- **Features:**
  - User registration/login with Google account
  - JWT token generation
  - CSRF protection with state tokens
  - Automatic user creation on first login

### 💳 Payment Gateways (Payme/Click)
- **Status:** ✅ Fully implemented (supports both test and production modes)
- **Location:** `services/payments.py`, `routers/payments.py`
- **Setup:** See [INTEGRATIONS_SETUP.md](INTEGRATIONS_SETUP.md#-paymeclick-tolov-sozlash)
- **Features:**
  - Payme payment integration
  - Click payment integration
  - Webhook handling for both gateways
  - Test mode for development
  - Premium subscription activation

### 📊 Sentry Monitoring
- **Status:** ✅ Fully implemented
- **Location:** `services/monitoring.py`
- **Setup:** See [INTEGRATIONS_SETUP.md](INTEGRATIONS_SETUP.md#-sentry-monitoring-sozlash)
- **Features:**
  - Error tracking and alerting
  - Performance monitoring
  - User context tracking
  - Custom event tracking (signups, logins, payments, quizzes)
  - LLM call performance monitoring
  - Sensitive data sanitization

For detailed integration setup instructions, see [INTEGRATIONS_SETUP.md](INTEGRATIONS_SETUP.md).

---

## �🛠 Tech Stack
 
### Backend
| Layer | Technology |
|-------|-----------|
| Framework | FastAPI (Python) |
| Database | PostgreSQL + pgvector |
| Migrations | Alembic |
| LLM | Google Gemini |
| Auth | JWT |
| Payments | Payme, Click |
| Messaging | Telegram Bot API |
 
### Frontend
| Layer | Technology |
|-------|-----------|
| Languages | HTML, CSS, JavaScript |
| Repo | [ilm-ai-frontend](https://github.com/UMIDABDURAZZOQOV/ilm-ai-frontend) |
 
### Infrastructure
| Layer | Technology |
|-------|-----------|
| Container | Docker + Docker Compose |
| CI/CD | GitHub Actions |
 
---
 
## 🚀 Quick Start
 
### Docker (Recommended)
 
```bash
# Clone the repository
git clone https://github.com/UMIDABDURAZZOQOV/ilm-ai.git
cd ilm-ai
 
# Start all services
docker compose up -d
```
 
### Manual Setup
 
```bash
# Install dependencies
pip install -r requirements.txt
 
# Run database migrations
alembic upgrade head
 
# Start backend
python main.py
 
# Start Telegram bot (separate terminal)
python run_telegram_bot.py
```

### 📊 Core Features Backend
 
<img width="1561" height="762" alt="project11" src="https://github.com/user-attachments/assets/d92a4152-b643-4aef-8bea-c66e122b19b6" />
<img width="1580" height="759" alt="project12" src="https://github.com/user-attachments/assets/b3cb7968-5e95-4adb-8c84-3401bcfc035b" />
<img width="1579" height="759" alt="project13" src="https://github.com/user-attachments/assets/fae69333-0db5-49f8-8384-0a34ff51c1f4" />
<img width="1586" height="767" alt="project8" src="https://github.com/user-attachments/assets/51af07aa-b3d6-409d-a4ac-ff03edbd2972" />
<img width="1590" height="769" alt="project9" src="https://github.com/user-attachments/assets/c9b1e40f-4471-409f-9881-18d5840eed9f" />
<img width="1567" height="773" alt="project10" src="https://github.com/user-attachments/assets/c8e293fe-1a78-4bb6-b959-3e5c517ce7d3" />


 
### Windows PowerShell Scripts
 
```powershell
# Start everything at once
./start_all.ps1
 
# Or start individually
./start_backend.ps1
./start_bot.ps1
./start_frontend.ps1
```
 
---
 
## 📁 Project Structure
 
```
ilm-ai/
├── main.py                  # FastAPI entry point
├── run_telegram_bot.py      # Telegram bot runner
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
│
├── routers/                 # API endpoints
│   ├── auth.py
│   ├── chat.py
│   ├── files.py
│   ├── quiz.py
│   ├── plan.py
│   ├── gaps.py
│   ├── payments.py
│   ├── feedback.py
│   └── telegram_link.py
│
├── services/                # Business logic
│   ├── db.py
│   ├── models.py
│   ├── users.py
│   ├── tokens.py
│   ├── quiz_engine.py
│   ├── quiz_history.py
│   ├── gap_detection.py
│   ├── payments.py
│   └── subscriptions.py
│
├── telegram_bot/            # Telegram bot
│   └── bot.py
│
├── alembic/                 # Database migrations
│   └── versions/
│       └── 0001_initial.py
│
├── diary/                   # Weekly progress diary
│   ├── 2026-05-28.md
│   ├── 2026-05-29.md
│   ├── 2026-05-31.md
│   └── 2026-06-01.md
│
├── tests/
│   └── test_smoke.py
│
└── assets/                  # Screenshots
```
 
---
 
## 🗓 Project Milestones
 
| Week | Milestone | Status |
|------|-----------|--------|
| Week 1 | Auth + File Upload + Basic RAG Chat | ✅ Done |
| Week 2 | Quiz Mode + Learning Plan + Telegram Bot | ✅ Done |
| Week 3 | Knowledge Gap Detection + Payment + Mobile UI | ✅ Done |
 
---
 
## 📓 Development Diary
 
Weekly progress diary is available in the `diary/` folder. Each entry covers what was done, problems encountered, solutions found, and next steps.
 
---
 
## 👤 Author
 
**Umid Abdurazzoqov**
AI Mentorship Program — AI Incubator Uzbekistan 2025
GitHub: [@UMIDABDURAZZOQOV](https://github.com/UMIDABDURAZZOQOV)
 
---
 
*Built with ❤️ during the AI Incubator Mentorship Program, Uzbekistan 2026*

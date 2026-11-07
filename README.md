# 🎓 Ilm AI — Your Personal AI Learning Companion

**Ilm AI** is a multilingual, AI-powered learning platform designed to make personalized education more accessible to learners in Uzbekistan. It brings together document-grounded AI tutoring, practice tools, learning analytics, and exam preparation in a connected web and mobile experience.

**Languages:** Uzbek · Russian · English  
**Status:** Active development — web platform available; Flutter app in development / pre-release

### 🌐 Explore the project

| Component | Link |
| --- | --- |
| Web app | [ilm-ai-edu.vercel.app](https://ilm-ai-edu.vercel.app) |
| Backend API | [ilm-ai](https://github.com/UMIDABDURAZZOQOV/ilm-ai) |
| Web frontend | [ilm-ai-frontend](https://github.com/UMIDABDURAZZOQOV/ilm-ai-frontend) |
| Flutter mobile app | [ilm-ai-flutter](https://github.com/UMIDABDURAZZOQOV/ilm-ai-flutter) |

> This repository contains the **Python backend and core application services**. The web interface and Flutter app are maintained in separate repositories and communicate with the same API.

## ✨ What Ilm AI does

### 📚 Learn from your own materials
- Upload learning materials and ask questions about their content.
- Use **Retrieval-Augmented Generation (RAG)** to retrieve relevant passages before generating responses.
- Create quizzes, explanations, flashcards, and study plans from learning materials.
- Track quiz history, progress, and areas that need more practice.

### 🤖 AI learning companion
- Personalized AI assistance with text, image, and voice interactions.
- Multilingual explanations and follow-up questions.
- Learning tools including summaries, knowledge maps, mock tests, and study aids.
- Voice features and some advanced tools depend on configured external services.

### 📝 Exam preparation and guided learning
- Practice and study experiences for SAT, IELTS, and Uzbekistan's **Milliy Sertifikat** subjects.
- Subject-based lessons, quizzes, progress tracking, and gamification.
- Practice analytics and AI-assisted explanations where supported.

> **Feature availability varies by platform.** Certain exam-preparation experiences are web-first or web-only; some content and integrations remain under development and require further quality checks.

### 📱 Web, mobile, and messaging
- Responsive web experience.
- Flutter mobile application with shared backend services.
- Telegram bot integrations for study interactions and reminders.

## 🧠 How the AI works

Ilm AI uses a document-grounded question-answering pipeline:

1. A learner uploads study material.
2. The backend processes and organizes the content.
3. Text is represented as embeddings for semantic retrieval.
4. Relevant content is retrieved for a learner's question.
5. An LLM generates a response using the retrieved context.
6. Related learning features use study results to suggest practice and next steps.

The runtime AI layer was **migrated from Google Gemini to OpenAI in August 2026**. Some historical filenames and documentation still reflect the earlier provider. Model choices are configurable through environment variables; offline content-generation workflows may use different providers.

## 🛠 Tech stack

| Area | Technologies |
| --- | --- |
| Backend | Python, FastAPI, SQLAlchemy, Uvicorn |
| Database | PostgreSQL, SQLite for local fallback |
| AI | OpenAI API, embeddings, RAG, multimodal processing |
| Web | Next.js 14, TypeScript, Tailwind CSS |
| Mobile | Flutter, Dart, Riverpod, go_router, Dio |
| Authentication | Google OAuth, JWT |
| Integrations | Telegram Bot API, payment and monitoring integrations |
| Deployment | Render (backend), Vercel (web) |
| Tooling | Docker, Docker Compose, GitHub Actions |

## 🏗 Repository structure

```text
ilm-ai/
├── main.py                 # FastAPI application entry point
├── routers/                # HTTP routes and API endpoints
├── services/               # Business logic, AI, retrieval, persistence
├── telegram_bot/           # Telegram bot integration
├── scripts/                # Development and data utilities
├── alembic/                # Migration-related files
├── migrations/             # Additional migration utilities
├── tests/                  # Test suite
├── data/                   # Data and development fixtures
├── .github/workflows/      # Automation and CI workflows
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example            # Configuration template — no real secrets
```

The structure may evolve as the project develops. See the repository for the current source of truth.

## 🚀 Getting started (backend)

### Prerequisites
- Python and pip
- Docker and Docker Compose (optional)
- Access to the external services required by the features you intend to run

### Run locally

```bash
git clone https://github.com/UMIDABDURAZZOQOV/ilm-ai.git
cd ilm-ai

python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure the necessary environment variables. **Never commit `.env`, access tokens, API keys, or private user data.**

```bash
python -m uvicorn main:app --reload
```

API documentation (local): **http://127.0.0.1:8000/docs**

Start the Telegram bot separately if configured:

```bash
python run_telegram_bot.py
```

**Note:** Some features need external credentials and database configuration. The local SQLite fallback is not a substitute for production PostgreSQL configuration.

### Docker

```bash
docker compose up -d
```

Review `docker-compose.yml` and your environment configuration before running services.

### Web frontend and Flutter

The interfaces are maintained separately:

- [Web setup and source](https://github.com/UMIDABDURAZZOQOV/ilm-ai-frontend)
- [Flutter setup and source](https://github.com/UMIDABDURAZZOQOV/ilm-ai-flutter)

Both clients use the backend API. Follow each repository's setup instructions for platform-specific configuration.

## 🔐 Privacy and security

Ilm AI handles learning materials and account data. Developers deploying this project should:

- Keep environment variables, signing credentials, and service keys private.
- Configure OAuth, CORS, authentication, and database access securely.
- Review the active AI provider's data handling and sharing settings before processing real learner materials.
- Use appropriately licensed or original educational content.
- Test integrations thoroughly before enabling them for real users.

See the deployed product's [privacy policy](https://ilm-ai-edu.vercel.app/privacy) for product-facing information.

## 📌 Project status

- **Web platform:** Deployed; individual features may still be refined.
- **Backend:** Deployed and actively maintained.
- **Flutter app:** Developed and tested; **not described here as publicly released on Google Play**.
- **README:** Updated to reflect the newer OpenAI-based runtime, Next.js web client, and Flutter mobile codebase.


## 👤 Project author

**Umidjon Abdurazzakov**  
GitHub: [@UMIDABDURAZZOQOV](https://github.com/UMIDABDURAZZOQOV)



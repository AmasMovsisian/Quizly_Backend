# Quizly Backend

Quizly is a Django REST API that converts YouTube videos into AI-generated quizzes.

The backend downloads audio from YouTube videos, processes the audio with FFmpeg, creates transcripts using Whisper AI, and generates quizzes using Google Gemini Flash.

---

# Installation

## FFmpeg Installation

FFmpeg is required for audio processing with Whisper AI.

### Windows

```bash
winget install --id Gyan.FFmpeg -e --source winget
```

### macOS

```bash
brew install ffmpeg
```

### Linux

```bash
sudo apt update
sudo apt install ffmpeg
```

---

# Setup Project

## 1. Clone the repository

```bash
git clone <repository-url>
```

## 2. Navigate into the project

```bash
cd Quizly_Backend
```

## 3. Create a virtual environment

```bash
python -m venv .venv
```

## 4. Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create your local environment file from the template:

```bash
cp .env.template .env
```

Open the `.env` file and replace the placeholder values with your own settings:

```env
SECRET_KEY=your_django_secret_key

DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1

GEMINI_API_KEY=your_gemini_api_key
```

Generate a Django secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

The `GEMINI_API_KEY` is required for AI-generated quiz creation.

Create your free API key:

https://ai.google.dev/

# Database Setup

Run migrations:

```bash
python manage.py migrate
```

---

# Start Backend

Run the development server:

```bash
python manage.py runserver
```

Backend URL:

```
http://127.0.0.1:8000/
```

---

# Project Structure

```
Quizly_Backend/
│
├── core/
│   ├── settings.py
│   └── urls.py
│
├── api/
├── users/
├── quizzes/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# API Endpoints

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register a new user |
| POST | `/api/login/` | Login user |
| POST | `/api/logout/` | Logout user |
| POST | `/api/token/refresh/` | Refresh access token |

---

## Quiz Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/quizzes/` | Generate a quiz from a YouTube URL |
| GET | `/api/quizzes/` | Get all user quizzes |
| GET | `/api/quizzes/{id}/` | Get one quiz |
| PATCH | `/api/quizzes/{id}/` | Update quiz information |
| DELETE | `/api/quizzes/{id}/` | Delete quiz |

---

# AI Quiz Generation Workflow

1. User submits a YouTube URL.
2. `yt-dlp` extracts the audio.
3. FFmpeg prepares the audio file.
4. Whisper AI creates a transcript.
5. Gemini Flash generates quiz questions.
6. Quiz data is saved in the database.
7. The API returns the generated quiz.

---

# Frontend

The frontend is provided by Developer Akademie and communicates with this backend through REST API endpoints.

Frontend Repository:

https://github.com/AmasMovsisian/Quizly_Frontend

---

# Author

**Amas Movsisian**  
**Backend Developer**

Fully developed the complete Quizly backend, including REST API design, authentication system, database structure, AI integration, media processing workflow, and backend architecture.

**Project Date:** 07/2026
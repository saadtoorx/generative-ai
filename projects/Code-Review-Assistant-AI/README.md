# Code Review Assistant AI

A production-ready code review application powered by a local CodeLlama model via Ollama. Features a FastAPI backend and a modern Streamlit frontend.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🔍 **Multiple Review Types** - Bug Detection, Code Quality, Performance, Security, and General reviews
- 📊 **Code Statistics** - Automatic calculation of lines, characters, and words
- 📋 **Session History** - Track and view your past reviews within the session
- 📥 **Export Results** - Download reviews as Markdown files
- ⚙️ **Configurable** - Adjust timeouts and model settings
- 🔍 **Health Status** - Real-time API and Ollama connection monitoring
- 🟢 **Visual Feedback** - Color-coded badges and status indicators
- 🔒 **Privacy** - All code processing happens locally on your machine

## 🏗️ Architecture

```
┌─────────────────┐     HTTP      ┌─────────────────┐     HTTP      ┌─────────────────┐
│                 │   POST/GET    │                 │   /api        │                 │
│   Streamlit     │ ────────────▶ │    FastAPI      │ ────────────▶ │     Ollama      │
│   Frontend      │               │    Backend      │               │   (CodeLlama)   │
│   (Port 8501)   │ ◀──────────── │   (Port 8000)   │ ◀──────────── │   (Port 11434)  │
│                 │     JSON      │                 │     JSON      │                 │
└─────────────────┘               └─────────────────┘               └─────────────────┘
```

## 📋 Prerequisites

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Ollama** - [Install Ollama](https://ollama.ai/download)
- **CodeLlama Model** - Run `ollama pull codellama` after installing Ollama

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/saadtoorx/Code-Review-Assistant-AI
cd "Project 4 Code Review Assistant AI Project"
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment (Optional)

```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Start Ollama

Make sure Ollama is running:

```bash
ollama serve
```

### 6. Run the Application

**Terminal 1 - Start Backend:**

```bash
python -m uvicorn backend.main:app --reload
```

**Terminal 2 - Start Frontend:**

```bash
streamlit run frontend/app.py
```

### 7. Open the App

Navigate to `http://localhost:8501` in your browser.

## 📚 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

| Method | Endpoint   | Description                   |
| ------ | ---------- | ----------------------------- |
| GET    | `/health`  | Check API and Ollama status   |
| POST   | `/review`  | Submit code for review (JSON) |
| POST   | `/review/` | Legacy endpoint (Form data)   |

## 🎨 Screenshots

_Coming soon_

## 🛠️ Configuration

Environment variables (set in `.env`):

| Variable          | Default                               | Description                |
| ----------------- | ------------------------------------- | -------------------------- |
| `OLLAMA_URL`      | `http://localhost:11434/api/generate` | Ollama API URL             |
| `MODEL_NAME`      | `codellama`                           | Model to use               |
| `REQUEST_TIMEOUT` | `300`                                 | Request timeout in seconds |
| `BACKEND_URL`     | `http://localhost:8000`               | FastAPI Backend URL        |

## 📁 Project Structure

```
Code Review Assistant AI Project/
├── backend/
│   ├── services/
│   │   └── llm_service.py  # Ollama integration
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── main.py             # FastAPI application
│   └── models.py           # Pydantic models
├── frontend/
│   └── app.py              # Streamlit application
├── V1/                     # Version 1 of project
├── .env                    # Environment variables
├── .env.example            # Environment template
├── README.md
└── requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - Local LLM runner
- [CodeLlama](https://github.com/facebookresearch/codellama) - State-of-the-art code model
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Streamlit](https://streamlit.io/) - Data app framework

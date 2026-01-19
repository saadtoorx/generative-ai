# Pro Image Caption Generator

A production-ready image captioning application powered by a local LLaVA vision-language model via Ollama. Features a FastAPI backend and a modern Streamlit frontend.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.127+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.49+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 📸 **Image Captioning** - Generate detailed descriptions for any image using LLaVA.
- 🎭 **Tone Selection** - Choose from styles like Professional, Funny, Creative, or Social Media.
- #️⃣ **Hashtag Generator** - Automatically generate relevant hashtags for social media growth.
- 🗣️ **Text-to-Speech (TTS)** - Listen to the generated captions instantly.
- 📜 **History** - Track and view your past generated captions in the current session.
- 📥 **Export Results** - Download captions as text files.
- ⚙️ **Configurable** - Customize prompts and API settings.
- 🔒 **Privacy** - All processing happens locally.

## 🏗️ Architecture

```
┌─────────────────┐     HTTP      ┌─────────────────┐     HTTP      ┌─────────────────┐
│                 │   POST/GET    │                 │   /api        │                 │
│   Streamlit     │ ────────────▶ │    FastAPI      │ ────────────▶ │     Ollama      │
│   Frontend      │               │    Backend      │               │     (LLaVA)     │
│   (Port 8501)   │ ◀──────────── │   (Port 8000)   │ ◀──────────── │   (Port 11434)  │
│                 │     JSON      │                 │     JSON      │                 │
└─────────────────┘               └─────────────────┘               └─────────────────┘
```

## 📋 Prerequisites

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Ollama** - [Install Ollama](https://ollama.ai/download)
- **LLaVA Model** - Run `ollama pull llava` after installing Ollama

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "Project 3 Image Caption Generation AI Project"
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

The application works out-of-the-box with default settings. You can modify `backend/config.py` if needed.

### 5. Start Ollama

Make sure Ollama is running:

```bash
ollama serve
```

### 6. Run the Application

**Terminal 1 - Start Backend:**

```bash
uvicorn backend.main:app --reload
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

| Method | Endpoint    | Description                            |
| ------ | ----------- | -------------------------------------- |
| GET    | `/docs`     | API Documentation                      |
| POST   | `/caption/` | Generate caption for an uploaded image |

## 🎨 Screenshots

_Coming soon_

## 🛠️ Configuration

Settings can be managed in `backend/config.py`:

| Variable         | Default                               | Description             |
| ---------------- | ------------------------------------- | ----------------------- |
| `OLLAMA_API_URL` | `http://localhost:11434/api/generate` | Ollama API URL          |
| `MODEL_NAME`     | `llava`                               | Model to use by default |
| `HOST`           | `127.0.0.1`                           | Backend Host            |
| `PORT`           | `8000`                                | Backend Port            |

## 📁 Project Structure

```
Image Caption Generator/
├── backend/
│   ├── __init__.py
│   ├── config.py        # Configuration settings
│   ├── main.py          # FastAPI application
│   └── services.py      # Business logic & Ollama integration
├── frontend/
│   └── app.py           # Streamlit application
├── V1/                  # Legacy version
├── README.md
└── requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - Local LLM runner
- [LLaVA](https://llava-vl.github.io/) - Vision-Language Model
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Streamlit](https://streamlit.io/) - Data app framework

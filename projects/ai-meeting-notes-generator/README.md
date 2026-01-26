# AI Meeting Notes Generator

A production-ready meeting transcription and summarization application powered by OpenAI Whisper and a local LLaMA model via Ollama. Features a FastAPI backend and a modern Streamlit frontend.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🎤 **Audio Transcription** - Convert meeting audio files (MP3, WAV) to text using Whisper
- 📝 **Smart Summarization** - Generate concise meeting summaries with AI
- ✅ **Action Items** - Automatically extract tasks and action items
- 🏷️ **Key Topics** - Identify main discussion themes
- 📊 **Analytics** - View word counts and processing metrics
- 💾 **Export** - Download notes as TXT or Markdown files
- 📋 **Copy to Clipboard** - Quick copy functionality for all sections
- � **Privacy** - All processing happens locally (Whisper + Ollama)

## 🏗️ Architecture

```
┌─────────────────┐     HTTP      ┌─────────────────┐     Func      ┌─────────────────┐
│                 │   POST/GET    │                 │   Call        │                 │
│   Streamlit     │ ────────────▶ │    FastAPI      │ ────────────▶ │     Whisper     │
│   Frontend      │               │    Backend      │               │  (Transcriber)  │
│   (Port 8501)   │ ◀──────────── │   (Port 8000)   │ ◀──────────── │                 │
│                 │     JSON      │                 │     Text      │                 │
└─────────────────┘               └─────────────────┘               └───────┬─────────┘
                                                                            │
                                                          HTTP              ▼
                                                        ┌─────────────────────────────┐
                                                        │                             │
                                                        │      Ollama (LLaMA 2)       │
                                                        │      (Summarization)        │
                                                        │      (Port 11434)           │
                                                        │                             │
                                                        └─────────────────────────────┘
```

## 📋 Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Ollama** - [Install Ollama](https://ollama.ai/download)
- **LLaMA 2 Model** - Run `ollama pull llama2` after installing Ollama
- **FFmpeg** - [Download](https://ffmpeg.org/download.html) (Required for audio processing)
  - Ensure FFmpeg bin folder is added to system PATH

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/saadtoorx/ai-meeting-notes-generator.git
cd ai-meeting-notes-generator
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

Make sure Ollama is running with the Llama2 model:

```bash
ollama serve
```

### 6. Run the Application

**Terminal 1 - Start Backend:**

```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 - Start Frontend:**

```bash
cd frontend
streamlit run app.py
```

### 7. Open the App

Navigate to `http://localhost:8501` in your browser.

## 📚 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

| Method | Endpoint    | Description                           |
| ------ | ----------- | ------------------------------------- |
| GET    | `/health`   | Check API, Ollama, and Whisper status |
| POST   | `/process/` | Upload audio and generate notes       |
| GET    | `/`         | Root endpoint info                    |

## 🎨 Screenshots

_Coming soon_

## 🛠️ Configuration

Environment variables (set in `.env`):

| Variable        | Default                  | Description                                           |
| --------------- | ------------------------ | ----------------------------------------------------- |
| `WHISPER_MODEL` | `base`                   | Whisper model size (tiny, base, small, medium, large) |
| `OLLAMA_MODEL`  | `llama2`                 | LLM model to use for summarization                    |
| `OLLAMA_HOST`   | `http://localhost:11434` | Ollama API URL                                        |
| `API_HOST`      | `localhost`              | Backend API host                                      |
| `API_PORT`      | `8000`                   | Backend API port                                      |

## 📁 Project Structure

```
ai-meeting-notes-generator/
├── backend/
│   └── main.py           # FastAPI application with Whisper & Ollama
├── frontend/
│   └── app.py            # Streamlit application
├── V1                    # Previous version of the project
│   └── main.py           # FastAPI application with Whisper & Ollama      
├── .env.example          # Environment template
├── .gitignore            # Git ignore patterns
├── LICENSE               # MIT License
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - Local LLM runner
- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Streamlit](https://streamlit.io/) - Data app framework

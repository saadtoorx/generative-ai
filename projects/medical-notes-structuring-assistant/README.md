# 🏥 Medical Notes Structuring Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.53-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Transform unstructured clinical notes into organized medical data using AI**

[Features](#-features) •
[Installation](#-installation) •
[Usage](#-usage) •
[API Documentation](#-api-documentation) •
[Contributing](#-contributing)

</div>

---

## 📖 Overview

The **Medical Notes Structuring Assistant** is an AI-powered application that extracts structured medical information from unstructured doctor's notes. It uses LLaMA (via Ollama) to intelligently parse clinical text and identify key medical components.

### What it does:

- 📝 **Extracts** symptoms, diagnoses, medications, and follow-up instructions
- 🔄 **Processes** single notes or batch CSV files
- 📊 **Exports** structured data as CSV or JSON
- 🎨 **Provides** a modern, user-friendly interface

---

## ✨ Features

| Feature                        | Description                                           |
| ------------------------------ | ----------------------------------------------------- |
| 🩺 **AI-Powered Extraction**   | Uses LLaMA model to intelligently parse medical notes |
| 📝 **Single Note Mode**        | Analyze individual clinical notes in real-time        |
| 📁 **Batch Processing**        | Upload CSV files for bulk extraction                  |
| 📥 **Multiple Export Formats** | Download results as CSV or JSON                       |
| 🎨 **Modern UI**               | Professional medical-themed interface                 |
| 📊 **Progress Tracking**       | Real-time processing status and metrics               |
| ✅ **Health Monitoring**       | Built-in API and Ollama status checks                 |

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **AI Model**: LLaMA 2 via Ollama
- **Data Processing**: Pandas

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
2. **Ollama** - [Download Ollama](https://ollama.ai/)
3. **Git** (optional) - [Download Git](https://git-scm.com/)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/saadtoorx/generative-ai/tree/main/projects/medical-notes-structuring-assistant.git
cd medical-notes-structuring-assistant
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Start Ollama

```bash
# Download and install Ollama from https://ollama.ai/
# Then pull the LLaMA model:
ollama pull llama2
```

### 5. Start the Application

**Windows:**

```bash
start.bat
```

**macOS/Linux:**

```bash
chmod +x start.sh
./start.sh
```

**Or manually:**

```bash
# Terminal 1 - Start Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Start Frontend
cd frontend
streamlit run app.py
```

---

## 💻 Usage

### Accessing the Application

Once started, open your browser and navigate to:

- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

### Single Note Mode

1. Select the **"📝 Single Note"** tab
2. Paste or type a doctor's note in the text area
3. Click **"🔍 Extract Information"**
4. View the structured results
5. Download as JSON or CSV

### Batch Processing Mode

1. Select the **"📁 Batch Upload"** tab
2. Prepare a CSV file with columns: `patient_id`, `doctor_notes`
3. Upload your CSV file
4. Click **"🚀 Process All Notes"**
5. Review individual results
6. Download the complete dataset

### Sample Data

Click **"📥 Load Sample Data"** to test the application with pre-loaded medical notes.

---

## 📚 API Documentation

### Endpoints

| Method | Endpoint    | Description                 |
| ------ | ----------- | --------------------------- |
| GET    | `/`         | API information             |
| GET    | `/health`   | Health check status         |
| GET    | `/models`   | Available Ollama models     |
| POST   | `/extract/` | Extract medical information |

### Example Request

```bash
curl -X POST "http://localhost:8000/extract/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "note=Patient presents with severe headache and fever. Diagnosis: Migraine. Prescribed Ibuprofen."
```

### Example Response

```json
{
  "structured": "{\"symptoms\": [\"severe headache\", \"fever\"], \"diagnosis\": \"Migraine\", \"medications\": [\"Ibuprofen\"], \"follow_up\": \"Not specified\"}",
  "model_used": "llama2",
  "note_length": 95
}
```

---

## 📁 Project Structure

```
medical-notes-structuring-assistant/
├── backend/
│   └── main.py              # FastAPI backend server
├── frontend/
│   └── app.py               # Streamlit frontend application
├── data/
│   └── example_notes.csv    # Sample medical notes
├── .env.example             # Environment configuration template
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── start.bat                # Windows startup script
├── start.sh                 # Unix startup script
└── debug_extraction.py      # Debug utility script
```

---

## ⚙️ Configuration

Copy `.env.example` to `.env` and modify as needed:

```env
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=llama2
BACKEND_HOST=http://localhost:8000
BACKEND_PORT=8000
STREAMLIT_PORT=8501
```

---

## 🔧 Troubleshooting

### Common Issues

| Issue                          | Solution                                 |
| ------------------------------ | ---------------------------------------- |
| **"Cannot connect to Ollama"** | Ensure Ollama is running: `ollama serve` |
| **"Model not found"**          | Pull the model: `ollama pull llama2`     |
| **Backend not responding**     | Check if port 8000 is available          |
| **Frontend not loading**       | Verify Streamlit is installed correctly  |

### Checking Service Status

```bash
# Check Ollama
curl http://localhost:11434/api/tags

# Check Backend
curl http://localhost:8000/health
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Streamlit](https://streamlit.io/) for the frontend framework
- [Meta AI](https://ai.meta.com/) for the LLaMA model

---

<div align="center">

**Built by Saad Toor (saadtoorx)**

</div>

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Medical Notes Structuring API",
    description="API for extracting structured medical information from doctor's notes using LLaMA",
    version="1.0.0"
)

# CORS Configuration for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama2"


class HealthResponse(BaseModel):
    status: str
    api_version: str
    ollama_status: str
    timestamp: str


class ModelInfo(BaseModel):
    name: str
    available: bool


def check_ollama_status() -> dict:
    """Check if Ollama is running and accessible."""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            return {"status": "connected", "models": response.json().get("models", [])}
        return {"status": "error", "models": []}
    except requests.exceptions.ConnectionError:
        return {"status": "disconnected", "models": []}
    except Exception as e:
        return {"status": f"error: {str(e)}", "models": []}


def query_llama(prompt: str, model: str = DEFAULT_MODEL) -> dict:
    """Query the Ollama LLaMA model with the given prompt."""
    logger.info(f"Querying model '{model}' with prompt length: {len(prompt)} chars")
    
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        
        if response.status_code == 404:
            logger.error(f"Model '{model}' not found")
            return {"error": f"Model '{model}' not found. Run `ollama pull {model}` to download it."}
        
        response.raise_for_status()
        logger.info("Successfully received response from Ollama")
        return response.json()
        
    except requests.exceptions.ConnectionError:
        logger.error("Ollama connection failed")
        return {"error": "Cannot connect to Ollama. Please ensure Ollama is running on port 11434."}
    except requests.exceptions.Timeout:
        logger.error("Ollama request timed out")
        return {"error": "Request timed out. The model is taking too long to respond."}
    except Exception as e:
        logger.error(f"Ollama error: {str(e)}")
        return {"error": f"Ollama Error: {str(e)}"}


@app.get("/", tags=["Root"])
def root():
    """Root endpoint with API information."""
    return {
        "message": "Medical Notes Structuring API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Check the health status of the API and Ollama connection."""
    ollama_info = check_ollama_status()
    
    return HealthResponse(
        status="healthy",
        api_version="1.0.0",
        ollama_status=ollama_info["status"],
        timestamp=datetime.now().isoformat()
    )


@app.get("/models", tags=["Models"])
def get_available_models():
    """Get list of available Ollama models."""
    ollama_info = check_ollama_status()
    
    if ollama_info["status"] != "connected":
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Please ensure it is running."
        )
    
    models = [
        {
            "name": model.get("name", "unknown"),
            "size": model.get("size", 0),
            "modified": model.get("modified_at", "")
        }
        for model in ollama_info["models"]
    ]
    
    return {"models": models, "default": DEFAULT_MODEL}


@app.post("/extract/", tags=["Extraction"])
def extract_medical_info(
    note: str = Form(...),
    model: Optional[str] = Form(DEFAULT_MODEL)
):
    """
    Extract structured medical information from a doctor's note.
    
    - **note**: The doctor's note text to analyze
    - **model**: The Ollama model to use (default: llama2)
    
    Returns structured data including:
    - Symptoms
    - Diagnosis
    - Medications
    - Follow-up Instructions
    """
    logger.info(f"Received extraction request - Note length: {len(note)} chars, Model: {model}")
    
    if not note or not note.strip():
        raise HTTPException(status_code=400, detail="Note cannot be empty")
    
    prompt = (
        "You are a medical information extraction assistant. "
        "Extract the following information from the doctor's note and return ONLY valid JSON:\n\n"
        "Required fields:\n"
        "- symptoms: List of symptoms mentioned\n"
        "- diagnosis: The diagnosis given\n"
        "- medications: List of medications prescribed\n"
        "- follow_up: Follow-up instructions\n\n"
        "If any field is not mentioned, use 'Not specified'.\n\n"
        "Return ONLY the JSON object, no additional text.\n\n"
        f"Doctor's Note:\n{note}\n\n"
        "JSON Output:"
    )

    result = query_llama(prompt, model)
    
    if "error" in result:
        logger.error(f"Extraction failed: {result['error']}")
        raise HTTPException(status_code=500, detail=result["error"])
    
    structured_data = result.get("response", "{}").strip()
    logger.info("Extraction completed successfully")
    
    return {
        "structured": structured_data,
        "model_used": model,
        "note_length": len(note)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

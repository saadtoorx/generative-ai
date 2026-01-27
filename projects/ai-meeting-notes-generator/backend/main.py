"""
AI Meeting Notes Generator - Backend API

This module provides the FastAPI backend for processing meeting audio files.
It uses OpenAI Whisper for transcription and Ollama (Llama2) for AI-powered
summarization, action item extraction, and key topic identification.
"""

import os
import time
import logging
import tempfile
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import whisper
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Initialize FastAPI app
app = FastAPI(
    title="AI Meeting Notes Generator API",
    description="API for transcribing meeting audio and generating AI-powered notes",
    version="1.0.0"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Whisper model at startup
logger.info(f"Loading Whisper model: {WHISPER_MODEL}")
model = whisper.load_model(WHISPER_MODEL)
logger.info("Whisper model loaded successfully")


# Pydantic models for response validation
class MeetingNotesResponse(BaseModel):
    """Response model for meeting notes generation."""
    transcript: str
    summary: str
    action_items: str
    key_topics: str
    word_count: int
    processing_time: float


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    whisper_model: str
    ollama_model: str
    ollama_status: str


class ErrorResponse(BaseModel):
    """Response model for error responses."""
    error: str
    detail: Optional[str] = None


def call_ollama(prompt: str) -> str:
    """
    Call the Ollama API to generate text based on the given prompt.
    
    Args:
        prompt: The prompt to send to the LLM.
        
    Returns:
        The generated text response.
        
    Raises:
        HTTPException: If the Ollama API call fails.
    """
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120  # 2 minute timeout for long responses
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to Ollama service")
        raise HTTPException(
            status_code=503,
            detail="Ollama service is not available. Please ensure Ollama is running."
        )
    except requests.exceptions.Timeout:
        logger.error("Ollama request timed out")
        raise HTTPException(
            status_code=504,
            detail="Request to Ollama timed out. Please try again."
        )
    except Exception as e:
        logger.error(f"Ollama API error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error calling Ollama: {str(e)}"
        )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Meeting Notes Generator API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify service status.
    
    Returns:
        Health status of the API and connected services.
    """
    # Check Ollama connectivity
    ollama_status = "unknown"
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            ollama_status = "connected"
        else:
            ollama_status = "error"
    except requests.exceptions.ConnectionError:
        ollama_status = "disconnected"
    except Exception:
        ollama_status = "error"
    
    return HealthResponse(
        status="healthy",
        whisper_model=WHISPER_MODEL,
        ollama_model=OLLAMA_MODEL,
        ollama_status=ollama_status
    )


@app.post("/process/", response_model=MeetingNotesResponse, tags=["Meeting Notes"])
async def process_audio(file: UploadFile = File(...)):
    """
    Process an audio file and generate meeting notes.
    
    This endpoint accepts an audio file (MP3 or WAV), transcribes it using
    Whisper, and then uses Ollama to generate a summary, action items,
    and key discussion topics.
    
    Args:
        file: The audio file to process (MP3 or WAV format).
        
    Returns:
        MeetingNotesResponse with transcript, summary, action items,
        key topics, word count, and processing time.
        
    Raises:
        HTTPException: If file processing fails.
    """
    start_time = time.time()
    
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_extension = file.filename.lower().split('.')[-1]
    if file_extension not in ['mp3', 'wav', 'm4a', 'flac', 'ogg']:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {file_extension}. Supported formats: mp3, wav, m4a, flac, ogg"
        )
    
    logger.info(f"Processing audio file: {file.filename}")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        logger.info("Transcribing audio with Whisper...")
        
        # Check if ffmpeg is available (simple check by running it)
        import shutil
        if not shutil.which("ffmpeg"):
            raise HTTPException(
                status_code=500,
                detail="FFmpeg is not installed or not found in system PATH. Please install FFmpeg to use audio transcription. (See README.md)"
            )

        # Transcribe audio
        try:
            result = model.transcribe(tmp_path)
            transcript = result["text"].strip()
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            error_msg = str(e)
            if "WinError 2" in error_msg or "No such file or directory" in error_msg: 
                 raise HTTPException(
                    status_code=500,
                    detail="FFmpeg not found. Please ensure FFmpeg is installed and added to your system PATH."
                )
            raise HTTPException(
                status_code=500,
                detail=f"Failed to transcribe audio: {error_msg}"
            )
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
        if not transcript:
            raise HTTPException(
                status_code=400,
                detail="No speech detected in the audio file"
            )
        
        logger.info(f"Transcription complete. Word count: {len(transcript.split())}")
        
        # Generate summary
        logger.info("Generating summary...")
        summary_prompt = (
            "You are a professional meeting assistant. Summarize the following meeting transcript "
            "in a clear and concise manner. Focus on the main points discussed and any decisions made. "
            "Keep the summary under 200 words.\n\n"
            f"Transcript:\n{transcript}\n\n"
            "Summary:"
        )
        summary = call_ollama(summary_prompt)
        
        # Extract action items
        logger.info("Extracting action items...")
        tasks_prompt = (
            "You are a professional meeting assistant. Extract all action items and tasks "
            "from the following meeting transcript. Format them as a numbered list. "
            "If no clear action items are found, write 'No specific action items identified.'\n\n"
            f"Transcript:\n{transcript}\n\n"
            "Action Items:"
        )
        action_items = call_ollama(tasks_prompt)
        
        # Extract key topics
        logger.info("Identifying key topics...")
        topics_prompt = (
            "You are a professional meeting assistant. Identify the main topics and themes "
            "discussed in this meeting. List them as short phrases (2-4 words each), "
            "separated by commas. Provide 3-7 key topics.\n\n"
            f"Transcript:\n{transcript}\n\n"
            "Key Topics:"
        )
        key_topics = call_ollama(topics_prompt)
        
        # Calculate metrics
        word_count = len(transcript.split())
        processing_time = round(time.time() - start_time, 2)
        
        logger.info(f"Processing complete. Total time: {processing_time}s")
        
        return MeetingNotesResponse(
            transcript=transcript,
            summary=summary,
            action_items=action_items,
            key_topics=key_topics,
            word_count=word_count,
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
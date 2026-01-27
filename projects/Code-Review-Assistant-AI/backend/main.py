"""
Code Review Assistant - FastAPI Backend
Production-ready API with multiple review types and proper error handling.
"""
import time
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.models import (
    CodeReviewRequest, 
    CodeReviewResponse, 
    CodeStats,
    HealthResponse,
    ErrorResponse
)
from backend.services.llm_service import llm_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Code Review Assistant API",
    description="AI-powered code review using local LLM",
    version="1.0.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint.
    Returns status of the API and Ollama connection.
    """
    settings = get_settings()
    ollama_connected = llm_service.check_connection()
    
    return HealthResponse(
        status="healthy",
        ollama_status="connected" if ollama_connected else "disconnected",
        model=settings.model_name
    )


@app.post("/review", response_model=CodeReviewResponse, responses={
    400: {"model": ErrorResponse},
    503: {"model": ErrorResponse}
})
def review_code(request: CodeReviewRequest):
    """
    Review code using AI.
    
    Accepts code and review type, returns comprehensive review.
    """
    start_time = time.time()
    
    # Validate input
    if not request.code.strip():
        raise HTTPException(
            status_code=400,
            detail="Code cannot be empty"
        )
    
    # Check code length (prevent extremely long inputs)
    if len(request.code) > 50000:
        raise HTTPException(
            status_code=400,
            detail="Code too long. Maximum 50,000 characters allowed."
        )
    
    try:
        logger.info(f"Processing {request.review_type.value} review request")
        
        # Get review from LLM
        review = llm_service.get_review(
            code=request.code,
            review_type=request.review_type.value,
            language=request.language
        )
        
        # Calculate stats
        lines = request.code.count('\n') + 1
        characters = len(request.code)
        words = len(request.code.split())
        
        response_time = round(time.time() - start_time, 2)
        
        logger.info(f"Review completed in {response_time}s")
        
        return CodeReviewResponse(
            review=review,
            review_type=request.review_type.value,
            stats=CodeStats(
                lines=lines,
                characters=characters,
                words=words
            ),
            response_time=response_time
        )
        
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Please ensure it is running."
        )
    except TimeoutError as e:
        logger.error(f"Timeout error: {e}")
        raise HTTPException(
            status_code=503,
            detail="Request timed out. Try with shorter code."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )


# Keep legacy endpoint for backward compatibility
from fastapi import Form

@app.post("/review/")
def review_code_legacy(code: str = Form(...)):
    """
    Legacy endpoint for backward compatibility.
    Uses form data instead of JSON.
    """
    request = CodeReviewRequest(code=code)
    response = review_code(request)
    return {"review": response.review}

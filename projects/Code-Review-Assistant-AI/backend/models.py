"""
Pydantic models for request and response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ReviewType(str, Enum):
    """Available review types."""
    GENERAL = "general"
    BUGS = "bugs"
    QUALITY = "quality"
    PERFORMANCE = "performance"
    SECURITY = "security"


class CodeReviewRequest(BaseModel):
    """Request model for code review."""
    code: str = Field(..., min_length=1, description="Code to review")
    review_type: ReviewType = Field(default=ReviewType.GENERAL, description="Type of review")
    language: Optional[str] = Field(default=None, description="Programming language")


class CodeStats(BaseModel):
    """Statistics about the submitted code."""
    lines: int
    characters: int
    words: int


class CodeReviewResponse(BaseModel):
    """Response model for code review."""
    review: str
    review_type: str
    stats: CodeStats
    response_time: float


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    ollama_status: str
    model: str


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str
    detail: Optional[str] = None

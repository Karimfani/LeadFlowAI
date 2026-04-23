"""LeadFlow AI FastAPI application.

Provides a REST API for the lead generation pipeline.

Usage:
    uvicorn api.app:app --reload
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from leadflow.config import setup_logging
from leadflow.collector import fetch_leads
from leadflow.scorer import score_leads
from leadflow.generator import generate_messages
from leadflow.utils import filter_leads

logger = setup_logging()

app = FastAPI(
    title="LeadFlow AI",
    description="AI-powered lead generation tool for freelancers",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LeadRequest(BaseModel):
    """Request body for lead generation."""

    keyword: str
    location: str


class LeadResponse(BaseModel):
    """Response model for a single lead."""

    name: str
    rating: float
    has_website: bool
    contact: str
    score: int
    message: str


@app.get("/", tags=["info"])
def root() -> dict:
    """LeadFlow AI API root."""
    return {"name": "LeadFlow AI", "version": "1.0.0", "docs": "/docs"}


@app.post("/leads", response_model=List[LeadResponse], tags=["leads"])
def generate_leads(
    request: LeadRequest,
    min_score: int = Query(0, ge=0, description="Minimum score filter"),
) -> List[LeadResponse]:
    """Generate, score, and return leads for a keyword and location.

    Args:
        request: The lead generation request with keyword and location.
        min_score: Optional minimum score filter.

    Returns:
        A list of leads with scores and personalized outreach messages.
    """
    logger.info("Generating leads for keyword=%s location=%s", request.keyword, request.location)

    raw_leads = fetch_leads(request.keyword, request.location)
    scored_leads = score_leads(raw_leads)
    filtered = filter_leads(scored_leads, min_score=min_score)
    final_leads = generate_messages(filtered, request.keyword)

    return [LeadResponse(**lead) for lead in final_leads]


@app.get("/leads", response_model=List[LeadResponse], tags=["leads"])
def search_leads(
    keyword: str = Query(..., description="Business type"),
    location: str = Query(..., description="City or area"),
    min_score: Optional[int] = Query(None, ge=0, description="Minimum score filter"),
) -> List[LeadResponse]:
    """Generate leads via GET request (for quick testing).

    Args:
        keyword: The type of business to search for.
        location: The city or area to search in.
        min_score: Optional minimum score filter.

    Returns:
        A list of leads with scores and personalized outreach messages.
    """
    raw_leads = fetch_leads(keyword, location)
    scored_leads = score_leads(raw_leads)
    filtered = filter_leads(scored_leads, min_score=min_score or 0)
    final_leads = generate_messages(filtered, keyword)
    return [LeadResponse(**lead) for lead in final_leads]


@app.get("/health", tags=["health"])
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}

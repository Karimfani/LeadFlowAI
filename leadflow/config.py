"""Configuration management for LeadFlow AI."""

import os
import logging
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
DATA_DIR: str = os.getenv("DATA_DIR", "data")

SCORING_RULES = {
    "high_rating_threshold": 4.3,
    "high_rating_points": 2,
    "no_website_points": 2,
    "good_rating_threshold": 4.0,
    "good_rating_points": 1,
}

def setup_logging(level: str = LOG_LEVEL) -> logging.Logger:
    """Configure and return a logger instance."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger("leadflow")

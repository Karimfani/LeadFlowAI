"""Lead scoring engine.

Scores leads based on configurable business rules.
The higher the score, the more valuable the lead is for outreach.
"""

from typing import Dict, Any, List
from leadflow.config import SCORING_RULES


def score_lead(lead: Dict[str, Any], rules: Dict[str, Any] = None) -> int:
    """Calculate a numeric quality score for a single lead.

    Scoring rules (configurable via SCORING_RULES in config.py):
        - rating >= 4.3  → +2 points (high-rated business, trusted by customers)
        - no website     → +2 points (major opportunity: needs an online presence)
        - rating >= 4.0  → +1 point  (above-average business)

    Args:
        lead: A dictionary with at minimum 'rating' (float) and 'has_website' (bool).
        rules: Optional override for scoring rules. Falls back to config defaults.

    Returns:
        Integer score. Higher = better lead.
    """
    active_rules = rules or SCORING_RULES
    score = 0
    rating = float(lead.get("rating", 0))
    has_website = bool(lead.get("has_website", True))

    if rating >= active_rules["high_rating_threshold"]:
        score += active_rules["high_rating_points"]

    if not has_website:
        score += active_rules["no_website_points"]

    if rating >= active_rules["good_rating_threshold"]:
        score += active_rules["good_rating_points"]

    return score


def score_leads(leads: List[Dict[str, Any]], rules: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Score a list of leads and attach a 'score' field to each.

    Args:
        leads: A list of lead dictionaries.
        rules: Optional override for scoring rules.

    Returns:
        The same list with a 'score' key added to each lead, sorted descending by score.
    """
    scored = []
    for lead in leads:
        scored_lead = dict(lead)
        scored_lead["score"] = score_lead(lead, rules)
        scored.append(scored_lead)
    return sorted(scored, key=lambda x: x["score"], reverse=True)

"""General utility helpers for LeadFlow AI."""

from typing import List, Dict, Any, Optional


def format_lead_summary(lead: Dict[str, Any]) -> str:
    """Return a human-readable one-line summary of a lead.

    Args:
        lead: A lead dictionary.

    Returns:
        A formatted summary string.
    """
    name = lead.get("name", "Unknown")
    rating = lead.get("rating", 0)
    score = lead.get("score", 0)
    has_website = "has website" if lead.get("has_website") else "no website"
    contact = lead.get("contact", "N/A")
    return f"[Score: {score}] {name} | Rating: {rating} | {has_website} | {contact}"


def filter_leads(
    leads: List[Dict[str, Any]],
    min_score: Optional[int] = None,
    min_rating: Optional[float] = None,
    no_website_only: bool = False,
) -> List[Dict[str, Any]]:
    """Filter a list of leads based on criteria.

    Args:
        leads: The list of leads to filter.
        min_score: Only include leads with score >= min_score.
        min_rating: Only include leads with rating >= min_rating.
        no_website_only: If True, only include leads without a website.

    Returns:
        A filtered list of leads.
    """
    result = leads
    if min_score is not None:
        result = [l for l in result if l.get("score", 0) >= min_score]
    if min_rating is not None:
        result = [l for l in result if l.get("rating", 0) >= min_rating]
    if no_website_only:
        result = [l for l in result if not l.get("has_website", True)]
    return result


def sort_leads(
    leads: List[Dict[str, Any]],
    by: str = "score",
    descending: bool = True,
) -> List[Dict[str, Any]]:
    """Sort leads by a given field.

    Args:
        leads: The list of leads to sort.
        by: The field name to sort by. Defaults to 'score'.
        descending: If True, sort in descending order. Defaults to True.

    Returns:
        A sorted list of leads.
    """
    return sorted(leads, key=lambda x: x.get(by, 0), reverse=descending)

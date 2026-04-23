"""AI-powered outreach message generator.

Generates personalized, professional outreach messages for each lead.
Uses a high-quality template by default, with optional OpenAI integration
when an API key is provided in the .env file.
"""

import os
import logging
from typing import Dict, Any

logger = logging.getLogger("leadflow.generator")


def _generate_template_message(lead: Dict[str, Any], keyword: str = "") -> str:
    """Generate a personalized outreach message using a template.

    Args:
        lead: The lead dictionary with name, rating, has_website fields.
        keyword: The business keyword used during search.

    Returns:
        A formatted outreach message string.
    """
    name = lead.get("name", "there")
    rating = lead.get("rating", 0)
    has_website = lead.get("has_website", True)
    industry = keyword or "business"

    website_pitch = (
        "I noticed you're already online, but there's often room to streamline your booking or ordering system."
        if has_website
        else "I noticed your business doesn't have an online presence yet — that's a significant opportunity."
    )

    return f"""Hi {name},

I came across your {industry} on Google Maps and was genuinely impressed by your {rating}-star rating. {website_pitch}

I help businesses like yours set up modern online systems — from booking platforms to order management — that convert more customers and free up your team's time.

Would you be open to a quick 15-minute call this week? I'd love to share a few ideas specific to your situation at no cost.

Best regards"""


def _generate_openai_message(lead: Dict[str, Any], keyword: str, api_key: str) -> str:
    """Generate a message using the OpenAI API.

    Args:
        lead: The lead dictionary.
        keyword: Business keyword context.
        api_key: OpenAI API key.

    Returns:
        An AI-generated outreach message.

    Raises:
        ImportError: If the openai package is not installed.
        Exception: If the API call fails.
    """
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError("Install openai: pip install openai") from exc

    client = OpenAI(api_key=api_key)
    name = lead.get("name", "")
    rating = lead.get("rating", 0)
    has_website = lead.get("has_website", True)
    website_note = "no website" if not has_website else "has a website"

    prompt = (
        f"Write a short, professional cold outreach message to a {keyword} business called '{name}'. "
        f"Their Google rating is {rating}/5.0 and they {website_note}. "
        f"The message should: mention their rating, pitch the value of a better online booking or order system, "
        f"and end with a soft call to action for a 15-minute call. Keep it under 120 words. Be friendly but professional."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def generate_message(lead: Dict[str, Any], keyword: str = "") -> str:
    """Generate a personalized outreach message for a lead.

    Automatically uses OpenAI if OPENAI_API_KEY is set in the environment.
    Falls back to a high-quality template otherwise.

    Args:
        lead: The lead dictionary with name, rating, has_website, contact fields.
        keyword: The business keyword used in the search (adds context).

    Returns:
        A personalized outreach message string.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if api_key:
        try:
            logger.debug("Generating message with OpenAI for lead: %s", lead.get("name"))
            return _generate_openai_message(lead, keyword, api_key)
        except Exception as exc:
            logger.warning("OpenAI generation failed, falling back to template: %s", exc)

    return _generate_template_message(lead, keyword)


def generate_messages(leads: list[Dict[str, Any]], keyword: str = "") -> list[Dict[str, Any]]:
    """Generate outreach messages for a list of leads.

    Args:
        leads: List of lead dictionaries.
        keyword: The search keyword for context.

    Returns:
        The same list with a 'message' key added to each lead.
    """
    result = []
    for lead in leads:
        enriched = dict(lead)
        enriched["message"] = generate_message(lead, keyword)
        result.append(enriched)
    return result

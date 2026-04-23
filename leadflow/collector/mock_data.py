"""Mock data provider for lead collection.

In a real implementation, this would call a real API such as Google Maps Places API.
We use mock data to avoid any API costs or rate-limiting during development.
"""

from typing import List, Dict, Any
import random

MOCK_LEADS_POOL: List[Dict[str, Any]] = [
    {"name": "Al Baik Restaurant", "rating": 4.7, "has_website": False, "contact": "+971-4-555-0101"},
    {"name": "Zara Boutique", "rating": 3.9, "has_website": True, "contact": "+971-4-555-0102"},
    {"name": "Golden Spice Kitchen", "rating": 4.5, "has_website": False, "contact": "+971-4-555-0103"},
    {"name": "Metro Dental Clinic", "rating": 4.1, "has_website": False, "contact": "+971-4-555-0104"},
    {"name": "Sunrise Cafe", "rating": 4.8, "has_website": True, "contact": "+971-4-555-0105"},
    {"name": "The Urban Barber", "rating": 4.4, "has_website": False, "contact": "+971-4-555-0106"},
    {"name": "Green Garden Nursery", "rating": 3.7, "has_website": True, "contact": "+971-4-555-0107"},
    {"name": "Blue Wave Laundry", "rating": 4.2, "has_website": False, "contact": "+971-4-555-0108"},
    {"name": "Peak Fitness Studio", "rating": 4.6, "has_website": False, "contact": "+971-4-555-0109"},
    {"name": "Artisan Pizza House", "rating": 4.3, "has_website": True, "contact": "+971-4-555-0110"},
    {"name": "City Lights Photography", "rating": 4.9, "has_website": False, "contact": "+971-4-555-0111"},
    {"name": "Happy Paws Pet Store", "rating": 3.8, "has_website": False, "contact": "+971-4-555-0112"},
    {"name": "Modern Auto Garage", "rating": 4.4, "has_website": True, "contact": "+971-4-555-0113"},
    {"name": "Fresh Juice Bar", "rating": 4.6, "has_website": False, "contact": "+971-4-555-0114"},
    {"name": "Elite Spa & Wellness", "rating": 4.3, "has_website": False, "contact": "+971-4-555-0115"},
]


def fetch_leads(keyword: str, location: str) -> List[Dict[str, Any]]:
    """Fetch leads for a given keyword and location.

    Args:
        keyword: The type of business to search for (e.g., "restaurant", "dentist").
        location: The city or area to search in (e.g., "Dubai", "New York").

    Returns:
        A list of lead dictionaries with name, rating, has_website, and contact fields.

    Note:
        This implementation returns mock data. Replace with a real API integration
        (Google Maps Places API, Yelp API, etc.) for production use.
    """
    sample_size = min(len(MOCK_LEADS_POOL), random.randint(8, 12))
    leads = random.sample(MOCK_LEADS_POOL, sample_size)

    result = []
    for lead in leads:
        result.append({
            "name": lead["name"],
            "rating": lead["rating"],
            "has_website": lead["has_website"],
            "contact": lead["contact"],
        })

    return result

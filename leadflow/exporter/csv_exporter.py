"""CSV exporter for lead data."""

import csv
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger("leadflow.exporter.csv")

DEFAULT_FIELDS = ["name", "rating", "has_website", "contact", "score", "message"]


def export_csv(
    leads: List[Dict[str, Any]],
    output_path: str = "data/leads.csv",
    fields: List[str] = None,
) -> str:
    """Export leads to a CSV file.

    Args:
        leads: List of lead dictionaries to export.
        output_path: File path for the output CSV. Defaults to 'data/leads.csv'.
        fields: List of fields to include. Defaults to all standard fields.

    Returns:
        The absolute path to the created CSV file.

    Raises:
        IOError: If the file cannot be written.
    """
    active_fields = fields or DEFAULT_FIELDS
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=active_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(leads)

    abs_path = os.path.abspath(output_path)
    logger.info("Exported %d leads to CSV: %s", len(leads), abs_path)
    return abs_path

"""JSON exporter for lead data."""

import json
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger("leadflow.exporter.json")


def export_json(
    leads: List[Dict[str, Any]],
    output_path: str = "data/leads.json",
    indent: int = 2,
) -> str:
    """Export leads to a JSON file.

    Args:
        leads: List of lead dictionaries to export.
        output_path: File path for the output JSON. Defaults to 'data/leads.json'.
        indent: JSON indentation level. Defaults to 2.

    Returns:
        The absolute path to the created JSON file.

    Raises:
        IOError: If the file cannot be written.
    """
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as jsonfile:
        json.dump(leads, jsonfile, indent=indent, ensure_ascii=False, default=str)

    abs_path = os.path.abspath(output_path)
    logger.info("Exported %d leads to JSON: %s", len(leads), abs_path)
    return abs_path

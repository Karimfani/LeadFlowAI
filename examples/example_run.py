#!/usr/bin/env python3
"""Example demonstrating the full LeadFlow AI pipeline.

Run this script to see LeadFlow AI in action:
    python examples/example_run.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from leadflow.config import setup_logging
from leadflow.collector import fetch_leads
from leadflow.scorer import score_leads
from leadflow.generator import generate_messages
from leadflow.exporter import export_csv, export_json
from leadflow.utils import format_lead_summary, filter_leads

logger = setup_logging("INFO")


def main():
    print("=" * 60)
    print("  LeadFlow AI — Example Run")
    print("=" * 60)

    KEYWORD = "restaurant"
    LOCATION = "Dubai"

    print(f"\n Step 1: Collecting leads for '{KEYWORD}' in '{LOCATION}'...")
    raw_leads = fetch_leads(KEYWORD, LOCATION)
    print(f"   Found {len(raw_leads)} leads.")

    print("\n Step 2: Scoring leads...")
    scored_leads = score_leads(raw_leads)

    print("\n Step 3: Filtering leads with score >= 3...")
    top_leads = filter_leads(scored_leads, min_score=3)
    print(f"   {len(top_leads)} leads passed the filter.")

    print("\n Step 4: Generating personalized outreach messages...")
    final_leads = generate_messages(top_leads, KEYWORD)

    print("\n Results:")
    print("-" * 60)
    for lead in final_leads:
        print(format_lead_summary(lead))
    print("-" * 60)

    if final_leads:
        print("\n First lead's outreach message:")
        print("-" * 60)
        print(final_leads[0]["message"])
        print("-" * 60)

    print("\n Step 5: Exporting results...")
    os.makedirs("data", exist_ok=True)
    csv_path = export_csv(final_leads, "data/example_leads.csv")
    json_path = export_json(final_leads, "data/example_leads.json")

    print(f"   CSV exported to: {csv_path}")
    print(f"   JSON exported to: {json_path}")

    print("\n Pipeline complete!")
    print(f"   Total leads processed: {len(final_leads)}")
    avg_score = sum(l["score"] for l in final_leads) / len(final_leads) if final_leads else 0
    print(f"   Average score: {avg_score:.1f}")
    print("=" * 60)


if __name__ == "__main__":
    main()

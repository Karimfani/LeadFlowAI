#!/usr/bin/env python3
"""LeadFlow AI Command Line Interface.

Usage:
    python cli/main.py --keyword "restaurant" --location "Dubai"
    python cli/main.py --keyword "dentist" --location "New York" --min-score 3
    python cli/main.py --keyword "gym" --location "London" --format json
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from leadflow.config import setup_logging
from leadflow.collector import fetch_leads
from leadflow.scorer import score_leads
from leadflow.generator import generate_messages
from leadflow.exporter import export_csv, export_json
from leadflow.utils import format_lead_summary, filter_leads


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="leadflow",
        description="LeadFlow AI — AI-powered lead generation tool for freelancers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli/main.py --keyword "restaurant" --location "Dubai"
  python cli/main.py --keyword "dentist" --location "New York" --min-score 3
  python cli/main.py --keyword "gym" --location "London" --format json --output data/gyms.json
        """,
    )
    parser.add_argument("--keyword", required=True, help="Business type to search (e.g. restaurant, dentist, gym)")
    parser.add_argument("--location", required=True, help="City or area to search in (e.g. Dubai, London)")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum lead score to include (default: 0)")
    parser.add_argument(
        "--format",
        choices=["csv", "json", "both"],
        default="csv",
        help="Export format (default: csv)",
    )
    parser.add_argument("--output", default=None, help="Output file path (auto-generated if not specified)")
    parser.add_argument("--no-messages", action="store_true", help="Skip message generation (faster)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser


def run_pipeline(
    keyword: str,
    location: str,
    min_score: int = 0,
    export_format: str = "csv",
    output_path: str = None,
    generate_msgs: bool = True,
    verbose: bool = False,
) -> list:
    """Run the full LeadFlow AI pipeline.

    Args:
        keyword: The business type to search.
        location: The city or area to search.
        min_score: Minimum score filter.
        export_format: 'csv', 'json', or 'both'.
        output_path: Custom output file path.
        generate_msgs: Whether to generate outreach messages.
        verbose: Enable verbose output.

    Returns:
        List of processed leads.
    """
    log_level = "DEBUG" if verbose else "INFO"
    logger = setup_logging(log_level)

    logger.info("Starting LeadFlow AI pipeline")
    logger.info("Keyword: %s | Location: %s", keyword, location)

    print(f"\n LeadFlow AI | Searching for '{keyword}' in '{location}'...")

    logger.debug("Collecting leads...")
    raw_leads = fetch_leads(keyword, location)
    print(f" Collected {len(raw_leads)} raw leads")

    logger.debug("Scoring leads...")
    scored_leads = score_leads(raw_leads)

    filtered = filter_leads(scored_leads, min_score=min_score)
    print(f" Scored and filtered to {len(filtered)} leads (min score: {min_score})")

    if generate_msgs:
        print(" Generating outreach messages...")
        final_leads = generate_messages(filtered, keyword)
    else:
        final_leads = filtered

    print("\n Results:")
    print("-" * 60)
    for lead in final_leads:
        print(format_lead_summary(lead))
    print("-" * 60)

    if not final_leads:
        print(" No leads matched the criteria.")
        return final_leads

    os.makedirs("data", exist_ok=True)
    base_name = f"data/{keyword.replace(' ', '_')}_{location.replace(' ', '_')}"

    if export_format in ("csv", "both"):
        csv_path = output_path if output_path and export_format == "csv" else f"{base_name}.csv"
        path = export_csv(final_leads, csv_path)
        print(f"\n Exported CSV → {path}")

    if export_format in ("json", "both"):
        json_path = output_path if output_path and export_format == "json" else f"{base_name}.json"
        path = export_json(final_leads, json_path)
        print(f" Exported JSON → {path}")

    print(f"\n Done! Processed {len(final_leads)} leads.")
    return final_leads


def main() -> None:
    """Main entry point for the CLI."""
    parser = build_parser()
    args = parser.parse_args()

    run_pipeline(
        keyword=args.keyword,
        location=args.location,
        min_score=args.min_score,
        export_format=args.format,
        output_path=args.output,
        generate_msgs=not args.no_messages,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()

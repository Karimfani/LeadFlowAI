# LeadFlow AI – AI-Powered Lead Generation Tool for Freelancers

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Stop hunting for clients manually. Let AI find them, score them, and write your outreach for you.

---

## The Problem

Freelancers spend hours every week manually searching for potential clients — scrolling Google Maps, copy-pasting contact info, writing the same outreach emails, and struggling to prioritize who to contact first.

It's inefficient, demoralizing, and takes time away from the actual work that pays the bills.

## The Solution

**LeadFlow AI** is an open-source Python tool that automates the entire lead generation pipeline:

1. **Collect** — Find businesses by keyword and location
2. **Score** — Intelligently rank leads by conversion potential
3. **Message** — Generate personalized outreach messages using AI
4. **Export** — Save results to CSV or JSON for your workflow

No paid subscriptions. No dashboards you'll never use. Just a clean, powerful tool that runs from your terminal.

---

## Features

- **Smart Lead Scoring** — Ranks leads by conversion potential (rating, online presence, and more)
- **AI-Powered Messages** — Generates personalized outreach using OpenAI GPT (with a high-quality template fallback)
- **Flexible Export** — CSV and JSON exporters for any workflow
- **CLI Interface** — Run the full pipeline from your terminal in seconds
- **REST API** — FastAPI-powered API for integration into your own tools
- **Configurable Rules** — Customize scoring logic to match your target market
- **Zero Required API Keys** — Works fully offline with mock data (real integrations optional)

---

## Installation

### Prerequisites

- Python 3.11+
- pip

### Quick Start

```bash
git clone https://github.com/yourusername/leadflow-ai.git
cd leadflow-ai
pip install -r requirements.txt
```

### Optional: Enable AI Messages

Add your OpenAI key to `.env`:

```bash
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here
```

---

## Usage

### CLI

```bash
# Basic usage
python cli/main.py --keyword "restaurant" --location "Dubai"

# With score filter
python cli/main.py --keyword "dentist" --location "New York" --min-score 3

# Export as JSON
python cli/main.py --keyword "gym" --location "London" --format json

# Export both CSV and JSON
python cli/main.py --keyword "cafe" --location "Paris" --format both

# Skip message generation (faster)
python cli/main.py --keyword "barber" --location "Tokyo" --no-messages

# Verbose mode
python cli/main.py --keyword "salon" --location "Berlin" --verbose
```

**Output example:**

```
 LeadFlow AI | Searching for 'restaurant' in 'Dubai'...
 Collected 10 raw leads
 Scored and filtered to 6 leads (min score: 0)
 Generating outreach messages...

 Results:
------------------------------------------------------------
[Score: 5] Al Baik Restaurant | Rating: 4.7 | no website | +971-4-555-0101
[Score: 5] Peak Fitness Studio | Rating: 4.6 | no website | +971-4-555-0109
[Score: 4] Golden Spice Kitchen | Rating: 4.5 | no website | +971-4-555-0103
------------------------------------------------------------

 Exported CSV → /path/to/data/restaurant_Dubai.csv
```

### Python API

```python
from leadflow.collector import fetch_leads
from leadflow.scorer import score_leads
from leadflow.generator import generate_messages
from leadflow.exporter import export_csv

# Collect leads
leads = fetch_leads("restaurant", "Dubai")

# Score them
scored = score_leads(leads)

# Generate messages
final = generate_messages(scored, "restaurant")

# Export
export_csv(final, "data/my_leads.csv")
```

### REST API

Start the API server:

```bash
uvicorn api.app:app --reload
```

#### Generate leads

```bash
curl -X POST http://localhost:8000/leads \
  -H "Content-Type: application/json" \
  -d '{"keyword": "restaurant", "location": "Dubai"}'
```

#### Search leads (GET)

```bash
curl "http://localhost:8000/leads?keyword=dentist&location=NYC&min_score=3"
```

**Response:**

```json
[
  {
    "name": "Al Baik Restaurant",
    "rating": 4.7,
    "has_website": false,
    "contact": "+971-4-555-0101",
    "score": 5,
    "message": "Hi Al Baik Restaurant,\n\nI came across your restaurant..."
  }
]
```

**Interactive API docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Scoring System

Leads are scored based on configurable rules in `leadflow/config.py`:

| Rule | Points | Rationale |
|------|--------|-----------|
| Rating ≥ 4.3 | +2 | Trusted by customers, worth contacting |
| No website | +2 | Biggest opportunity — needs online presence |
| Rating ≥ 4.0 | +1 | Above-average business |

**Score 5** = Hot lead. Contact immediately.
**Score 3-4** = Good lead. Prioritize this week.
**Score 1-2** = Cold lead. Contact if time permits.

Customize rules by editing `SCORING_RULES` in `leadflow/config.py`.

---

## Screenshots

```
[CLI Screenshot - Running pipeline for "restaurant" in "Dubai"]
[API Docs Screenshot - FastAPI interactive documentation]
[Export Screenshot - Generated CSV file in data/ directory]
```

*(Screenshots will be added in v1.1)*

---

## Running Tests

```bash
pytest tests/ -v
```

Expected output:

```
PASSED tests/test_pipeline.py::TestLeadScorer::test_score_high_rating_no_website
PASSED tests/test_pipeline.py::TestLeadScorer::test_scores_sorted_descending
PASSED tests/test_pipeline.py::TestLeadCollector::test_fetch_leads_returns_list
PASSED tests/test_pipeline.py::TestMessageGenerator::test_message_contains_name
PASSED tests/test_pipeline.py::TestFullPipeline::test_full_pipeline
...
```

---

## Project Structure

```
leadflow-ai/
├── leadflow/                  # Core library
│   ├── config.py              # Configuration and scoring rules
│   ├── collector/             # Lead collection
│   │   ├── mock_data.py       # Mock data (default)
│   │   └── google_maps.py     # Google Maps placeholder
│   ├── scorer/                # Lead scoring engine
│   │   └── lead_scorer.py
│   ├── generator/             # Message generation
│   │   └── message_generator.py  # Template + OpenAI fallback
│   ├── exporter/              # Data exporters
│   │   ├── csv_exporter.py
│   │   └── json_exporter.py
│   └── utils/                 # Helpers and utilities
│       └── helpers.py
├── cli/                       # Command-line interface
│   └── main.py
├── api/                       # FastAPI REST server
│   └── app.py
├── tests/                     # Pytest test suite
│   └── test_pipeline.py
├── examples/                  # Example scripts
│   └── example_run.py
├── data/                      # Output directory
├── .env.example               # Environment variable template
├── requirements.txt
└── setup.py
```

---

## Roadmap

- [ ] **v1.1** — Real Google Maps Places API integration
- [ ] **v1.2** — LinkedIn lead discovery
- [ ] **v1.3** — Email sequence automation
- [ ] **v1.4** — Lead CRM with SQLite persistence
- [ ] **v1.5** — Slack/Telegram notification bot
- [ ] **v2.0** — Web dashboard with analytics

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes with tests
4. Run the test suite: `pytest tests/`
5. Submit a pull request

Please follow the existing code style:
- Type hints on all functions
- Docstrings on all public functions
- No hardcoded values (use `config.py`)

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built with ❤️ for the freelancer community. If this tool helps you land clients, consider starring the repo and sharing it with other freelancers.

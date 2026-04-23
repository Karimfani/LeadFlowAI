"""Tests for the LeadFlow AI pipeline.

Run with:
    pytest tests/
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from leadflow.collector import fetch_leads
from leadflow.scorer import score_lead, score_leads
from leadflow.generator import generate_message
from leadflow.exporter import export_csv, export_json
from leadflow.utils import filter_leads, sort_leads, format_lead_summary


class TestLeadScorer:
    """Tests for the lead scoring engine."""

    def test_score_high_rating_no_website(self):
        """A lead with a high rating and no website should score 5."""
        lead = {"name": "Test Biz", "rating": 4.5, "has_website": False}
        assert score_lead(lead) == 5

    def test_score_high_rating_with_website(self):
        """A lead with a high rating but a website should score 3."""
        lead = {"name": "Test Biz", "rating": 4.5, "has_website": True}
        assert score_lead(lead) == 3

    def test_score_low_rating_no_website(self):
        """A lead with a low rating and no website should score 2."""
        lead = {"name": "Test Biz", "rating": 3.5, "has_website": False}
        assert score_lead(lead) == 2

    def test_score_low_rating_with_website(self):
        """A lead with a low rating and a website should score 0."""
        lead = {"name": "Test Biz", "rating": 3.0, "has_website": True}
        assert score_lead(lead) == 0

    def test_score_boundary_rating(self):
        """Rating of exactly 4.3 should trigger high_rating_points."""
        lead = {"name": "Test Biz", "rating": 4.3, "has_website": True}
        score = score_lead(lead)
        assert score >= 2

    def test_scores_sorted_descending(self):
        """score_leads should return leads sorted by score descending."""
        leads = [
            {"name": "Low", "rating": 3.0, "has_website": True},
            {"name": "High", "rating": 4.8, "has_website": False},
            {"name": "Mid", "rating": 4.1, "has_website": False},
        ]
        scored = score_leads(leads)
        scores = [l["score"] for l in scored]
        assert scores == sorted(scores, reverse=True)


class TestLeadCollector:
    """Tests for the lead collector."""

    def test_fetch_leads_returns_list(self):
        """fetch_leads should return a non-empty list."""
        leads = fetch_leads("restaurant", "Dubai")
        assert isinstance(leads, list)
        assert len(leads) > 0

    def test_lead_structure(self):
        """Each lead should have required fields."""
        leads = fetch_leads("cafe", "London")
        for lead in leads:
            assert "name" in lead
            assert "rating" in lead
            assert "has_website" in lead
            assert "contact" in lead

    def test_lead_types(self):
        """Lead fields should have correct types."""
        leads = fetch_leads("gym", "NYC")
        for lead in leads:
            assert isinstance(lead["name"], str)
            assert isinstance(lead["rating"], float)
            assert isinstance(lead["has_website"], bool)
            assert isinstance(lead["contact"], str)


class TestMessageGenerator:
    """Tests for the message generator."""

    def test_generate_message_returns_string(self):
        """generate_message should return a non-empty string."""
        lead = {"name": "Test Biz", "rating": 4.5, "has_website": False}
        message = generate_message(lead, "restaurant")
        assert isinstance(message, str)
        assert len(message) > 0

    def test_message_contains_name(self):
        """Message should mention the business name."""
        lead = {"name": "Dragon Palace", "rating": 4.5, "has_website": False}
        message = generate_message(lead, "restaurant")
        assert "Dragon Palace" in message

    def test_message_contains_rating(self):
        """Message should reference the rating."""
        lead = {"name": "Test Biz", "rating": 4.7, "has_website": False}
        message = generate_message(lead, "restaurant")
        assert "4.7" in message

    def test_no_website_pitch_in_message(self):
        """Message should mention online presence for businesses without a website."""
        lead = {"name": "Test Biz", "rating": 4.5, "has_website": False}
        message = generate_message(lead, "restaurant")
        assert any(phrase in message.lower() for phrase in ["online", "website", "presence"])


class TestFullPipeline:
    """End-to-end pipeline integration tests."""

    def test_full_pipeline(self):
        """The full collect → score → message pipeline should work end to end."""
        from leadflow.scorer import score_leads
        from leadflow.generator import generate_messages

        raw = fetch_leads("restaurant", "Dubai")
        scored = score_leads(raw)
        final = generate_messages(scored, "restaurant")

        assert len(final) > 0
        for lead in final:
            assert "score" in lead
            assert "message" in lead
            assert isinstance(lead["score"], int)
            assert isinstance(lead["message"], str)

    def test_export_csv(self, tmp_path):
        """export_csv should create a valid CSV file."""
        leads = [{"name": "Test", "rating": 4.5, "has_website": False, "contact": "123", "score": 4, "message": "Hi"}]
        csv_path = str(tmp_path / "test.csv")
        result_path = export_csv(leads, csv_path)
        assert os.path.exists(result_path)

        with open(result_path) as f:
            content = f.read()
        assert "name" in content
        assert "Test" in content

    def test_export_json(self, tmp_path):
        """export_json should create a valid JSON file."""
        import json
        leads = [{"name": "Test", "rating": 4.5, "has_website": False, "contact": "123", "score": 4, "message": "Hi"}]
        json_path = str(tmp_path / "test.json")
        result_path = export_json(leads, json_path)
        assert os.path.exists(result_path)

        with open(result_path) as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["name"] == "Test"


class TestUtils:
    """Tests for utility helpers."""

    def test_filter_by_min_score(self):
        """filter_leads should return only leads meeting the minimum score."""
        leads = [{"score": 1}, {"score": 3}, {"score": 5}]
        filtered = filter_leads(leads, min_score=3)
        assert all(l["score"] >= 3 for l in filtered)

    def test_sort_leads(self):
        """sort_leads should sort by the given field."""
        leads = [{"score": 3}, {"score": 1}, {"score": 5}]
        sorted_leads = sort_leads(leads, by="score")
        assert sorted_leads[0]["score"] == 5

    def test_format_lead_summary(self):
        """format_lead_summary should return a non-empty string."""
        lead = {"name": "Test", "rating": 4.5, "has_website": False, "contact": "123", "score": 4}
        summary = format_lead_summary(lead)
        assert "Test" in summary
        assert "4.5" in summary

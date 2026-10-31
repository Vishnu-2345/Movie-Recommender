"""Tests for TMDB client and enrichment logic."""
import unittest
from src.tmdb_client import TMDBClient


class TestTMDBClient(unittest.TestCase):
    """Test suite for TMDBClient."""

    def setUp(self):
        # Client without API key to test fallback and sample data enrichment
        self.client = TMDBClient(api_key="")

    def test_sample_enrichment_finds_zodiac(self):
        movie = self.client.enrich_movie(
            title="Zodiac",
            year=2007,
            ai_rationale="Rainy detective investigation",
            vibe_tags=["Rainy City", "Slow-burn"],
            match_score=97
        )

        self.assertEqual(movie["title"], "Zodiac")
        self.assertEqual(movie["year"], 2007)
        self.assertIsNotNone(movie["poster_url"])
        self.assertIn("David Fincher", movie["director"])
        self.assertEqual(movie["match_score"], 97)
        self.assertIsNotNone(movie["trailer_key"])

    def test_unknown_movie_synthetic_fallback(self):
        movie = self.client.enrich_movie(
            title="Nonexistent Indie Film 2029",
            year=2029,
            ai_rationale="Hypothetical recommendation",
            vibe_tags=["Indie", "Experimental"],
            match_score=85
        )

        self.assertEqual(movie["title"], "Nonexistent Indie Film 2029")
        self.assertEqual(movie["year"], 2029)
        self.assertIsNotNone(movie["poster_url"])
        self.assertEqual(movie["match_score"], 85)


if __name__ == "__main__":
    unittest.main()

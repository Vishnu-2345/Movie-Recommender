"""Tests for the AI Recommender engine."""
import unittest
from src.recommender import AIRecommender


class TestAIRecommender(unittest.TestCase):
    """Test suite for AIRecommender."""

    def setUp(self):
        self.recommender = AIRecommender()

    def test_empty_prompt_returns_gracefully(self):
        result = self.recommender.recommend("")
        self.assertEqual(len(result["recommended_movies"]), 0)

    def test_heuristic_fallback_returns_expected_structure(self):
        prompt = "A cozy, slow-burn mystery set in a rainy city that makes me feel like a detective."
        result = self.recommender.recommend(prompt, num_movies=3)

        self.assertIn("search_summary", result)
        self.assertIn("recommended_movies", result)
        movies = result["recommended_movies"]
        self.assertEqual(len(movies), 3)

        for m in movies:
            self.assertIn("title", m)
            self.assertIn("year", m)
            self.assertIn("vibe_tags", m)
            self.assertIn("match_rationale", m)
            self.assertIn("match_score", m)
            self.assertGreaterEqual(m["match_score"], 80)

    def test_json_extractor_handles_markdown_blocks(self):
        raw_llm_output = """
        ```json
        {
            "search_summary": "Cyberpunk vibes",
            "recommended_movies": [
                {
                    "title": "Blade Runner 2049",
                    "year": 2017,
                    "vibe_tags": ["Neon", "Synth"],
                    "match_rationale": "Perfect visual tone.",
                    "match_score": 95
                }
            ]
        }
        ```
        """
        parsed = self.recommender._extract_json(raw_llm_output)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["search_summary"], "Cyberpunk vibes")
        self.assertEqual(len(parsed["recommended_movies"]), 1)


if __name__ == "__main__":
    unittest.main()

"""AI Recommendation Engine: Translates natural language prompts into movie suggestions."""
import json
import re
from typing import Dict, Any, List, Optional
from src.config import Config
from src.sample_data import SAMPLE_MOVIES


SYSTEM_PROMPT = """You are CineMind, an expert cinematic curator and film critic with encyclopedic knowledge of cinema.
The user will provide a natural language mood, aesthetic, storyline vibe, or emotional prompt (for example: "A cozy, slow-burn mystery set in a rainy city that makes me feel like a detective").

Your task is to analyze the emotional nuance, visual tone, setting, and pacing, and recommend movies that truly embody that exact feeling.

Return ONLY a valid JSON object matching this exact format, with NO Markdown backticks, NO commentary, and NO explanations outside the JSON:
{
  "search_summary": "A 1-2 sentence atmospheric analysis describing the user's requested vibe and themes.",
  "recommended_movies": [
    {
      "title": "Exact Title of Movie",
      "year": 2007,
      "vibe_tags": ["Atmospheric", "Rain-slicked", "Methodical Pacing", "Obsession"],
      "match_rationale": "2-3 sentences explaining precisely why this film matches the mood, atmosphere, and specific details requested.",
      "match_score": 96
    }
  ]
}

Guidelines:
1. Provide between 3 and 8 distinct, high-quality movie recommendations as requested.
2. Ensure titles are accurate real movies.
3. Keep match_score between 80 and 99.
4. vibe_tags should be short (1-3 words) highlighting aesthetics, tone, or specific settings.
5. In match_rationale, cite specific elements (cinematography, mood, pacing, characters) that connect to the user's prompt.
"""


class AIRecommender:
    """Orchestrates LLM calls to generate tailored film recommendations."""

    def __init__(self, gemini_key: Optional[str] = None, openai_key: Optional[str] = None):
        self.gemini_key = Config.get_gemini_key(gemini_key or "")
        self.openai_key = Config.get_openai_key(openai_key or "")

    @property
    def has_ai_key(self) -> bool:
        """Returns True if at least one AI provider is configured."""
        return bool(self.gemini_key or self.openai_key)

    def recommend(
        self,
        prompt: str,
        num_movies: int = 5,
        era_filter: Optional[str] = None,
        min_rating: float = 0.0
    ) -> Dict[str, Any]:
        """Main recommendation entrypoint."""
        cleaned_prompt = prompt.strip()
        if not cleaned_prompt:
            return {
                "search_summary": "Please enter a mood, vibe, or plot description to get recommendations.",
                "recommended_movies": []
            }

        # Build prompt instructions with any filters
        augmented_prompt = f"User Request: \"{cleaned_prompt}\"\n\nDesired number of recommendations: {num_movies}."
        if era_filter and era_filter != "Any Era":
            augmented_prompt += f"\nFilter preference: Must fit era: {era_filter}."
        if min_rating > 0:
            augmented_prompt += f"\nMinimum rating criteria: High acclaim or minimum ~{min_rating}/10."

        # 1. Try Google Gemini if key available
        if self.gemini_key:
            gemini_result = self._call_gemini(augmented_prompt)
            if gemini_result and gemini_result.get("recommended_movies"):
                return gemini_result

        # 2. Try OpenAI if key available
        if self.openai_key:
            openai_result = self._call_openai(augmented_prompt)
            if openai_result and openai_result.get("recommended_movies"):
                return openai_result

        # 3. Fallback to smart heuristic matcher for demo / offline experience
        return self._heuristic_fallback(cleaned_prompt, num_movies)

    def _call_gemini(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Call Google Gemini using google.genai or google.generativeai."""
        # Try modern google.genai SDK
        try:
            from google import genai
            client = genai.Client(api_key=self.gemini_key)
            full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            if response and response.text:
                parsed = self._extract_json(response.text)
                if parsed and "recommended_movies" in parsed:
                    return parsed
        except Exception:
            pass

        # Try fallback model or legacy SDK
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=self.gemini_key)
            model = legacy_genai.GenerativeModel("gemini-1.5-flash")
            full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
            res = model.generate_content(full_prompt)
            if res and res.text:
                parsed = self._extract_json(res.text)
                if parsed and "recommended_movies" in parsed:
                    return parsed
        except Exception:
            pass

        return None

    def _call_openai(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Call OpenAI API if configured."""
        try:
            import requests
            headers = {
                "Authorization": f"Bearer {self.openai_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "response_format": {"type": "json_object"}
            }
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=15
            )
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                return self._extract_json(content)
        except Exception:
            pass

        return None

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract and parse JSON safely from LLM output."""
        if not text:
            return None
        # Remove markdown fences if present
        cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
        cleaned = re.sub(r"\s*```$", "", cleaned.strip(), flags=re.MULTILINE)
        
        # Try direct parse
        try:
            return json.loads(cleaned)
        except Exception:
            pass

        # Find first { and last }
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(cleaned[start:end+1])
            except Exception:
                pass
                
        return None

    def _heuristic_fallback(self, prompt: str, num_movies: int = 5) -> Dict[str, Any]:
        """Intelligent semantic keyword matcher over sample database when no key is set."""
        query = prompt.lower()
        scored_movies: List[tuple[int, Dict[str, Any]]] = []

        # Keywords mapping to movie traits
        theme_weights = {
            "rain": ["Zodiac", "Se7en", "Blade Runner 2049", "The Batman"],
            "mystery": ["Knives Out", "Zodiac", "Se7en", "Shutter Island", "Arrival"],
            "detective": ["Zodiac", "Se7en", "Blade Runner 2049", "Knives Out", "The Dark Knight"],
            "cozy": ["Knives Out", "Spirited Away", "The Secret Life of Walter Mitty", "Forrest Gump"],
            "sci-fi": ["Interstellar", "Arrival", "Blade Runner 2049", "The Matrix", "Ex Machina", "Inception"],
            "space": ["Interstellar", "Arrival", "Thor: Ragnarok"],
            "mind": ["Inception", "Arrival", "Shutter Island", "The Matrix", "Ex Machina"],
            "twist": ["Shutter Island", "Get Out", "Parasite", "Inception", "Se7en"],
            "dark": ["Se7en", "The Dark Knight", "Zodiac", "Parasite", "Get Out"],
            "cyberpunk": ["Blade Runner 2049", "The Matrix"],
            "synth": ["Blade Runner 2049", "Thor: Ragnarok", "The Matrix"],
            "feel good": ["Forrest Gump", "The Intouchables", "The Secret Life of Walter Mitty", "Spirited Away"],
            "whimsical": ["Spirited Away", "The Secret Life of Walter Mitty"],
            "horror": ["Get Out", "A Quiet Place", "Se7en"],
            "tense": ["A Quiet Place", "Parasite", "Get Out", "Zodiac"],
            "heist": ["Inception", "The Dark Knight"]
        }

        for movie in SAMPLE_MOVIES:
            score = 70  # Baseline
            movie_text = f"{movie['title']} {movie['overview']} {' '.join(movie['genres'])} {' '.join(movie['vibe_tags'])}".lower()

            # Direct word overlap
            for word in query.split():
                if len(word) > 3 and word in movie_text:
                    score += 8

            # Theme associations
            for trigger, favored_titles in theme_weights.items():
                if trigger in query:
                    if movie["title"] in favored_titles:
                        score += 15

            scored_movies.append((score, movie))

        # Sort descending by score
        scored_movies.sort(key=lambda x: x[0], reverse=True)
        selected = scored_movies[:num_movies]

        recommendations = []
        for score, m in selected:
            # Construct tailored rationale
            rationale = (
                f"Selected for its atmospheric alignment with '{prompt}'. "
                f"Features {', '.join(m['vibe_tags'][:3])} which mirror the specific tone and pace of your search."
            )
            recommendations.append({
                "title": m["title"],
                "year": m["year"],
                "vibe_tags": m["vibe_tags"][:4],
                "match_rationale": rationale,
                "match_score": min(98, max(82, score))
            })

        return {
            "search_summary": f"Curated selections capturing the essence of: \"{prompt}\"",
            "recommended_movies": recommendations
        }

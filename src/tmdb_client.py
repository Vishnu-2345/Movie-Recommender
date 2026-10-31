"""TMDB API Client for fetching rich movie metadata, posters, trailers, and streaming options."""
from typing import Dict, Any, Optional, List
import requests
from src.config import Config
from src.sample_data import SAMPLE_MOVIES


class TMDBClient:
    """Client for interacting with The Movie Database (TMDB) API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = Config.get_tmdb_key(api_key or "")
        self.base_url = Config.TMDB_BASE_URL
        self.headers = {
            "Accept": "application/json"
        }
        # Check if the key provided is a v4 Read Access Token (starts with eyJ...) or a v3 32-char hex key
        if self.api_key and len(self.api_key) > 50:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
            self.auth_param = {}
        elif self.api_key:
            self.auth_param = {"api_key": self.api_key}
        else:
            self.auth_param = {}

    @property
    def is_configured(self) -> bool:
        """Return True if an API key is available."""
        return bool(self.api_key)

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Internal helper for making TMDB GET requests with error handling."""
        if not self.is_configured:
            return None
            
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        combined_params = {**self.auth_param, **(params or {})}
        
        try:
            resp = requests.get(url, params=combined_params, headers=self.headers, timeout=8)
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception:
            return None

    def search_movie(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Search for a movie by title and optional release year."""
        params = {"query": title, "include_adult": False}
        if year:
            params["year"] = year
            
        data = self._get("search/movie", params)
        if data and data.get("results"):
            return data["results"][0]
        
        # Fallback search without year if year-filtered search had no hits
        if year:
            params.pop("year")
            data = self._get("search/movie", params)
            if data and data.get("results"):
                return data["results"][0]
                
        return None

    def get_details(self, movie_id: int) -> Optional[Dict[str, Any]]:
        """Fetch detailed information for a movie."""
        return self._get(f"movie/{movie_id}")

    def get_trailer_key(self, movie_id: int) -> Optional[str]:
        """Fetch official YouTube trailer key for a movie."""
        data = self._get(f"movie/{movie_id}/videos")
        if not data or not data.get("results"):
            return None
            
        videos = data.get("results", [])
        
        # 1. Look for official YouTube trailers
        for video in videos:
            if video.get("site") == "YouTube" and video.get("type") == "Trailer" and video.get("official"):
                return video.get("key")
                
        # 2. Look for any YouTube trailer
        for video in videos:
            if video.get("site") == "YouTube" and video.get("type") == "Trailer":
                return video.get("key")
                
        # 3. Look for teasers / clips
        for video in videos:
            if video.get("site") == "YouTube":
                return video.get("key")
                
        return None

    def get_watch_providers(self, movie_id: int, region: str = "US") -> List[str]:
        """Fetch streaming platforms for a movie in a specific country/region."""
        data = self._get(f"movie/{movie_id}/watch/providers")
        if not data or not data.get("results"):
            return []
            
        region_data = data["results"].get(region.upper())
        if not region_data:
            # Fallback to US if specific region not found
            region_data = data["results"].get("US", {})
            
        providers = []
        # Priority on flatrate (subscription streaming), then free/ads
        for stream in region_data.get("flatrate", []):
            name = stream.get("provider_name")
            if name and name not in providers:
                providers.append(name)
                
        for stream in region_data.get("free", []):
            name = stream.get("provider_name")
            if name and name not in providers:
                providers.append(name)
                
        return providers[:4]

    def get_credits(self, movie_id: int) -> Dict[str, Any]:
        """Fetch director and top cast for a movie."""
        data = self._get(f"movie/{movie_id}/credits")
        if not data:
            return {"director": "Unknown", "cast": []}
            
        director = "Unknown"
        for crew in data.get("crew", []):
            if crew.get("job") == "Director":
                director = crew.get("name", "Unknown")
                break
                
        cast = [actor.get("name") for actor in data.get("cast", [])[:4] if actor.get("name")]
        return {"director": director, "cast": cast}

    def enrich_movie(
        self,
        title: str,
        year: Optional[int] = None,
        ai_rationale: str = "",
        vibe_tags: Optional[List[str]] = None,
        match_score: int = 90
    ) -> Dict[str, Any]:
        """Search and assemble all metadata for a movie recommendation."""
        # 1. Try finding in sample database first if offline
        sample_match = self._find_in_sample(title)
        
        # 2. If TMDB is configured, query TMDB live API
        if self.is_configured:
            search_res = self.search_movie(title, year)
            if search_res:
                movie_id = search_res.get("id")
                details = self.get_details(movie_id) or search_res
                credits_info = self.get_credits(movie_id)
                trailer_key = self.get_trailer_key(movie_id)
                providers = self.get_watch_providers(movie_id)
                
                poster_path = details.get("poster_path")
                full_poster = (
                    f"{Config.TMDB_IMAGE_BASE_URL}{poster_path}"
                    if poster_path else
                    (f"{Config.TMDB_IMAGE_BASE_URL}{sample_match.get('poster_path')}" if sample_match else None)
                )
                
                backdrop_path = details.get("backdrop_path")
                full_backdrop = (
                    f"{Config.TMDB_BACKDROP_BASE_URL}{backdrop_path}"
                    if backdrop_path else None
                )
                
                release_date = details.get("release_date", "")
                resolved_year = int(release_date.split("-")[0]) if release_date and "-" in release_date else (year or 2020)
                
                genres = [g.get("name") for g in details.get("genres", []) if g.get("name")]
                if not genres and sample_match:
                    genres = sample_match.get("genres", [])

                return {
                    "id": movie_id,
                    "title": details.get("title", title),
                    "year": resolved_year,
                    "overview": details.get("overview", sample_match.get("overview", "") if sample_match else ""),
                    "poster_url": full_poster,
                    "backdrop_url": full_backdrop,
                    "vote_average": round(details.get("vote_average", 7.5), 1),
                    "vote_count": details.get("vote_count", 1000),
                    "runtime": details.get("runtime") or (sample_match.get("runtime", 120) if sample_match else 120),
                    "genres": genres or ["Drama"],
                    "director": credits_info.get("director", sample_match.get("director", "Unknown") if sample_match else "Unknown"),
                    "cast": credits_info.get("cast") or (sample_match.get("cast", []) if sample_match else []),
                    "trailer_key": trailer_key or (sample_match.get("trailer_key") if sample_match else None),
                    "streaming": providers or (sample_match.get("streaming", []) if sample_match else ["Check JustWatch"]),
                    "ai_rationale": ai_rationale,
                    "vibe_tags": vibe_tags or ["Atmospheric"],
                    "match_score": match_score
                }

        # 3. Fallback to sample match if found
        if sample_match:
            poster_path = sample_match.get("poster_path")
            full_poster = f"{Config.TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None
            return {
                "id": sample_match.get("id"),
                "title": sample_match.get("title"),
                "year": sample_match.get("year"),
                "overview": sample_match.get("overview"),
                "poster_url": full_poster,
                "backdrop_url": f"{Config.TMDB_BACKDROP_BASE_URL}{sample_match.get('backdrop_path')}",
                "vote_average": sample_match.get("vote_average"),
                "vote_count": sample_match.get("vote_count"),
                "runtime": sample_match.get("runtime"),
                "genres": sample_match.get("genres"),
                "director": sample_match.get("director"),
                "cast": sample_match.get("cast"),
                "trailer_key": sample_match.get("trailer_key"),
                "streaming": sample_match.get("streaming"),
                "ai_rationale": ai_rationale or f"Matches your requested atmosphere and tone.",
                "vibe_tags": vibe_tags or sample_match.get("vibe_tags", []),
                "match_score": match_score
            }

        # 4. Generic synthetic fallback
        return {
            "id": 999999,
            "title": title,
            "year": year or 2022,
            "overview": "A compelling film that mirrors the emotional resonance, visual styling, and tone of your prompt.",
            "poster_url": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=500&q=80",
            "backdrop_url": None,
            "vote_average": 7.8,
            "vote_count": 2500,
            "runtime": 118,
            "genres": ["Drama", "Mystery"],
            "director": "Acclaimed Director",
            "cast": ["Ensemble Cast"],
            "trailer_key": None,
            "streaming": ["Apple TV", "Prime Video"],
            "ai_rationale": ai_rationale or "Curated based on thematic alignment with your query.",
            "vibe_tags": vibe_tags or ["Cinematic", "Recommended"],
            "match_score": match_score
        }

    def _find_in_sample(self, title: str) -> Optional[Dict[str, Any]]:
        """Look for title match in curated offline database."""
        clean_target = title.lower().strip()
        for movie in SAMPLE_MOVIES:
            if clean_target in movie["title"].lower() or movie["title"].lower() in clean_target:
                return movie
        return None

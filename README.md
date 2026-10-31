# 🎬 CineMind AI — Mood & Vibe-Driven Movie Recommender

> **Next-generation cinematic discovery powered by Natural Language AI.**  
> Instead of generic genre filters, CineMind understands mood, atmosphere, narrative depth, and specific emotional cravings like *"A cozy, slow-burn mystery set in a rainy city that makes me feel like a detective."*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4.svg)](https://aistudio.google.com/)
[![TMDB API](https://img.shields.io/badge/Data-TMDB%20v3-01b4e4.svg)](https://www.themoviedb.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🛠️ Core Architecture

CineMind connects three distinct layers into a seamless, cinema-grade experience:

```
┌─────────────────────────────────────────────────────────────┐
│                       1. FRONTEND / UI                      │
│   Streamlit Glassmorphic Dark UI (Posters, Badges, Trailers)│
└──────────────────────────────┬──────────────────────────────┘
                               │ Natural Language Prompt
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 2. AI BRAIN (LLM REASONER)                  │
│       Google Gemini (gemini-1.5-flash / gemini-2.5-flash)   │
│       Extracts mood, cinematography, pacing & real films    │
└──────────────────────────────┬──────────────────────────────┘
                               │ Movie Titles & AI Rationale
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               3. MOVIE DATABASE (CONTENT & MEDIA)           │
│                    The Movie Database (TMDB)                │
│    HD Posters, Trailers, TMDB Scores, Streaming Providers   │
└─────────────────────────────────────────────────────────────┘
```

1. **Frontend / UI (`Streamlit + Custom CSS`)**:
   - Modern obsidian/indigo cinema theme with glassmorphism.
   - Dynamic movie cards featuring match confidence badges, vibe tags, ratings, and director/cast credits.
   - Embedded official YouTube trailers and streaming platform badges (Netflix, Prime, Max, Disney+).
   - Interactive personal **Watchlist** to save movies during the session.

2. **AI Brain (`Google Gemini / OpenAI`)**:
   - Translates open-ended emotional prompts into structured JSON recommendations.
   - Delivers bespoke justifications explaining *why* each movie matches the user's specific mood, pacing, and visual style.
   - Built-in heuristic offline fallback engine ensures immediate out-of-the-box functionality even without API keys.

3. **Movie Database API (`TMDB v3`)**:
   - Searches and enriches recommendations with real-time metadata.
   - Fetches high-definition poster paths, vote averages, runtime, certification, and localized watch providers.

---

## ✨ Key Features

- 🌧️ **Natural Language Understanding**: Enter any vibe, aesthetic, or obscure feeling.
- 🎯 **AI Match Breakdown**: Understand why each movie was selected (atmosphere, pacing, themes).
- 📺 **Official YouTube Trailers**: Watch trailers directly in the app without leaving the page.
- 🏷️ **Streaming Availability**: Discover where to stream or rent (Netflix, Prime Video, Apple TV, Max).
- 🎛️ **Granular Controls**: Filter by release era (80s, 90s, 2000s, Modern), minimum score, and recommendation count.
- 📌 **Interactive Watchlist**: Save favorites for later with persistent session storage.
- ⚡ **Zero-Setup Demo Mode**: Runs immediately with rich curated data, even before configuring API keys!

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Vishnu-2345/Movie-Recommender.git
cd Movie-Recommender
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure API Keys
Create a `.env` file in the root directory (or enter keys directly in the app's sidebar):
```bash
cp .env.example .env
```
Edit `.env` with your keys:
```env
# Free key from Google AI Studio: https://aistudio.google.com/
GEMINI_API_KEY=your_gemini_api_key_here

# Free key from The Movie Database: https://www.themoviedb.org/settings/api
TMDB_API_KEY=your_tmdb_api_key_here
```
> *Note: If you run without API keys, CineMind activates **Smart Demo Mode**, providing curated recommendations and full trailer playback immediately.*

### 5. Launch the Application
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## 🧪 Running Unit Tests

Run the test suite to verify prompt parsing, heuristic fallbacks, and TMDB enrichment:
```bash
python -m unittest discover -s tests
```

---

## 💡 Example Prompts to Try

- 🌧️ *"Give me a cozy, slow-burn mystery set in a rainy city that makes me feel like a detective."*
- 🚀 *"Mind-bending sci-fi with philosophical questions about time and human existence like Interstellar or Arrival."*
- 🌆 *"A stylish, neon-soaked cyberpunk thriller with synth music and an existential protagonist."*
- 🏰 *"A cozy autumn whodunit set in an old quirky mansion with eccentric family members."*
- 🌀 *"A claustrophobic psychological thriller with an isolated setting and a shocking final twist."*
- 💛 *"A heartwarming, whimsical story of unlikely friendship and wonder."*

---

## 📁 Project Structure

```
Movie-Recommender/
│
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Python dependencies
├── .env.example                # Template for API keys
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
│
├── src/
│   ├── __init__.py
│   ├── config.py               # Central environment configuration
│   ├── recommender.py          # LLM Brain (Gemini / OpenAI / Heuristic fallback)
│   ├── tmdb_client.py          # TMDB API client (Posters, Trailers, Watch Providers)
│   ├── sample_data.py          # Curated offline database for instant demo mode
│   └── styles.py               # Custom dark-theme CSS & HTML card renderer
│
└── tests/
    ├── __init__.py
    ├── test_recommender.py     # Tests for AI engine & JSON parsing
    └── test_tmdb_client.py     # Tests for movie enrichment & fallback behavior
```

---

## 🌐 Deployment Options

### Streamlit Community Cloud (Recommended)
1. Push your repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your repository, specify `app.py` as the entrypoint.
4. In Advanced Settings, add `GEMINI_API_KEY` and `TMDB_API_KEY` in **Secrets**.
5. Click **Deploy**!

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).

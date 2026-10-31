"""CineMind AI - Natural Language Movie Recommender Application."""
import streamlit as st
from src.config import Config
from src.recommender import AIRecommender
from src.tmdb_client import TMDBClient
from src.styles import CUSTOM_CSS, render_movie_card_html

# 1. Page Configuration
st.set_page_config(
    page_title="CineMind AI — Mood & Vibe Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Custom Styles
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 3. Session State Initialization
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []
if "results" not in st.session_state:
    st.session_state.results = None
if "search_summary" not in st.session_state:
    st.session_state.search_summary = ""
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = "Give me a cozy, slow-burn mystery set in a rainy city that makes me feel like a detective."
if "view_watchlist" not in st.session_state:
    st.session_state.view_watchlist = False


# Helper callback for sample prompts
def set_prompt(sample_text: str):
    st.session_state.current_prompt = sample_text
    st.session_state.view_watchlist = False


# 4. Sidebar Configuration
with st.sidebar:
    st.markdown("### 🎬 CineMind AI")
    st.caption("AI-Powered Cinematic Exploration")
    st.markdown("---")

    # API Keys Section
    with st.expander("🔑 API Key Settings", expanded=False):
        st.write("Keys can also be configured via `.env` file.")
        sidebar_gemini_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=Config.GEMINI_API_KEY,
            help="Free key from Google AI Studio (https://aistudio.google.com)"
        )
        sidebar_tmdb_key = st.text_input(
            "TMDB API Key",
            type="password",
            value=Config.TMDB_API_KEY,
            help="Free key from The Movie Database (https://www.themoviedb.org)"
        )
        sidebar_openai_key = st.text_input(
            "OpenAI API Key (Optional)",
            type="password",
            value=Config.OPENAI_API_KEY
        )

    # Status indicators
    has_gemini = bool(sidebar_gemini_key or Config.GEMINI_API_KEY)
    has_tmdb = bool(sidebar_tmdb_key or Config.TMDB_API_KEY)
    
    st.markdown("##### 🔌 Connection Status")
    if has_gemini:
        st.success("🧠 AI Brain: Google Gemini Connected", icon="✅")
    else:
        st.info("🧠 AI Brain: Smart Demo Mode (Add Gemini key for live LLM)", icon="💡")
        
    if has_tmdb:
        st.success("🎥 Movie DB: TMDB Connected", icon="✅")
    else:
        st.info("🎥 Movie DB: Curated Media Mode (Add TMDB key for full catalog)", icon="💡")

    st.markdown("---")

    # Preferences & Filters
    st.markdown("##### 🎛️ Filters & Preferences")
    num_recommendations = st.slider("Number of Movies", min_value=3, max_value=8, value=5)
    
    era_filter = st.selectbox(
        "Release Era",
        ["Any Era", "Modern (2016 - Present)", "2000s - 2015", "80s & 90s Classics", "Vintage (< 1980)"]
    )
    
    min_rating = st.slider("Minimum Rating (TMDB)", min_value=0.0, max_value=8.5, value=7.0, step=0.1)
    
    region = st.selectbox("Streaming Region", ["US", "GB", "IN", "CA", "AU"], index=0)

    st.markdown("---")

    # Watchlist counter & toggle
    watchlist_count = len(st.session_state.watchlist)
    st.markdown(f"##### 📌 Saved Watchlist ({watchlist_count})")
    if st.button("👁️ View Watchlist" if not st.session_state.view_watchlist else "🔙 Back to Search", use_container_width=True):
        st.session_state.view_watchlist = not st.session_state.view_watchlist
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #64748b; line-height: 1.4;">
            <strong>Architecture:</strong><br>
            1. <strong>UI:</strong> Streamlit Glassmorphic Frontend<br>
            2. <strong>LLM:</strong> Google Gemini / OpenAI NLP Engine<br>
            3. <strong>Data:</strong> TMDB API for posters, trailers & providers
        </div>
        """,
        unsafe_allow_html=True
    )

# 5. Main Content Area
if st.session_state.view_watchlist:
    # Watchlist View
    st.markdown('<div class="hero-header"><h1 class="hero-title">📌 My Saved Watchlist</h1><p class="hero-subtitle">Movies you saved for your next movie night.</p></div>', unsafe_allow_html=True)
    
    if not st.session_state.watchlist:
        st.info("Your watchlist is currently empty. Explore movies and click 'Add to Watchlist' to save them here!")
    else:
        if st.button("🗑️ Clear Entire Watchlist"):
            st.session_state.watchlist = []
            st.rerun()

        for idx, movie in enumerate(st.session_state.watchlist):
            col_post, col_card = st.columns([1, 3])
            with col_post:
                if movie.get("poster_url"):
                    st.image(movie["poster_url"], use_container_width=True)
                else:
                    st.image("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500", use_container_width=True)
            with col_card:
                st.markdown(render_movie_card_html(movie), unsafe_allow_html=True)
                if movie.get("trailer_key"):
                    with st.expander("▶️ Watch Official Trailer", expanded=False):
                        st.video(f"https://www.youtube.com/watch?v={movie['trailer_key']}")
                if st.button(f"❌ Remove from Watchlist", key=f"remove_{idx}"):
                    st.session_state.watchlist.pop(idx)
                    st.rerun()
            st.markdown("---")

else:
    # Standard Search View
    st.markdown(
        """
        <div class="hero-header">
            <h1 class="hero-title">CineMind AI</h1>
            <p class="hero-subtitle">
                Describe a mood, atmosphere, or specific feeling — our AI curator translates your prompt into cinema gems with posters, trailers, and streaming options.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Prompt Suggestions Pills
    st.markdown("<div style='text-align: center; margin-bottom: 0.5rem; color: #94a3b8; font-size: 0.9rem;'>💡 <em>Need inspiration? Try clicking one of these moods:</em></div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🌧️ Cozy, rainy city slow-burn mystery", use_container_width=True):
            set_prompt("Give me a cozy, slow-burn mystery set in a rainy city that makes me feel like a detective.")
            st.rerun()
        if st.button("🚀 Mind-bending sci-fi with philosophical questions", use_container_width=True):
            set_prompt("Mind-bending sci-fi with philosophical questions about time and human existence like Interstellar or Arrival.")
            st.rerun()
    with c2:
        if st.button("🌆 Neon cyberpunk thriller with synth soundtrack", use_container_width=True):
            set_prompt("A stylish, neon-soaked cyberpunk thriller with synth music and an existential detective.")
            st.rerun()
        if st.button("🏰 Cozy autumn whodunit in an old mansion", use_container_width=True):
            set_prompt("A cozy autumn whodunit set in an old quirky mansion with eccentric family members.")
            st.rerun()
    with c3:
        if st.button("🌀 Psychological thriller with a shocking twist", use_container_width=True):
            set_prompt("A claustrophobic psychological thriller with an isolated setting and a shocking final twist.")
            st.rerun()
        if st.button("✨ Whimsical, heartwarming journey of wonder", use_container_width=True):
            set_prompt("A whimsical, heartwarming journey full of wonder, beautiful animation, and gentle mystery.")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Search Box Form
    with st.form("search_form"):
        user_prompt = st.text_area(
            "What kind of movie experience are you craving?",
            value=st.session_state.current_prompt,
            height=95,
            placeholder="e.g. A slow-burn 90s psychological thriller with dark alleyways and rain, where the ending leaves you speechless..."
        )
        
        search_clicked = st.form_submit_button("🔮 Discover Movies", use_container_width=True)

    # Trigger Search
    if search_clicked and user_prompt.strip():
        st.session_state.current_prompt = user_prompt.strip()
        
        with st.spinner("🎬 Analyzing atmospheric nuances and querying movie database..."):
            recommender = AIRecommender(
                gemini_key=sidebar_gemini_key,
                openai_key=sidebar_openai_key
            )
            tmdb_client = TMDBClient(api_key=sidebar_tmdb_key)

            # Get AI suggestions
            ai_output = recommender.recommend(
                prompt=user_prompt,
                num_movies=num_recommendations,
                era_filter=era_filter,
                min_rating=min_rating
            )

            st.session_state.search_summary = ai_output.get("search_summary", "")
            raw_recommendations = ai_output.get("recommended_movies", [])

            # Enrich each recommendation with TMDB metadata, trailer & stream providers
            enriched_results = []
            for item in raw_recommendations:
                movie_data = tmdb_client.enrich_movie(
                    title=item.get("title", ""),
                    year=item.get("year"),
                    ai_rationale=item.get("match_rationale", ""),
                    vibe_tags=item.get("vibe_tags", []),
                    match_score=item.get("match_score", 90)
                )
                enriched_results.append(movie_data)

            st.session_state.results = enriched_results

    # Display Results
    if st.session_state.results:
        if st.session_state.search_summary:
            st.markdown(
                f'<div class="ai-summary-box">🎯 <strong>AI Curator Insight:</strong> {st.session_state.search_summary}</div>',
                unsafe_allow_html=True
            )

        st.markdown(f"### 🎞️ Hand-picked Recommendations ({len(st.session_state.results)})")

        for idx, movie in enumerate(st.session_state.results):
            col_poster, col_details = st.columns([1, 2.8])

            with col_poster:
                if movie.get("poster_url"):
                    st.image(movie["poster_url"], use_container_width=True)
                else:
                    st.image("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500", use_container_width=True)

            with col_details:
                # Render HTML card
                st.markdown(render_movie_card_html(movie), unsafe_allow_html=True)

                # Trailer expander
                if movie.get("trailer_key"):
                    with st.expander("▶️ Watch Official Trailer", expanded=False):
                        st.video(f"https://www.youtube.com/watch?v={movie['trailer_key']}")

                # Action buttons
                is_saved = any(m.get("title") == movie.get("title") for m in st.session_state.watchlist)
                
                col_btn1, col_btn2 = st.columns([1, 2])
                with col_btn1:
                    if not is_saved:
                        if st.button("➕ Add to Watchlist", key=f"save_{idx}"):
                            st.session_state.watchlist.append(movie)
                            st.rerun()
                    else:
                        st.button("✅ Saved in Watchlist", key=f"saved_{idx}", disabled=True)

            st.markdown("---")

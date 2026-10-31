"""Custom CSS styles and UI component renderers for a cinema-grade dark interface."""

CUSTOM_CSS = """
<style>
/* Global Styling */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Background gradient */
.stApp {
    background: radial-gradient(circle at 50% 0%, #151c2e 0%, #0a0d14 70%, #05070a 100%);
    color: #e2e8f0;
}

/* Header container */
.hero-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem 1rem;
    position: relative;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 20%, #94a3b8 60%, #6366f1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.hero-subtitle {
    font-size: 1.15rem;
    color: #94a3b8;
    max-width: 650px;
    margin: 0 auto 1.5rem auto;
    line-height: 1.6;
}

/* Prompt Card & Box */
.stTextArea textarea {
    background: rgba(18, 24, 38, 0.75) !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 14px !important;
    color: #f8fafc !important;
    font-size: 1.05rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35) !important;
    transition: all 0.2s ease !important;
}

.stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25), 0 8px 30px rgba(99, 102, 241, 0.2) !important;
}

/* Action button */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.75rem !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 22px rgba(99, 102, 241, 0.55) !important;
}

/* AI Summary Card */
.ai-summary-box {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-left: 4px solid #6366f1;
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin: 1.5rem 0 2rem 0;
    color: #cbd5e1;
    font-size: 1.02rem;
    line-height: 1.6;
}

/* Movie Card */
.movie-card {
    background: rgba(18, 24, 38, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.75rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.movie-card:hover {
    border-color: rgba(99, 102, 241, 0.4);
    transform: translateY(-2px);
}

.movie-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.3rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.movie-meta {
    font-size: 0.92rem;
    color: #94a3b8;
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.6rem;
}

.badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}

.badge-score {
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(99, 102, 241, 0.5);
    color: #a5b4fc;
}

.badge-rating {
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.4);
    color: #fbbf24;
}

.badge-tag {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #cbd5e1;
}

.badge-provider {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.35);
    color: #34d399;
}

.rationale-quote {
    background: rgba(15, 23, 42, 0.7);
    border-left: 3px solid #818cf8;
    padding: 0.85rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.85rem 0;
    font-style: italic;
    color: #e0e7ff;
    font-size: 0.95rem;
}

.movie-overview {
    color: #94a3b8;
    font-size: 0.95rem;
    line-height: 1.55;
    margin: 0.75rem 0;
}

.credits-line {
    font-size: 0.88rem;
    color: #64748b;
    margin-top: 0.5rem;
}

.credits-highlight {
    color: #cbd5e1;
    font-weight: 500;
}

/* Quick prompt pill buttons */
.sample-pill {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #cbd5e1;
    border-radius: 20px;
    padding: 0.4rem 0.9rem;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-block;
    margin: 0.25rem;
}

.sample-pill:hover {
    background: rgba(99, 102, 241, 0.25);
    border-color: rgba(99, 102, 241, 0.5);
    color: #ffffff;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #0c1017 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

/* Hide Streamlit default chrome if desired */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""


def render_movie_card_html(movie: dict) -> str:
    """Generate HTML snippet for a movie recommendation card."""
    title = movie.get("title", "Untitled")
    year = movie.get("year", "")
    runtime = movie.get("runtime", 0)
    runtime_str = f"{runtime // 60}h {runtime % 60}m" if runtime else ""
    vote_avg = movie.get("vote_average", 0.0)
    vote_count = movie.get("vote_count", 0)
    match_score = movie.get("match_score", 90)
    genres = ", ".join(movie.get("genres", [])[:3])
    overview = movie.get("overview", "")
    rationale = movie.get("ai_rationale", "")
    director = movie.get("director", "Unknown")
    cast_members = ", ".join(movie.get("cast", [])[:3])
    vibe_tags = movie.get("vibe_tags", [])
    streaming = movie.get("streaming", [])

    # Tags html
    tags_html = "".join([f'<span class="badge badge-tag">#{tag}</span> ' for tag in vibe_tags])
    
    # Providers html
    providers_html = ""
    if streaming:
        prov_badges = "".join([f'<span class="badge badge-provider">📺 {p}</span> ' for p in streaming[:3]])
        providers_html = f'<div style="margin-top: 0.6rem;">{prov_badges}</div>'

    html = f"""
    <div class="movie-card">
        <div class="movie-title">
            <span>{title}</span>
            <span class="badge badge-score">⚡ {match_score}% Match</span>
        </div>
        <div class="movie-meta">
            <span>📅 {year}</span>
            {f'<span>• ⏱️ {runtime_str}</span>' if runtime_str else ''}
            <span>• <span class="badge badge-rating">★ {vote_avg} ({vote_count:,} votes)</span></span>
            {f'<span>• 🎭 {genres}</span>' if genres else ''}
        </div>
        <div style="margin: 0.5rem 0;">
            {tags_html}
        </div>
        <div class="rationale-quote">
            💡 <strong>Why this matches:</strong> {rationale}
        </div>
        <div class="movie-overview">
            {overview}
        </div>
        <div class="credits-line">
            🎬 Director: <span class="credits-highlight">{director}</span> 
            {f' | 👥 Cast: <span class="credits-highlight">{cast_members}</span>' if cast_members else ''}
        </div>
        {providers_html}
    </div>
    """
    return html

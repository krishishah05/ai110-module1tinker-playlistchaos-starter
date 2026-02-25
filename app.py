import streamlit as st
import random
from playlist_logic import build_playlists, search_songs, get_stats

st.set_page_config(page_title="Playlist Chaos", page_icon="🎵", layout="wide")

# ── Session state initialization ─────────────────────────────────────────────
if "songs" not in st.session_state:
    st.session_state.songs = [
        {"title": "Thunder Road", "artist": "Bruce Springsteen", "genre": "rock", "energy": 8},
        {"title": "Weightless", "artist": "Marconi Union", "genre": "ambient", "energy": 1},
        {"title": "Party Rock Anthem", "artist": "LMFAO", "genre": "party", "energy": 9},
        {"title": "Lofi Study Beats", "artist": "ChillHop", "genre": "lofi", "energy": 2},
        {"title": "Bohemian Rhapsody", "artist": "Queen", "genre": "rock", "energy": 7},
        {"title": "Ocean Eyes", "artist": "Billie Eilish", "genre": "pop", "energy": 3},
        {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "pop", "energy": 8},
        {"title": "Sleep Well Beast", "artist": "The National", "genre": "indie", "energy": 4},
    ]

if "profile" not in st.session_state:
    st.session_state.profile = {
        "favorite_genre": "pop",
        "hype_min_energy": 7,
        "chill_max_energy": 3,
    }

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🎵 Playlist Chaos")
st.caption("Your AI-powered mood playlist organizer (now with more chaos)")

# ── Sidebar: User Profile ────────────────────────────────────────────────────
with st.sidebar:
    st.header("👤 Your Profile")
    st.session_state.profile["favorite_genre"] = st.text_input(
        "Favorite Genre", value=st.session_state.profile["favorite_genre"]
    )
    st.session_state.profile["hype_min_energy"] = st.slider(
        "Hype Min Energy", 1, 10, st.session_state.profile["hype_min_energy"]
    )
    st.session_state.profile["chill_max_energy"] = st.slider(
        "Chill Max Energy", 1, 10, st.session_state.profile["chill_max_energy"]
    )

    st.divider()

    # ── Add Song Form ────────────────────────────────────────────────────────
    st.header("➕ Add a Song")
    with st.form("add_song_form"):
        new_title = st.text_input("Title")
        new_artist = st.text_input("Artist")
        new_genre = st.text_input("Genre")
        new_energy = st.slider("Energy", 1, 10, 5)
        submitted = st.form_submit_button("Add Song")

        if submitted and new_title:
            # Fix 9: trim whitespace and normalize artist/genre to lowercase
            new_song = {
                "title": new_title.strip(),
                "artist": new_artist.strip().lower(),
                "genre": new_genre.strip().lower(),
                "energy": new_energy,
            }
            st.session_state.songs.append(new_song)
            st.success(f"Added: {new_song['title']}")

# ── Build playlists ──────────────────────────────────────────────────────────
playlists = build_playlists(st.session_state.songs, st.session_state.profile)

# ── Main Layout ──────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🎧 Playlists", "🔍 Search", "📊 Stats"])

# ── Tab 1: Playlists ─────────────────────────────────────────────────────────
with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🔥 Hype")
        if playlists["Hype"]:
            for song in playlists["Hype"]:
                st.write(f"**{song['title']}** — {song['artist']} ({song['genre']}, ⚡{song['energy']})")
        else:
            st.info("No hype songs yet.")

    with col2:
        st.subheader("😌 Chill")
        if playlists["Chill"]:
            for song in playlists["Chill"]:
                st.write(f"**{song['title']}** — {song['artist']} ({song['genre']}, ⚡{song['energy']})")
        else:
            st.info("No chill songs yet.")

    with col3:
        st.subheader("🎲 Mixed")
        if playlists["Mixed"]:
            for song in playlists["Mixed"]:
                st.write(f"**{song['title']}** — {song['artist']} ({song['genre']}, ⚡{song['energy']})")
        else:
            st.info("No mixed songs yet.")

    st.divider()

    # ── Lucky Pick ───────────────────────────────────────────────────────────
    st.subheader("🎰 Lucky Pick")
    lucky_mode = st.selectbox("Pick from:", ["Any", "Hype", "Chill"])
    if st.button("🎲 Give me a song!"):
        # Fix 10: pick only from the selected mood playlist (or all combined for "Any")
        if lucky_mode == "Any":
            pool = (
                playlists["Hype"] + playlists["Chill"] + playlists["Mixed"]
            )
        else:
            pool = playlists[lucky_mode]
        if pool:
            pick = random.choice(pool)
            st.success(f"🎵 **{pick['title']}** by {pick['artist']} (⚡{pick['energy']})")
        else:
            st.warning(f"No songs in the {lucky_mode} playlist!")

# ── Tab 2: Search ─────────────────────────────────────────────────────────────
with tab2:
    st.subheader("🔍 Search Songs")
    search_field = st.selectbox("Search by:", ["title", "artist", "genre"])
    search_query = st.text_input("Search query")

    if search_query:
        results = search_songs(st.session_state.songs, search_query, search_field)
        if results:
            st.write(f"Found **{len(results)}** result(s):")
            for song in results:
                st.write(f"- **{song['title']}** by {song['artist']} [{song['genre']}] ⚡{song['energy']}")
        else:
            st.warning("No songs found.")

# ── Tab 3: Stats ──────────────────────────────────────────────────────────────
with tab3:
    st.subheader("📊 Playlist Statistics")
    stats = get_stats(st.session_state.songs, playlists)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Songs", stats["total"])
    c2.metric("Average Energy", stats["avg_energy"])
    # Fix 11: display hype ratio as a formatted percentage string
    c3.metric("Hype Ratio", f"{stats['hype_ratio']}%")

    st.divider()
    st.write("**Breakdown:**")
    for mood, songs in playlists.items():
        st.write(f"- {mood}: {len(songs)} songs")

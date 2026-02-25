HYPE_KEYWORDS = ["rock", "punk", "party"]
CHILL_KEYWORDS = ["lofi", "ambient", "sleep"]


def _matches_keywords(text, keywords):
    """Return True if text contains any keyword from the list."""
    return any(kw in text for kw in keywords)


def classify_song(song, profile):
    """
    Classify a song as 'Hype', 'Chill', or 'Mixed'.

    Hype  — energy >= hype_min_energy, OR genre matches favorite_genre,
             OR genre contains a hype keyword (rock, punk, party).
    Chill — energy <= chill_max_energy, OR title contains a chill keyword
             (lofi, ambient, sleep).
    Mixed — everything else.
    """
    energy = song.get("energy", 5)
    genre = song.get("genre", "").lower()
    title = song.get("title", "").lower()

    hype_min = profile.get("hype_min_energy", 7)
    chill_max = profile.get("chill_max_energy", 3)
    favorite_genre = profile.get("favorite_genre", "").lower()

    is_hype = (
        energy >= hype_min
        or genre == favorite_genre
        or _matches_keywords(genre, HYPE_KEYWORDS)
    )
    is_chill = (
        energy <= chill_max
        or _matches_keywords(title, CHILL_KEYWORDS)
    )

    if is_hype:
        return "Hype"
    if is_chill:
        return "Chill"
    return "Mixed"


def build_playlists(songs, profile):
    """Sort every song into the appropriate mood playlist."""
    playlists = {"Hype": [], "Chill": [], "Mixed": []}
    for song in songs:
        playlists[classify_song(song, profile)].append(song)
    return playlists


def search_songs(songs, query, field):
    """Case-insensitive partial-match search over a single song field."""
    needle = query.lower()
    return [s for s in songs if needle in s.get(field, "").lower()]


def get_stats(songs, playlists):
    """
    Return summary statistics for the current song library.

    total      — unique song count across all categories
    avg_energy — mean energy level of all songs
    hype_ratio — percentage of songs classified as Hype
    """
    total = len(songs)
    if total == 0:
        return {"total": 0, "avg_energy": 0.0, "hype_ratio": 0.0}

    avg_energy = sum(s.get("energy", 0) for s in songs) / total
    hype_ratio = len(playlists.get("Hype", [])) / total * 100

    return {
        "total": total,
        "avg_energy": round(avg_energy, 2),
        "hype_ratio": round(hype_ratio, 1),
    }

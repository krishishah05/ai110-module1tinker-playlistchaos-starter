HYPE_KEYWORDS = ["rock", "punk", "party"]
CHILL_KEYWORDS = ["lofi", "ambient", "sleep"]


def classify_song(song, profile):
    energy = song.get("energy", 5)
    genre = song.get("genre", "").lower()
    title = song.get("title", "").lower()

    hype_min = profile.get("hype_min_energy", 7)
    chill_max = profile.get("chill_max_energy", 3)
    favorite_genre = profile.get("favorite_genre", "").lower()

    # Fix 1: >= instead of > so songs at exactly hype_min count as Hype
    # Fix 2: also check whether genre matches the user's favorite_genre
    # Fix 3: also check genre against HYPE_KEYWORDS
    is_hype = (
        energy >= hype_min
        or genre == favorite_genre
        or any(kw in genre for kw in HYPE_KEYWORDS)
    )

    # Fix 4: also check title for CHILL_KEYWORDS
    is_chill = (
        energy <= chill_max
        or any(kw in title for kw in CHILL_KEYWORDS)
    )

    if is_hype:
        return "Hype"
    elif is_chill:
        return "Chill"
    else:
        return "Mixed"


def build_playlists(songs, profile):
    playlists = {"Hype": [], "Chill": [], "Mixed": []}
    for song in songs:
        category = classify_song(song, profile)
        playlists[category].append(song)
    return playlists


def search_songs(songs, query, field):
    # Fix 5: case-insensitive partial match instead of case-sensitive exact match
    query_lower = query.lower()
    return [s for s in songs if query_lower in s.get(field, "").lower()]


def get_stats(songs, playlists):
    # Fix 6: derive total from the master songs list, not from playlist lists
    total = len(songs)

    # Fix 7: average energy from master songs list
    avg_energy = sum(s.get("energy", 0) for s in songs) / total if total > 0 else 0

    hype_count = len(playlists.get("Hype", []))
    # Fix 8: hype_ratio as a percentage (0–100), not a raw fraction
    hype_ratio = (hype_count / total * 100) if total > 0 else 0

    return {
        "total": total,
        "avg_energy": round(avg_energy, 2),
        "hype_ratio": round(hype_ratio, 1),
    }

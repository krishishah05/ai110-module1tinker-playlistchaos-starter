HYPE_KEYWORDS = ["rock", "punk", "party"]
CHILL_KEYWORDS = ["lofi", "ambient", "sleep"]


def classify_song(song, profile):
    energy = song.get("energy", 5)
    genre = song.get("genre", "").lower()
    title = song.get("title", "").lower()

    hype_min = profile.get("hype_min_energy", 7)
    chill_max = profile.get("chill_max_energy", 3)
    favorite_genre = profile.get("favorite_genre", "").lower()

    # BUG 1: uses > instead of >= so energy == hype_min is not counted as Hype
    # BUG 2: does not check favorite_genre
    # BUG 3: does not check HYPE_KEYWORDS in genre
    is_hype = energy > hype_min

    # BUG 4: does not check CHILL_KEYWORDS in title
    is_chill = energy < chill_max

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
    # BUG 5: case-sensitive exact match instead of case-insensitive partial match
    return [s for s in songs if s.get(field, "") == query]


def get_stats(songs, playlists):
    # BUG 6: counts songs from playlists (may double-count) instead of using songs list
    all_playlist_songs = (
        playlists.get("Hype", [])
        + playlists.get("Chill", [])
        + playlists.get("Mixed", [])
    )
    total = len(all_playlist_songs)

    # BUG 7: sums energy from playlist songs (already correct length here but relies on above bug)
    avg_energy = sum(s.get("energy", 0) for s in all_playlist_songs) / total if total > 0 else 0

    hype_count = len(playlists.get("Hype", []))
    # BUG 8: hype_ratio is expressed as a fraction (0-1) instead of a percentage
    hype_ratio = hype_count / total if total > 0 else 0

    return {
        "total": total,
        "avg_energy": round(avg_energy, 2),
        "hype_ratio": round(hype_ratio, 4),
    }

# Playlist Chaos 🎵

A Streamlit app that organizes songs into mood-based playlists: **Hype**, **Chill**, and **Mixed** — powered by simple energy-level and genre logic.

This project is part of the **CodePath AI 110 Module 1 Tinker activity**.

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

A browser window will open at `http://localhost:8501`.

---

## Features

| Feature | Description |
|---|---|
| **Playlist Classification** | Songs are sorted into Hype, Chill, or Mixed based on energy level, genre, and title keywords |
| **User Profile** | Customize favorite genre and energy thresholds via the sidebar |
| **Add Songs** | Add new songs with title, artist, genre, and energy level |
| **Search** | Case-insensitive partial search by title, artist, or genre |
| **Lucky Pick** | Randomly grab a song from a specific mood playlist |
| **Statistics** | See total songs, average energy, and hype ratio at a glance |

---

## Classification Rules

| Playlist | Rule |
|---|---|
| **Hype** | Energy ≥ `hype_min_energy` (default 7), **OR** genre matches your favorite genre, **OR** genre contains a hype keyword (`rock`, `punk`, `party`) |
| **Chill** | Energy ≤ `chill_max_energy` (default 3), **OR** title contains a chill keyword (`lofi`, `ambient`, `sleep`) |
| **Mixed** | Everything else |

---

## Project Structure

```
module1-tinker-playlist-chaos/
├── app.py              # Streamlit UI
├── playlist_logic.py   # Classification, search, and stats logic
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Debugging Activity

This app was originally generated with intentional bugs for a debugging exercise. Key issues fixed:

1. **Classification** — `>=` vs `>` for hype energy threshold; missing genre and keyword checks
2. **Search** — changed from case-sensitive exact match to case-insensitive partial match
3. **Lucky Pick** — now respects the selected mood filter instead of pulling from all songs
4. **Statistics** — hype ratio now displays as a proper percentage; uses unique song count
5. **Data Normalization** — input is now trimmed of whitespace and normalized before storage

---

## Summary

This project demonstrates debugging skills through a Streamlit-based playlist organizer. Starting from a buggy initial implementation, the activity involves identifying and fixing logical errors in playlist classification, search, random selection, and statistics calculation. The end result is a working app that correctly sorts songs into mood-based playlists using configurable energy thresholds and genre rules.

---

## License

MIT

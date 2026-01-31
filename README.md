# NBA Player Stats Tracker

https://nbastatstracker.streamlit.app/

An interactive **Python + Streamlit** web application that allows users to search NBA players and explore career, seasonal, and per-game statistics using the `nba_api` library.

The app focuses on clean data presentation, historical accuracy, and real-world edge case handling for both modern and legacy NBA data.

---

## Current Features (v1.2.0)

### Player Search & Profiles
- Dropdown-based player search with optional **active-only toggle**
- Player header displaying:
  - Headshot image
  - Team logo (when available)
  - Career years
  - Position, height, weight, and birthdate

### Statistics & Data Views
- Career season statistics table
- Per-season **game log view**
- Automatic season sorting (newest → oldest)
- Per-season averages:
  - Points (PTS)
  - Rebounds (REB)
  - Assists (AST)
  - Field Goal Percentage (FG%) when available
- Conditional handling for **pre-1985 seasons** where FG% data is unavailable
- Clean tables with hidden indices and formatted percentages

### Accolades
- Filtered player awards (ex. All-Star, MVP, Championships)
- Deduplicated and counted accolades
- Responsive grid layout for clean display

### Performance & UX
- Cached API calls to reduce latency
- Loading spinners during data fetches
- Defensive handling of missing or incomplete API data
- Modular project structure for maintainability

---

## Tech Stack

- Python
- Streamlit
- nba_api
- Pandas

---


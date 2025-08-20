import requests
import re
import json
from datetime import datetime

URL = "https://www.psdevwiki.com/ps3/PS2_Classics_Emulator_Compatibility_List"

PLAYABILITY_TAGS = {
    "{{ps2classic}}": "PS2 Classic",
    "{{playable}}": "Playable",
    "{{minorissues}}": "Minor Issues",
    "{{majorissues}}": "Major Issues",
    "{{unplayable}}": "Unplayable",
}

def fetch_page():
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.text

def parse_stats(html):
    stats = {name: 0 for name in PLAYABILITY_TAGS.values()}
    stats["Untested"] = 0
    untested_games = []

    # parse table rows
    rows = re.findall(r"\|\-\n\| (.*?)\n", html, flags=re.DOTALL)
    
    for row in rows:
        cols = [c.strip() for c in row.split("||")]
        game_name = cols[0]
        availability = " ".join(cols[1:4])

        matched = False
        for marker, label in PLAYABILITY_TAGS.items():
            if marker in availability:
                stats[label] += 1
                matched = True
                break

        if not matched:
            stats["Untested"] += 1
            untested_games.append(game_name)

    return stats, untested_games

def main():
    html = fetch_page()
    stats, untested_games = parse_stats(html)

    data = {
        "stats": stats,
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    # write summary stats
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # write untested games
    with open("untested.json", "w", encoding="utf-8") as f:
        json.dump(untested_games, f, indent=2)

    print("Wrote data.json and untested.json")

if __name__ == "__main__":
    main()

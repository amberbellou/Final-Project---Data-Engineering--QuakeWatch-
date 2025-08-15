import os, requests
USGS_FEED = os.getenv(
    "USGS_FEED",
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson",
)
def fetch_events():
    r = requests.get(USGS_FEED, timeout=30)
    r.raise_for_status()
    return r.json().get("features", [])

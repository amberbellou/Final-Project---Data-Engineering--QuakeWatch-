# etl/extract.py

import os
import requests
import logging

# USGS real-time feed (all earthquakes in the past day)
USGS_FEED = os.getenv(
    "USGS_FEED",
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson",
)

def fetch_events():
    """Fetch recent earthquake events from USGS GeoJSON feed."""
    try:
        logging.info(f"Fetching data from {USGS_FEED}")
        response = requests.get(USGS_FEED, timeout=30)
        response.raise_for_status()
        data = response.json()
        if "features" not in data:
            raise ValueError("Unexpected format: 'features' key not found.")
        return data["features"]
    except requests.RequestException as e:
        logging.error(f"Failed to fetch events: {e}")
        raise
    except ValueError as ve:
        logging.error(f"Invalid response format: {ve}")
        raise

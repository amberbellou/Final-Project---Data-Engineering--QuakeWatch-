# app/dashboard.py

import os
import requests
import pandas as pd
import streamlit as st

# Optional: only used when you explicitly enable local DB reads
USE_LOCAL_DB = os.getenv("QW_USE_LOCAL_DB", "0") == "1"
if USE_LOCAL_DB:
    from sqlalchemy import text
    from sqlalchemy.orm import Session
    from app.db import engine

# --------- Config ---------
st.set_page_config(page_title="QuakeWatch", layout="wide")
st.title("🌍 QuakeWatch Dashboard")

# Public API base
API_BASE = os.getenv("QW_API_BASE", "http://localhost:8000")

with st.expander("🔧 Advanced: API Source Settings"):
    override_url = st.text_input("Override API Base URL", value=API_BASE)
    if override_url:
        API_BASE = override_url.strip()

# --------- Sidebar controls ---------
MIN_MAG = st.sidebar.slider("Minimum magnitude", -1.0, 10.0, 4.0, 0.1)
LIMIT = st.sidebar.slider("Rows (events)", 50, 2000, 500, 50)

# --------- Helpers ---------
def api_get(path: str, **params):
    """Robust API getter with fallback URLs."""
    bases = [API_BASE, "http://api:8000", "http://localhost:8000"]
    for base in bases:
        try:
            r = requests.get(f"{base}{path}", params=params, timeout=10)
            if r.ok:
                return r.json()
        except Exception:
            pass
    return []

def load_events(min_mag: float, limit: int) -> pd.DataFrame:
    """Load events from API or local DB."""
    if USE_LOCAL_DB:
        try:
            with Session(engine) as s:
                df = pd.read_sql_query(
                    text("""
                        SELECT event_id, time_utc, magnitude,
                               latitude AS lat, longitude AS lon, depth_km
                        FROM fact_event
                        WHERE magnitude >= :m
                        ORDER BY time_utc DESC
                        LIMIT :l
                    """),
                    s.bind,
                    params={"m": float(min_mag), "l": int(limit)},
                )
            return df
        except Exception as e:
            st.warning(f"Local DB read failed ({e}). Falling back to API.")

    rows = api_get("/events", min_mag=min_mag, limit=limit)
    df = pd.DataFrame(rows)
    if not df.empty:
        if "latitude" in df.columns and "lat" not in df.columns:
            df = df.rename(columns={"latitude": "lat"})
        if "longitude" in df.columns and "lon" not in df.columns:
            df = df.rename(columns={"longitude": "lon"})
        if "time_utc" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["time_utc"]):
            df["time_utc"] = pd.to_datetime(df["time_utc"], errors="coerce", utc=True)
    return df

def get_last_updated(events_df: pd.DataFrame):
    if not events_df.empty and "time_utc" in events_df.columns:
        try:
            return pd.to_datetime(events_df["time_utc"]).max()
        except Exception:
            return None
    return None

# --------- Data source banner ---------
source = f"API: {API_BASE}" if not USE_LOCAL_DB else "Local DB connection"
st.caption(f"Data source: {source}")

# --------- Country stats ---------
st.subheader("Top countries by quake count")
country_rows = api_get("/stats/by-country", min_mag=MIN_MAG)
country_df = pd.DataFrame(country_rows)
if not country_df.empty and {"country", "events"}.issubset(country_df.columns):
    st.bar_chart(country_df.set_index("country")["events"])
else:
    st.warning("No country stats available. Try lowering magnitude or check ETL/API.")

# --------- Recent events ---------
st.subheader("Recent events")
events_df = load_events(MIN_MAG, LIMIT)

last_ts = get_last_updated(events_df)
st.caption(f"Last updated: {last_ts if last_ts is not None else 'N/A'} UTC")

if events_df.empty:
    st.warning("No event data found. Try running ETL or adjust filters.")
else:
    if "time_utc" in events_df.columns:
        events_df = events_df.sort_values("time_utc")

    if {"time_utc", "magnitude"}.issubset(events_df.columns):
        st.line_chart(events_df.set_index("time_utc")["magnitude"])

    if {"lat", "lon"}.issubset(events_df.columns):
        st.map(events_df[["lat", "lon"]])

    show_cols = [c for c in ["event_id", "time_utc", "magnitude", "mag_type", "lat", "lon", "depth_km", "place"] if c in events_df.columns]
    st.dataframe(events_df[show_cols] if show_cols else events_df)

# --------- Footer ---------
with st.expander("ℹ️ How this works"):
    st.write("""
    - On Streamlit Cloud, this app calls the **FastAPI** via `QW_API_BASE`.
    - Locally, set `QW_USE_LOCAL_DB=1` to read directly from Postgres.
    - Endpoints used: `/events` and `/stats/by-country`.
    """)

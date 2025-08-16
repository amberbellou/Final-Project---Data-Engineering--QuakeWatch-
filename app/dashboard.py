# app/dashboard.py

import os
import requests
import pandas as pd
import streamlit as st

# Optional: only used when you explicitly enable local DB reads
USE_LOCAL_DB = os.getenv("QW_USE_LOCAL_DB", "0") == "1"
if USE_LOCAL_DB:
    # these imports will fail on Streamlit Cloud, so keep them gated
    from sqlalchemy import text
    from sqlalchemy.orm import Session
    from app.db import engine  # requires your Postgres to be reachable

# --------- Config ---------
st.set_page_config(page_title="QuakeWatch", layout="wide")
st.title("🌍 QuakeWatch Dashboard")

# Public API base (for Streamlit Cloud or any deployment)
# Set this in Streamlit Cloud → Settings → Secrets:
# QW_API_BASE = https://<your-public-fastapi-url>
API_BASE = os.getenv("QW_API_BASE", "http://localhost:8000")

# --------- Sidebar controls ---------
MIN_MAG = st.sidebar.slider("Minimum magnitude", -1.0, 10.0, 4.0, 0.1)
LIMIT   = st.sidebar.slider("Rows (events)", 50, 2000, 500, 50)

# --------- Helpers ---------
def api_get(path: str, **params):
    """
    Robust API getter:
    - Tries QW_API_BASE first (cloud-friendly)
    - Falls back to docker-compose hostnames (api) and localhost for local dev
    """
    bases = [API_BASE]
    # convenient fallbacks for local setups
    if "http://api:8000" not in bases:
        bases.append("http://api:8000")
    if "http://localhost:8000" not in bases:
        bases.append("http://localhost:8000")

    for base in bases:
        try:
            r = requests.get(f"{base}{path}", params=params, timeout=10)
            if r.ok:
                return r.json()
        except Exception:
            pass
    return []

def load_events(min_mag: float, limit: int) -> pd.DataFrame:
    """
    Load events either from API (default) or directly from DB (if USE_LOCAL_DB=1).
    Returns a DataFrame with at least: time_utc, magnitude, lat, lon.
    """
    if USE_LOCAL_DB:
        try:
            from sqlalchemy import text  # local import to keep Cloud safe
            from sqlalchemy.orm import Session
            from app.db import engine

            with Session(engine) as s:
                df = pd.read_sql_query(
                    text("""
                        SELECT event_id,
                               time_utc,
                               magnitude,
                               latitude  AS lat,
                               longitude AS lon,
                               depth_km
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
            # fall through to API path below

    # API path (works on Cloud)
    rows = api_get("/events", min_mag=min_mag, limit=limit)
    df = pd.DataFrame(rows)
    # normalize expected columns
    if not df.empty:
        # rename if needed
        if "latitude" in df.columns and "lat" not in df.columns:
            df = df.rename(columns={"latitude": "lat"})
        if "longitude" in df.columns and "lon" not in df.columns:
            df = df.rename(columns={"longitude": "lon"})
        # parse timestamps
        if "time_utc" in df.columns:
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

# --------- Country stats (API) ---------
st.subheader("Top countries by quake count")
country_rows = api_get("/stats/by-country", min_mag=MIN_MAG)
country_df = pd.DataFrame(country_rows)
if not country_df.empty and {"country", "events"}.issubset(country_df.columns):
    st.bar_chart(country_df.set_index("country")["events"])
else:
    st.info("No country stats to display yet (try lowering the magnitude or run the ETL).")

# --------- Recent events ---------
st.subheader("Recent events")
events_df = load_events(MIN_MAG, LIMIT)

last_ts = get_last_updated(events_df)
st.caption(f"Last updated: {last_ts if last_ts is not None else 'N/A'} UTC")

if events_df.empty:
    st.info("No events yet. Try running the ETL or lowering the magnitude.")
else:
    # ensure sorting by time if available
    if "time_utc" in events_df.columns:
        events_df = events_df.sort_values("time_utc")

    # magnitude timeline
    if "time_utc" in events_df.columns and "magnitude" in events_df.columns:
        st.line_chart(events_df.set_index("time_utc")["magnitude"])

    # map (needs lat/lon)
    if {"lat", "lon"}.issubset(events_df.columns):
        st.map(events_df[["lat", "lon"]])

    # show table
    show_cols = [c for c in ["event_id","time_utc","magnitude","mag_type","lat","lon","depth_km","place"] if c in events_df.columns]
    st.dataframe(events_df[show_cols] if show_cols else events_df)

# --------- Footer tips ---------
with st.expander("ℹ️ How this works"):
    st.write(
        """
        - On Streamlit Cloud, this app calls the **FastAPI** you deployed via `QW_API_BASE`.
        - Locally, you can set `QW_USE_LOCAL_DB=1` to read directly from Postgres instead.
        - Endpoints used: `/events` and `/stats/by-country` (plus the DB for local-only mode).
        """
    )

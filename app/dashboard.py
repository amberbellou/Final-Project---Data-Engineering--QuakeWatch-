# app/dashboard.py

import os
import pandas as pd
import streamlit as st
import requests

st.set_page_config(page_title="QuakeWatch", layout="wide")
st.title("🌍 QuakeWatch Dashboard")

# --------- Config from env ---------
# If QW_API_BASE is set, we'll try the API first. Example: https://your-api.onrender.com
API_BASE = os.getenv("QW_API_BASE", "").strip().rstrip("/")
# If QW_USE_LOCAL_DB=1, allow direct DB reads as a fallback or primary when API not set/available
USE_LOCAL_DB = os.getenv("QW_USE_LOCAL_DB", "0") == "1"

if USE_LOCAL_DB:
    from sqlalchemy import create_engine, text
    # Reuse the same DATABASE_URL logic as the API
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)

# --------- Sidebar controls ---------
MIN_MAG = st.sidebar.slider("Minimum magnitude", -1.0, 10.0, 4.0, 0.1)
LIMIT = st.sidebar.slider("Rows (events)", 50, 2000, 500, 50)

# --------- Advanced (optional) ---------
with st.expander("🔧 Advanced: Data Source"):
    _override = st.text_input("API Base URL (optional)", value=API_BASE)
    API_BASE = _override.strip().rstrip("/") if _override else API_BASE
    st.caption("If empty, the dashboard will read directly from the database only when QW_USE_LOCAL_DB=1.")

# --------- Helpers ---------
def _try_api(path: str, **params):
    """Call FastAPI endpoint (JSON). Returns Python object or None if unavailable."""
    if not API_BASE:
        return None
    url = f"{API_BASE}{path}"
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.ok:
            return r.json()
    except Exception:
        pass
    return None

@st.cache_data(show_spinner=False)
def load_events(min_mag: float, limit: int) -> tuple[pd.DataFrame, str]:
    """
    Returns (df, source_str)
    Tries API first if API_BASE is set; otherwise uses local DB when enabled.
    """
    # 1) API path (JSON endpoint)
    if API_BASE:
        data = _try_api("/events.json", min_mag=min_mag, limit=limit)
        if isinstance(data, list) and data:
            df = pd.DataFrame(data)
            src = f"API: {API_BASE}"
            return _normalize_events(df), src
        elif isinstance(data, list):
            # empty list is still valid — just no rows yet
            return pd.DataFrame(), f"API: {API_BASE}"

    # 2) Local DB path (only if enabled)
    if USE_LOCAL_DB:
        try:
            with engine.connect() as conn:
                df = pd.read_sql_query(
                    text(
                        """
                        SELECT
                          fe.event_id,
                          fe.time_utc,
                          fe.magnitude,
                          fe.latitude AS lat,
                          fe.longitude AS lon,
                          fe.depth_km,
                          dmt.mag_type,
                          dp.raw_place AS place
                        FROM fact_event fe
                        LEFT JOIN dim_place dp     ON fe.place_id = dp.place_id
                        LEFT JOIN dim_mag_type dmt ON fe.mag_type_id = dmt.mag_type_id
                        WHERE fe.magnitude >= :m
                        ORDER BY fe.time_utc DESC
                        LIMIT :l
                        """
                    ),
                    conn,
                    params={"m": float(min_mag), "l": int(limit)},
                )
            return _normalize_events(df), "Local DB"
        except Exception as e:
            st.warning(f"Local DB read failed: {e}")

    # 3) Nothing available
    return pd.DataFrame(), "No data source available"

@st.cache_data(show_spinner=False)
def load_country_stats(min_mag: float) -> tuple[pd.DataFrame, bool]:
    """
    Returns (df, used_api: bool). Only available via API endpoint.
    """
    data = _try_api("/stats/by-country", min_mag=min_mag)
    if isinstance(data, list):
        df = pd.DataFrame(data)
        return df, True
    return pd.DataFrame(), False

def _normalize_events(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    # standardize columns for downstream charts
    rename_map = {
        "latitude": "lat",
        "longitude": "lon",
    }
    df = df.rename(columns=rename_map)
    if "time_utc" in df.columns:
        df["time_utc"] = pd.to_datetime(df["time_utc"], errors="coerce", utc=True)
    # keep only known columns where present
    keep = [c for c in ["event_id", "time_utc", "magnitude", "mag_type", "lat", "lon", "depth_km", "place"] if c in df.columns]
    return df[keep] if keep else df

def _last_updated(df: pd.DataFrame):
    if not df.empty and "time_utc" in df.columns:
        s = pd.to_datetime(df["time_utc"], errors="coerce")
        if not s.dropna().empty:
            return s.max()
    return None

# --------- Data loads ---------
events_df, source_str = load_events(MIN_MAG, LIMIT)
country_df, country_from_api = load_country_stats(MIN_MAG)

# --------- Source banner ---------
st.caption(f"Data source: {source_str}")

# --------- Country stats ---------
st.subheader("Top countries by quake count")
if not country_df.empty and {"country", "events"}.issubset(country_df.columns):
    st.bar_chart(country_df.set_index("country")["events"])
else:
    st.info("Country stats unavailable (API not set/reachable or no data).")

# --------- Recent events ---------
st.subheader("Recent events")
last_ts = _last_updated(events_df)
st.caption(f"Last updated: {last_ts if last_ts is not None else 'N/A'} UTC")

if events_df.empty:
    st.warning("No event data found. Try running ETL, adjust filters, or set QW_API_BASE / QW_USE_LOCAL_DB.")
else:
    # time series
    if {"time_utc", "magnitude"}.issubset(events_df.columns):
        st.line_chart(events_df.set_index("time_utc")["magnitude"])

    # map (needs lat/lon)
    if {"lat", "lon"}.issubset(events_df.columns):
        st.map(events_df[["lat", "lon"]].dropna())

    # table
    st.dataframe(events_df, use_container_width=True, height=420)

# --------- Footer ---------
with st.expander("ℹ️ Notes"):
    st.write("""
    - The dashboard prefers the **API** (endpoint `/events.json`, `/stats/by-country`) when `QW_API_BASE` is set.
    - If `QW_USE_LOCAL_DB=1`, the dashboard can read directly from your database using `DATABASE_URL`.
    - On Render, deploy the API and Dashboard as separate services and provide both with the same `DATABASE_URL`. 
    """)

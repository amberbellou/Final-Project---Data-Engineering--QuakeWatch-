# app/dashboard.py
import os
import time
import requests
import pandas as pd
import streamlit as st
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db import engine
import os
API_BASE = os.getenv("QW_API_BASE", "http://localhost:8000")  # default for local dev


# --- ensure project root is on the import path ---
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ../
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# --------------------------------------------------

# Try DB; if unavailable (e.g., Streamlit Cloud without a DB), fall back to API-only mode
engine = None
try:
    from app.db import engine as _engine
    engine = _engine
except Exception:
    pass


st.set_page_config(page_title="QuakeWatch", layout="wide")
st.title("🌍 QuakeWatch Dashboard")

MIN_MAG = st.sidebar.slider("Minimum magnitude", -1.0, 10.0, 4.0, 0.1)
LIMIT   = st.sidebar.slider("Rows (events)", 50, 2000, 500, 50)

 # --- ensure project root is on the import path ---
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# --------------------------------------------------

from app.db import engine

# ---- DB health + last updated ----
with Session(engine) as s:
    last_ts = s.execute(text("SELECT max(time_utc) FROM fact_event")).scalar()
st.caption(f"Last updated: {last_ts or 'N/A'} UTC")

# ---- Top countries (uses API) ----
# inside Docker, the API host is "api"; when running locally without compose, fall back to localhost
def api_get(path: str, **params):
    for base in ("http://api:8000", "http://localhost:8000"):
        try:
            r = requests.get(f"{base}{path}", params=params, timeout=10)
            if r.ok:
                return r.json()
        except Exception:
            pass
    return []

country_rows = api_get("/stats/by-country", min_mag=MIN_MAG)
country_df = pd.DataFrame(country_rows)
st.subheader("Top countries by quake count")
if not country_df.empty:
    st.bar_chart(country_df.set_index("country")["events"])
else:
    st.info("No country stats yet (run the ETL or lower the magnitude).")

# ---- Recent events (direct SQL) ----
with Session(engine) as s:
    events_df = pd.read_sql_query(
        text("""
            SELECT event_id, time_utc, magnitude, latitude AS lat, longitude AS lon, depth_km
            FROM fact_event
            WHERE magnitude >= :m
            ORDER BY time_utc DESC
            LIMIT :l
        """),
        s.bind,
        params={"m": float(MIN_MAG), "l": int(LIMIT)},
    )

st.subheader("Recent events")
st.write(f"{len(events_df)} rows")
if not events_df.empty:
    st.line_chart(events_df.set_index("time_utc")["magnitude"])
    st.map(events_df[["lat", "lon"]])
    st.dataframe(events_df)
else:
    st.info("No events yet. Try running the ETL.")
   


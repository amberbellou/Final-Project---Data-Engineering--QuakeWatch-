import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import engine

st.title("QuakeWatch Dashboard")
min_mag = st.slider("Minimum magnitude", 0.0, 10.0, 4.0, 0.1)
limit = st.number_input("Limit", 50, 2000, 500, 50)

with Session(engine) as s:
    df = pd.read_sql_query(
        text("""
            SELECT event_id, time_utc, magnitude, latitude, longitude, depth_km
            FROM fact_event
            WHERE magnitude >= :m
            ORDER BY time_utc DESC
            LIMIT :l
        """),
        s.bind, params={"m": float(min_mag), "l": int(limit)}
    )

st.write(f"{len(df)} events")
if not df.empty:
    st.line_chart(df.set_index("time_utc")["magnitude"])
    st.map(df.rename(columns={"latitude":"lat","longitude":"lon"})[["lat","lon"]])
else:
    st.info("No events yet. Run the ETL flow.")

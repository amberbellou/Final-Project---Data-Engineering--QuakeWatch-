# etl/transform.py

import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema
import logging

def _split_place(raw: str):
    """Split a USGS place string into region and country (best-effort)."""
    if not raw or not isinstance(raw, str):
        return None, None
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) == 1:
        return parts[0], None
    return parts[-2], parts[-1]

def features_to_df(features: list) -> pd.DataFrame:
    """Convert GeoJSON features list into a structured DataFrame."""
    rows = []
    for f in features:
        props = f.get("properties", {})
        geom = f.get("geometry", {}) or {}
        coords = geom.get("coordinates", [None, None, None])
        region, country = _split_place(props.get("place"))

        rows.append({
            "event_id": f.get("id"),
            "time_utc": pd.to_datetime(props.get("time"), unit="ms", utc=True),
            "updated_at": pd.to_datetime(props.get("updated"), unit="ms", utc=True),
            "latitude": coords[1],
            "longitude": coords[0],
            "depth_km": coords[2],
            "magnitude": props.get("mag"),
            "mag_type": (props.get("magType") or "").upper() or None,
            "raw_place": props.get("place"),
            "region": region,
            "country": country,
            "tsunami": int(props.get("tsunami") or 0),
            "source": props.get("type") or "earthquake",
        })
    return pd.DataFrame(rows)

# Define schema using Pandera
schema = DataFrameSchema({
    "event_id": Column(str),
    "time_utc": Column(pd.DatetimeTZDtype(tz="UTC")),
    "updated_at": Column(pd.DatetimeTZDtype(tz="UTC")),
    "latitude": Column(float, nullable=True),
    "longitude": Column(float, nullable=True),
    "depth_km": Column(float, nullable=True),
    "magnitude": Column(float, nullable=True),
    "mag_type": Column(object, nullable=True),
    "raw_place": Column(object, nullable=True),
    "region": Column(object, nullable=True),
    "country": Column(object, nullable=True),
    "tsunami": Column(int),
    "source": Column(object),
})

def validate_df(df: pd.DataFrame) -> pd.DataFrame:
    """Run custom and schema-based validation on DataFrame."""
    try:
        if not df["magnitude"].between(-1, 12).fillna(True).all():
            raise ValueError("Magnitude values are out of expected range (-1 to 12).")
        if not df["latitude"].between(-90, 90).fillna(True).all():
            raise ValueError("Latitude values are out of range (-90 to 90).")
        if not df["longitude"].between(-180, 180).fillna(True).all():
            raise ValueError("Longitude values are out of range (-180 to 180).")
        return schema.validate(df, lazy=True)
    except pa.errors.SchemaErrors as e:
        logging.error("DataFrame validation failed with schema errors:\n%s", e.failure_cases)
        raise
    except Exception as e:
        logging.error(f"Unexpected error during validation: {e}")
        raise

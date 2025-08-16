# app/api.py
from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sqlalchemy import func, literal, text, select
from sqlalchemy.orm import Session

from app.db import engine
from app.models import FactEvent, DimPlace, DimMagType


# ---------- FastAPI app ----------
app = FastAPI(title="QuakeWatch API", version="0.1.0")

# CORS (safe defaults for local; tighten in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, set explicit origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Response models ----------
class EventOut(BaseModel):
    event_id: str
    time_utc: Optional[str]          # ISO string
    magnitude: Optional[float]
    mag_type: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    depth_km: Optional[float]
    place: Optional[str]


class CountryStat(BaseModel):
    country: str
    events: int


class HealthOut(BaseModel):
    ok: bool


# ---------- Routes ----------
@app.get("/events", response_model=List[EventOut], tags=["default"])
def events(
    min_mag: float = Query(0.0, ge=-1.0, le=12.0),
    max_mag: float = Query(10.0, ge=-1.0, le=12.0),
    limit: int = Query(100, ge=1, le=2000),
):
    """Recent events with basic details."""
    with Session(engine) as s:
        q = (
            s.query(FactEvent, DimPlace, DimMagType)
            .join(DimPlace, FactEvent.place_id == DimPlace.place_id, isouter=True)
            .join(DimMagType, FactEvent.mag_type_id == DimMagType.mag_type_id, isouter=True)
            .filter(FactEvent.magnitude >= min_mag, FactEvent.magnitude <= max_mag)
            .order_by(FactEvent.time_utc.desc())
            .limit(limit)
        )
        rows = q.all()

    return [
        {
            "event_id": e.event_id,
            "time_utc": (e.time_utc.isoformat() if getattr(e, "time_utc", None) else None),
            "magnitude": e.magnitude,
            "mag_type": (m.mag_type if m else None),
            "lat": e.latitude,
            "lon": e.longitude,
            "depth_km": e.depth_km,
            "place": (p.raw_place if p else None),
        }
        for e, p, m in rows
    ]


@app.get("/stats/by-country", response_model=List[CountryStat], tags=["default"])
def stats_by_country(min_mag: float = Query(4.0, ge=-1.0, le=12.0)):
    """
    Count of events by country (falling back to 'Unknown' when missing), ordered by count desc.
    Uses SQLAlchemy Core select() to avoid label/order_by pitfalls and coerces counts to int.
    """
    unknown = literal("Unknown")
    country_expr = func.coalesce(DimPlace.country, unknown).label("country")
    count_expr = func.count(FactEvent.event_id).label("events")

    stmt = (
        select(country_expr, count_expr)
        .select_from(FactEvent)
        .join(DimPlace, FactEvent.place_id == DimPlace.place_id, isouter=True)
        .where(FactEvent.magnitude >= min_mag)
        .group_by(country_expr)
        .order_by(count_expr.desc())
    )

    with Session(engine) as s:
        rows = s.execute(stmt).all()

    return [{"country": c, "events": int(n)} for (c, n) in rows]


@app.get("/health", response_model=HealthOut, tags=["default"])
def health():
    """Simple DB liveness check."""
    with Session(engine) as s:
        s.execute(text("SELECT 1"))
    return {"ok": True}

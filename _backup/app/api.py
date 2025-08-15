from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import engine
from app.models import FactEvent, DimPlace, DimMagType

app = FastAPI(title="QuakeWatch API")

@app.get("/events")
def events(min_mag: float = 0.0, max_mag: float = 10.0, limit: int = 100):
    with Session(engine) as s:
        q = (s.query(FactEvent, DimPlace, DimMagType)
               .join(DimPlace, FactEvent.place_id == DimPlace.place_id, isouter=True)
               .join(DimMagType, FactEvent.mag_type_id == DimMagType.mag_type_id, isouter=True)
               .filter(FactEvent.magnitude >= min_mag, FactEvent.magnitude <= max_mag)
               .order_by(FactEvent.time_utc.desc())
               .limit(limit))
        return [{
            "event_id": e.event_id,
            "time_utc": e.time_utc,
            "magnitude": e.magnitude,
            "mag_type": m.mag_type if m else None,
            "lat": e.latitude,
            "lon": e.longitude,
            "depth_km": e.depth_km,
            "place": p.raw_place if p else None
        } for e, p, m in q.all()]

@app.get("/stats/by-country")
def stats_by_country(min_mag: float = 4.0):
    with Session(engine) as s:
        rows = (s.query(func.coalesce(DimPlace.country, "Unknown"), func.count())
                  .join(DimPlace, FactEvent.place_id == DimPlace.place_id, isouter=True)
                  .filter(FactEvent.magnitude >= min_mag)
                  .group_by(func.coalesce(DimPlace.country, "Unknown"))
                  .order_by(func.count().desc())
                ).all()
        return [{"country": c, "events": n} for c, n in rows]

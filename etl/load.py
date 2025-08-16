# etl/load.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import engine, Base
from app.models import FactEvent, DimPlace, DimMagType

def init_db():
    """Create tables if they don’t exist."""
    Base.metadata.create_all(engine)

def _get_or_create(session: Session, model, defaults=None, **kwargs):
    """Find or create a record in a dimension table."""
    instance = session.execute(select(model).filter_by(**kwargs)).scalar_one_or_none()
    if instance:
        return instance
    instance = model(**{**(defaults or {}), **kwargs})
    session.add(instance)
    session.flush()  # ensures instance gets an ID
    return instance

def upsert_events(df):
    """Upsert event records from a DataFrame into the database."""
    with Session(engine) as session:
        for row in df.to_dict(orient="records"):
            mag = _get_or_create(session, DimMagType, mag_type=row["mag_type"]) if row["mag_type"] else None
            place = _get_or_create(
                session,
                DimPlace,
                raw_place=row["raw_place"],
                defaults={"region": row["region"], "country": row["country"]}
            ) if row["raw_place"] else None

            existing = session.get(FactEvent, row["event_id"])
            payload = {
                "event_id": row["event_id"],
                "time_utc": row["time_utc"].to_pydatetime(),
                "updated_at": row["updated_at"].to_pydatetime(),
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "depth_km": row["depth_km"],
                "magnitude": row["magnitude"],
                "mag_type_id": getattr(mag, "mag_type_id", None),
                "place_id": getattr(place, "place_id", None),
                "tsunami": int(row["tsunami"]),
                "source": row["source"],
            }

            if existing:
                for key, value in payload.items():
                    setattr(existing, key, value)
            else:
                session.add(FactEvent(**payload))

        session.commit()

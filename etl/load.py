from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import engine, Base
from app.models import FactEvent, DimPlace, DimMagType

def init_db():
    Base.metadata.create_all(engine)

def _get_or_create(session: Session, model, defaults=None, **kwargs):
    inst = session.execute(select(model).filter_by(**kwargs)).scalar_one_or_none()
    if inst:
        return inst
    inst = model(**{**(defaults or {}), **kwargs})
    session.add(inst)
    session.flush()
    return inst

def upsert_events(df):
    with Session(engine) as s:
        for row in df.to_dict(orient="records"):
            mag = _get_or_create(s, DimMagType, mag_type=row["mag_type"]) if row["mag_type"] else None
            place = _get_or_create(
                s, DimPlace, raw_place=row["raw_place"],
                defaults={"region": row["region"], "country": row["country"]}
            ) if row["raw_place"] else None
            existing = s.get(FactEvent, row["event_id"])
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
                for k, v in payload.items():
                    setattr(existing, k, v)
            else:
                s.add(FactEvent(**payload))
        s.commit()

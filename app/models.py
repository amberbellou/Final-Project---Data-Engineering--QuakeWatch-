from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey, Index
from sqlalchemy.orm import relationship
from .db import Base

class DimPlace(Base):
    __tablename__ = "dim_place"
    place_id = Column(Integer, primary_key=True)
    region = Column(String(100))
    country = Column(String(100))
    raw_place = Column(String(255), unique=True, index=True)

    def __repr__(self):
        return f"<DimPlace(country='{self.country}', region='{self.region}')>"

class DimMagType(Base):
    __tablename__ = "dim_mag_type"
    mag_type_id = Column(Integer, primary_key=True)
    mag_type = Column(String(50), unique=True, index=True)

    def __repr__(self):
        return f"<DimMagType(mag_type='{self.mag_type}')>"

class FactEvent(Base):
    __tablename__ = "fact_event"
    event_id = Column(String, primary_key=True)
    time_utc = Column(TIMESTAMP, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    depth_km = Column(Float)
    magnitude = Column(Float, index=True)
    mag_type_id = Column(Integer, ForeignKey("dim_mag_type.mag_type_id"), index=True)
    place_id = Column(Integer, ForeignKey("dim_place.place_id"), index=True)
    tsunami = Column(Integer)
    updated_at = Column(TIMESTAMP)
    source = Column(String(50))

    mag_type = relationship("DimMagType")
    place = relationship("DimPlace")

    def __repr__(self):
        return f"<FactEvent(event_id='{self.event_id}', magnitude={self.magnitude}, time={self.time_utc})>"

# Composite index for performance
Index("ix_event_time_mag", FactEvent.time_utc, FactEvent.magnitude)

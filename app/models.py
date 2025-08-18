from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from .db import Base

class DimPlace(Base):
    __tablename__ = "dim_place"

    place_id = Column(Integer, primary_key=True, nullable=False)
    region   = Column(String(100), nullable=True)
    country  = Column(String(100), index=True, nullable=True)
    raw_place = Column(String(255), unique=True, index=True, nullable=True)

    def __repr__(self):
        return f"<DimPlace(country='{self.country}', region='{self.region}')>"

class DimMagType(Base):
    __tablename__ = "dim_mag_type"

    mag_type_id = Column(Integer, primary_key=True, nullable=False)
    mag_type    = Column(String(50), unique=True, index=True, nullable=True)

    def __repr__(self):
        return f"<DimMagType(mag_type='{self.mag_type}')>"

class FactEvent(Base):
    __tablename__ = "fact_event"

    event_id  = Column(String, primary_key=True, nullable=False)
    time_utc  = Column(DateTime(timezone=True), index=True, nullable=True)
    latitude  = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    depth_km  = Column(Float, nullable=True)
    magnitude = Column(Float, index=True, nullable=True)

    mag_type_id = Column(Integer, ForeignKey("dim_mag_type.mag_type_id"), index=True, nullable=True)
    place_id    = Column(Integer, ForeignKey("dim_place.place_id"),    index=True, nullable=True)

    tsunami   = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    source    = Column(String(50), nullable=True)

    mag_type = relationship("DimMagType")
    place    = relationship("DimPlace")

    def __repr__(self):
        return f"<FactEvent(event_id='{self.event_id}', magnitude={self.magnitude}, time={self.time_utc})>"

# Composite index for performance on time + magnitude queries
Index("ix_event_time_mag", FactEvent.time_utc, FactEvent.magnitude)

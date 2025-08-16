# tests/test_transform.py

import pandas as pd
import pytest
from etl.transform import validate_df

def test_validate_accepts_reasonable_values():
    """Test that a valid row passes schema and custom validation."""
    df = pd.DataFrame([{
        "event_id": "X",
        "time_utc": pd.Timestamp.utcnow().tz_localize("UTC"),
        "updated_at": pd.Timestamp.utcnow().tz_localize("UTC"),
        "latitude": 0.0,
        "longitude": 0.0,
        "depth_km": 10.0,
        "magnitude": 5.1,
        "mag_type": "MW",
        "raw_place": "Somewhere, Country",
        "region": "Somewhere",
        "country": "Country",
        "tsunami": 0,
        "source": "earthquake"
    }])
    validated = validate_df(df)
    assert not validated.empty, "Expected non-empty DataFrame after validation"

def test_validate_rejects_bad_magnitude():
    """Test that validation fails with magnitude out of range."""
    df = pd.DataFrame([{
        "event_id": "X",
        "time_utc": pd.Timestamp.utcnow().tz_localize("UTC"),
        "updated_at": pd.Timestamp.utcnow().tz_localize("UTC"),
        "latitude": 0.0,
        "longitude": 0.0,
        "depth_km": 10.0,
        "magnitude": 999.0,  # invalid
        "mag_type": "MW",
        "raw_place": "Somewhere, Country",
        "region": "Somewhere",
        "country": "Country",
        "tsunami": 0,
        "source": "earthquake"
    }])
    with pytest.raises(ValueError, match="magnitude out of expected range"):
        validate_df(df)

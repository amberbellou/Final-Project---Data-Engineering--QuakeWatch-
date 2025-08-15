import pandas as pd
from etl.transform import validate_df

def test_validate_accepts_reasonable_values():
    df = pd.DataFrame([{
        "event_id":"X",
        "time_utc":pd.Timestamp.utcnow().tz_localize("UTC"),
        "updated_at":pd.Timestamp.utcnow().tz_localize("UTC"),
        "latitude":0.0,"longitude":0.0,"depth_km":10.0,
        "magnitude":5.1,"mag_type":"MW","raw_place":"Somewhere, Country",
        "region":"Somewhere","country":"Country","tsunami":0,"source":"earthquake"
    }])
    out = validate_df(df)
    assert not out.empty

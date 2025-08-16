# etl/flow.py

import os
import json
import requests
import prefect
from prefect import task, flow
from etl.extract import fetch_events
from etl.transform import features_to_df, validate_df
from etl.load import init_db, upsert_events

# Optional Slack alerting
SLACK_WEBHOOK = os.getenv("PREFECT_SLACK_WEBHOOK_URL")

def notify(msg: str):
    """Send message to Slack if webhook is configured."""
    if SLACK_WEBHOOK:
        try:
            response = requests.post(
                SLACK_WEBHOOK,
                headers={"Content-Type": "application/json"},
                data=json.dumps({"text": msg}),
                timeout=10
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Slack notification failed: {e}")

@task(retries=3, retry_delay_seconds=10, log_prints=True)
def t_extract() -> list:
    return fetch_events()

@task(log_prints=True)
def t_transform(features: list):
    df = features_to_df(features)
    return validate_df(df)

@task(log_prints=True)
def t_load(df):
    init_db()
    upsert_events(df)
    return len(df)

@flow(name="quakewatch-flow")
def run_pipeline():
    logger = prefect.get_run_logger()
    try:
        feats = t_extract()
        df = t_transform(feats)
        n = t_load(df)
        msg = f"✅ QuakeWatch loaded {n} events."
        logger.info(msg)
        notify(msg)
    except Exception as e:
        err = f"❌ QuakeWatch failed: {e}"
        logger.error(err)
        notify(err)
        raise

if __name__ == "__main__":
    run_pipeline()

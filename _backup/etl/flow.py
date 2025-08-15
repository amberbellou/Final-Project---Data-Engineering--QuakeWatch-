import os, json, requests
import prefect
from prefect import task, flow
from etl.extract import fetch_events
from etl.transform import features_to_df, validate_df
from etl.load import init_db, upsert_events

SLACK_WEBHOOK = os.getenv("PREFECT_SLACK_WEBHOOK_URL")

def notify(msg: str):
    try:
        if SLACK_WEBHOOK:
            requests.post(SLACK_WEBHOOK, headers={"Content-Type":"application/json"},
                          data=json.dumps({"text": msg}), timeout=10)
    except Exception:
        pass

@task(retries=3, retry_delay_seconds=10)
def t_extract():
    return fetch_events()

@task
def t_transform(features):
    df = features_to_df(features)
    return validate_df(df)

@task
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
        msg = f"QuakeWatch loaded {n} events"
        logger.info(msg)
        notify(":white_check_mark: " + msg)
    except Exception as e:
        err = f"QuakeWatch failed: {e}"
        logger.error(err)
        notify(":x: " + err)
        raise

if __name__ == "__main__":
    run_pipeline()

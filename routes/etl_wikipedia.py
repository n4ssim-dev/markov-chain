import logging

from fastapi import BackgroundTasks, FastAPI
from etl_wikipedia import DB_PATH, RAW_DIR, main

logger = logging.getLogger("etl_wikipedia")
logging.basicConfig(level=logging.INFO)

router = FastAPI()

_job_running = {"active": False}

def _run_etl():
    _job_running["active"] = True
    try:
        logger.info("ETL job started")
        main()
        logger.info("ETL job finished")
    except Exception:
        logger.exception("ETL job failed")
    finally:
        _job_running["active"] = False


@app.get("/etl/wikipedia")
def etl_wikipedia(background_tasks: BackgroundTasks):
    if _job_running["active"]:
        return {"status": "already running"}

    background_tasks.add_task(_run_etl)
    return {"status": "started"}


@app.get("/etl/wikipedia/status")
def etl_wikipedia_status():
    return {"running": _job_running["active"]}

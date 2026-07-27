import logging

from fastapi import BackgroundTasks, FastAPI
from etl_wikipedia import DB_PATH, RAW_DIR, main

logger = logging.getLogger("etl_wikipedia")
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/")
def next_word_prob(word1:str) -> dict:
    

    return word_prob
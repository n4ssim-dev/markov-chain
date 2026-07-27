import logging

from fastapi import BackgroundTasks, FastAPI
from etl_wikipedia import DB_PATH, RAW_DIR, main

logger = logging.getLogger("etl_wikipedia")
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/next_words")
def highest_next_word_probability(word1:str) -> dict:
    highest_word_probabiltiy = {
            "word1": "I",
            "word 2": "am",
            "occurence": 17 
        }
    
    return highest_word_probabiltiy
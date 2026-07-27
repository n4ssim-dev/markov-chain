from pathlib import Path
import json
import time
from Scrape import Scrape

headers = {
    'User-Agent': 'MarkovChainProject/1.0 (https://github.com/n4ssim-dev/markov-chain);'
}

scraper = Scrape(headers)

# étape 1 : fetch et écriture des pages wikipedia
with open(Path("data/page_list.json"), "r") as f:
    page_list = json.load(f)

noms = [f"{p['nom']}_{p['source']}" for p in page_list]

raw_dir = Path(__file__).parent / "data" / "raw"

for page, nom in zip(page_list, noms):
    target_path = raw_dir / f"{nom}.txt"
    if target_path.is_file():
        continue

    try:
        paragraphs = scraper.fetch_avec_bon_encodage(url=page['url'], headers=headers)
    except Exception as e:
        print(f"failed to fetch {page['url']}: {e}")
        continue

    content = "\n".join(paragraphs)
    scraper.ecrire_txt(content, nom)
    time.sleep(1)

# étape 2 : peuplement de la db 
paragraphs_all = []
for path in raw_dir.glob("*.txt"):
    with open(path, "r", encoding="utf-8") as f:
        paragraphs_all.extend(f.read().split("\n"))

db_path = Path(__file__).parent / "data" / "bigrams.db"
scraper.peupler_db(paragraphs_all, db_path=str(db_path))
print(f"db peuplée : {db_path}")
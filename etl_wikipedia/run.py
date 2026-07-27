import json
import time
from .Scrape import Scrape
from . import RAW_DIR, DB_PATH, PROJECT_ROOT

headers = {
    'User-Agent': 'MarkovChainProject/1.0 (https://github.com/n4ssim-dev/markov-chain);'
}

def main(headers=headers):
    scraper = Scrape(headers)

    with open(PROJECT_ROOT / "data" / "page_list.json", "r") as f:
        page_list = json.load(f)

    noms = [f"{p['nom']}_{p['source']}" for p in page_list]

    for page, nom in zip(page_list, noms):
        target_path = RAW_DIR / f"{nom}.txt"
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

    paragraphs_all = []
    for path in RAW_DIR.glob("*.txt"):
        with open(path, "r", encoding="utf-8") as f:
            paragraphs_all.extend(f.read().split("\n"))

    scraper.peupler_db(paragraphs_all, db_path=str(DB_PATH))
    print(f"db peuplée : {DB_PATH}")

if __name__ == "__main__":
    main()
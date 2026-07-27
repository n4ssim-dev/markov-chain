from bs4 import BeautifulSoup
from charset_normalizer import from_bytes
import sqlite3
import requests
import os
import re
from collections import defaultdict, Counter

class Scrape:
    def __init__(self, headers):
        self.headers = headers

    def fetch_avec_bon_encodage(self, url : str, headers: dict):
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        raw_bytes = response.content

        result = from_bytes(raw_bytes).best()

        if result is not None:
            detected_encoding = result.encoding
            content = raw_bytes.decode(detected_encoding, errors="replace")

            soup : BeautifulSoup = BeautifulSoup(content, features="html.parser")

            p_texts = [p.get_text() for p in soup.find_all('p')]

            return p_texts
        else:
            raise TypeError('N`a pas correctement pu décoder le contenu de la page.')

    def ecrire_txt(self, content : str, nom_fichier : str):
        dir_name = os.path.dirname(__file__)
        file_name = f'data/raw/{nom_fichier}.txt'
        file_path = os.path.join(dir_name, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)

    def concat_txt_files(self, txt_path_list: list):
        concat_text = '';
        for p in txt_path_list:
            with open(p, "r", encoding="utf-8") as f:
                concat_text += '\n' + f.read()
        return concat_text;

    def tokenize(self, text: str) -> list[str]:
        # lowercase sans ponctuation
        return re.findall(r"[a-zàâäéèêëïîôöùûüç0-9]+(?:'[a-zàâäéèêëïîôöùûüç]+)?", text.lower())

    def peupler_db(self, paragraphs: list[str], db_path: str = "bigrams.db"):
        word_id: dict[str, int] = {}
        counts: dict[int, Counter] = defaultdict(Counter)

        def get_id(w: str) -> int:
            if w not in word_id:
                word_id[w] = len(word_id)
            return word_id[w]

        # build bigrams paragraph by paragraph so we don't bridge across them
        for para in paragraphs:
            tokens = self.tokenize(para)
            for a, b in zip(tokens, tokens[1:]):
                counts[get_id(a)][get_id(b)] += 1

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS words (
                id   INTEGER PRIMARY KEY,
                word TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS bigrams (
                w1   INTEGER NOT NULL REFERENCES words(id),
                w2   INTEGER NOT NULL REFERENCES words(id),
                freq INTEGER NOT NULL DEFAULT 1,
                PRIMARY KEY (w1, w2)
            ) WITHOUT ROWID;
        """)

        cur.executemany(
            "INSERT OR IGNORE INTO words(id, word) VALUES (?, ?)",
            [(i, w) for w, i in word_id.items()],
        )

        cur.executemany(
            """INSERT INTO bigrams(w1, w2, freq) VALUES (?, ?, ?)
            ON CONFLICT(w1, w2) DO UPDATE SET freq = freq + excluded.freq""",
            [(w1, w2, f) for w1, sub in counts.items() for w2, f in sub.items()],
        )

        conn.commit()
        conn.close()
            

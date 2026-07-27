from bs4 import BeautifulSoup
import requests

url = 'https://fr.wikipedia.org/wiki/Pain_au_chocolat'
headers = {
    'User-Agent': 'MarkovChainProject/1.0'
}

response = requests.get(url=url)

soup = BeautifulSoup(response.text, features="html.parser")

print(soup.prettify())


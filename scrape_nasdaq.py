import os
import json
from nasdaq_scraper import NasdaqScraper

ARTICLES_JSON_PATH = 'data/articles.json'
RE_SCRAPE = True
OVERWRITE = False

if RE_SCRAPE or not os.path.exists(ARTICLES_JSON_PATH):
    scraper = NasdaqScraper()
    scraper.scrape_articles(n_pages=1, n_tries=3)
    scraper.json_dump_articles(ARTICLES_JSON_PATH, extend=not OVERWRITE)

with open(ARTICLES_JSON_PATH, 'r') as f:
    articles = json.load(f)['articles']

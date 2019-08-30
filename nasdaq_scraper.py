import os
import json
from bs4 import BeautifulSoup
from scraper import Scraper


class NasdaqScraper(Scraper):
    robots_txt_url = 'https://www.nasdaq.com/robots.txt'
    splash_page_n_url = 'https://www.nasdaq.com/news/market-headlines.aspx?page={n}'
    article_div_selector = '#newsContent p'
    article_text_selector = '#articlebody p'

    def __init__(self, html_parser="html.parser"):
        self.html_parser = html_parser
        super().__init__(robots_txt_url=self.robots_txt_url)

        self.article_urls = []
        self.articles = []

    def _scrape_article_urls(self, page=1):
        page_url = self.splash_page_n_url.format(n=page)
        splash_page_html = self.get_page(page_url)
        splash_page_soup = BeautifulSoup(splash_page_html, features=self.html_parser)
        article_divs = splash_page_soup.select(self.article_div_selector)

        urls = []
        for article_div in article_divs:
            article_a_tag = article_div.select('span a')[0]
            article_url = article_a_tag.get_attribute_list('href')[0].strip()
            self.article_urls.append(article_url)

        return urls

    def _scrape_articles(self, n_pages=1):
        for i in range(n_pages):
            self._scrape_article_urls(page=i + 1)

        for article_url in self.article_urls:
            article_html = self.get_page(article_url)
            article_soup = BeautifulSoup(article_html, features=self.html_parser)

            article_title = article_soup.select('title')[0].text
            article_p_tags = article_soup.select(self.article_text_selector)
            article_text = [p_tag.text for p_tag in article_p_tags if p_tag.text.strip()]

            article_dict = {
                'url': article_url,
                'title': article_title,
                'text': article_text,
            }

            self.articles.append(article_dict)

    def scrape_articles(self, n_pages=1, n_tries=5):
        for i in range(n_tries):
            if i:
                print(f'Retry {i} of {n_tries - 1}')

            # noinspection PyBroadException
            try:
                self._scrape_articles(n_pages=n_pages)
                break
            except Exception:
                continue

    def json_dump_articles(self, file_path, extend=False):
        if extend and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                articles = json.load(f)['articles']

            articles.extend(self.articles)
        else:
            articles = self.articles

        articles_dict = {'articles': articles}
        with open(file_path, 'w') as f:
            f.write(json.dumps(articles_dict))

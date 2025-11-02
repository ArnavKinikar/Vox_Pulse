from ddgs import DDGS
from newspaper import Article
import re
import time

from Pipeline.Individual_Items import NewsItem


class NewsScraper:
    def __init__(self, polite_delay=1, max_results=10):
        self.polite_delay = polite_delay
        self.max_results = max_results

    def fetch_articles_from_heading(self, heading):
        """
        Search DuckDuckGo using a news heading and return a list of article URLs.
        """
        print(f"🔍 Searching DuckDuckGo for: {heading}")
        urls = []
        with DDGS() as ddgs:
            for result in ddgs.text(heading):
                urls.append(result['href'])
                if len(urls) >= self.max_results:
                    break
        print(f"Found {len(urls)} URLs for heading: '{heading}'")
        return urls

    def extract_article(self, url):
        """
        Extract clean article text from a URL and return a dictionary.
        """
        try:
            article = Article(url)
            article.download()
            article.parse()
            text = article.text.strip()

            if len(text) < 200:
                return None

            # Clean up the text
            lines = text.splitlines()
            cleaned_lines = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if len(line) < 20:
                    continue
                if re.search(r'https?://\S+|www\.\S+', line):
                    continue
                if re.search(r'\S+@\S+', line):
                    continue
                if re.match(r'(?i)(send an email|click here|subscribe|follow us)', line):
                    continue
                cleaned_lines.append(line)

            cleaned_text = " ".join(cleaned_lines)
            if len(cleaned_text) < 100:
                return None

            return {
                "title": article.title,
                "url": url,
                "text": cleaned_text
            }

        except Exception as e:
            print(f"Failed to parse {url}: {e}")
            return None

    def get_articles_for_heading(self, heading):
        """
        Fetch and parse multiple articles for a given heading.
        Returns a list of article dictionaries.
        """
        urls = self.fetch_articles_from_heading(heading)
        NewsItem(url=urls);
        articles = []

        for i, url in enumerate(urls, start=1):
            print(f"[{i}/{len(urls)}] Fetching article: {url}")
            data = self.extract_article(url)
            if data:
                articles.append(data)
            time.sleep(self.polite_delay)

        print(f"✅ Successfully extracted {len(articles)} articles for '{heading}'")
        return articles

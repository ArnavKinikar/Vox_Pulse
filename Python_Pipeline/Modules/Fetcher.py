import requests
from Pipeline.Individual_Items import NewsItem
from Pipeline.Config import NEWS_API_KEY

class NewsFetcher:
    """
    Fetches news titles (and optional URLs) from the NewsAPI.
    """

    def __init__(self, api_key=NEWS_API_KEY):
        self.api_key = api_key
        self.news_items = []

    def fetch_titles(self, country=None, category=None, query=None, page_size=10):
        """
        Fetch current top headlines from NewsAPI and store as NewsItem objects.
        """
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": self.api_key,
            "country": country,
            "pageSize": page_size
        }

        if category:
            params["category"] = category
        if query:
            params["q"] = query

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200 or "articles" not in data:
            print("Failed to fetch news:", data)
            return []

        for article in data["articles"]:
            title = article.get("title")
            url = article.get("url")
            if title:
                self.news_items.append(NewsItem(title=title))

        print(f"Fetched {len(self.news_items)} titles from NewsAPI")
        return self.news_items

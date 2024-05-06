from goose3 import Goose
from googlesearch import search

# Initialize Goose for extracting content from articles
g = Goose()


def extract_content(article_url):
    try:
        # Extract content from the given article URL
        content = g.extract(article_url)
        return {"title": content.title, "content": content.cleaned_text}
    except Exception as e:
        print(f"Error extracting text from article: {e}")


def fetch_urls(user_query, start=1, stop=2):
    articles = []
    try:
        # Perform Google search to fetch URLs related to user query
        for url in search(user_query,num_results=start):
            articles.append(url)
        # print(articles)
    except Exception as e:
        print(f"Error fetching articles: {e}")
    return list(set(articles))

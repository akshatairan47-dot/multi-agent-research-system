from langchain.tools import tool 
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import os 
from dotenv import load_dotenv
from rich import print
load_dotenv()

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs and snippets."""
    out = []
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
    for r in results:
        out.append(
            f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body'][:300]}\n"
        )
    return "\n----\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"


from urllib.parse import urlparse

def extract_arxiv_metadata(url):

    return {
        "url": url,
        "type": "research_paper",
        "title": None,
        "description": None,
        "thumbnail": None,
        "source": urlparse(url).netloc
    }
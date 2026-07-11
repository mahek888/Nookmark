from urllib.parse import urlparse

def extract_youtube_metadata(url):

    return {
        "url": url,
        "type": "youtube",
        "title": None,
        "description": None,
        "thumbnail": None,
        "source": urlparse(url).netloc
    }
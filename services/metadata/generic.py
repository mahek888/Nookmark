import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_title(soup):

    og_title = soup.find("meta", property="og:title")

    if og_title and og_title.get("content"):
        return og_title["content"].strip()

    if soup.title and soup.title.string:
        return soup.title.string.strip()

    return "No title found"


def get_description(soup):

    og_description = soup.find(
        "meta",
        property="og:description"
    )

    if og_description and og_description.get("content"):
        return og_description["content"].strip()

    meta_description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if meta_description and meta_description.get("content"):
        return meta_description["content"].strip()

    return "No description available"


def get_thumbnail(soup):

    og_image = soup.find(
        "meta",
        property="og:image"
    )

    if og_image and og_image.get("content"):
        return og_image["content"].strip()

    return None


def extract_generic_metadata(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

    except requests.RequestException:

        return None

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    return {
        "url": url,
        "type": "generic",
        "title": get_title(soup),
        "description": get_description(soup),
        "thumbnail": get_thumbnail(soup),
        "source": urlparse(url).netloc
    }
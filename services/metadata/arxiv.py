import feedparser
from urllib.parse import urlparse


def extract_arxiv_metadata(url):

    parsed = urlparse(url)

    paper_id = parsed.path.split("/")[-1]

    api = f"https://export.arxiv.org/api/query?id_list={paper_id}"

    feed = feedparser.parse(api)

    if not feed.entries:
        return None

    paper = feed.entries[0]

    authors = ", ".join(author.name for author in paper.authors)

    return {

        "url": url,

        "type": "research_paper",

        "title": paper.title,

        "description": paper.summary,

        "thumbnail": None,

        "source": "arXiv",

        "authors": authors,

        "published": paper.published,

        "category": paper.tags[0]["term"] if hasattr(paper, "tags") else None
    }
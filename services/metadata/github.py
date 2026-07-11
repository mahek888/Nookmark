from urllib.parse import urlparse




def extract_repo_metadata(url):

    return {
        "url": url,
        "type": "github_repo",
        "title": None,
        "description": None,
        "thumbnail": None,
        "source": urlparse(url).netloc
    }


def extract_profile_metadata(url):

    return {
        "url": url,
        "type": "github_profile",
        "title": None,
        "description": None,
        "thumbnail": None,
        "source": urlparse(url).netloc
    }
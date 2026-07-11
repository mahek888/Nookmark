from urllib.parse import urlparse

def detect_resource_type(url):
    parsed_url = urlparse(url)

    domain = parsed_url.netloc.lower()
    path = parsed_url.path.lower()

    if "youtube.com" in domain or "youtu.be" in domain:
        return "youtube"

    elif "github.com" in domain:
        path_parts = [part for part in path.strip("/").split("/") if part]

        if len(path_parts) == 1:
            return "github_profile"

        elif len(path_parts) >= 2:
            return "github_repo"

        return "github"

    elif "arxiv.org" in domain:
        return "research_paper"

    return "generic"
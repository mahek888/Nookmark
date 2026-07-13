import requests
from urllib.parse import urlparse


HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Nookmark"
}


def extract_github_repo_metadata(url):

    parsed = urlparse(url)

    path = parsed.path.strip("/")

    owner, repo = path.split("/")[:2]

    api = f"https://api.github.com/repos/{owner}/{repo}"

    try:

        response = requests.get(
            api,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException:

        return None

    return {

        "url": url,

        "type": "github_repo",

        "title": data["full_name"],

        "description": data["description"],

        "thumbnail": data["owner"]["avatar_url"],

        "source": "GitHub",

        "owner": owner,

        "stars": data["stargazers_count"],

        "language": data["language"],

        "archived": data["archived"],

        "last_updated": data["updated_at"]
    }


def extract_github_profile_metadata(url):

    parsed = urlparse(url)

    username = parsed.path.strip("/")

    api = f"https://api.github.com/users/{username}"

    try:

        response = requests.get(
            api,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException:

        return None

    return {

        "url": url,

        "type": "github_profile",

        "title": data["login"],

        "description": data["bio"],

        "thumbnail": data["avatar_url"],

        "source": "GitHub",

        "followers": data["followers"],

        "following": data["following"],

        "public_repos": data["public_repos"]
    }
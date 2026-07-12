import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def normalize_url(url):
    """
    Normalizes a URL for duplicate detection.
    """

    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower().replace("www.", "")
    path = parsed.path.rstrip("/")

    query = parse_qs(parsed.query)

    # Remove tracking parameters
    tracking_params = [
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
        "fbclid",
        "gclid"
    ]

    for param in tracking_params:
        query.pop(param, None)

    normalized_query = urlencode(query, doseq=True)

    return urlunparse((
        scheme,
        netloc,
        path,
        "",
        normalized_query,
        ""
    ))


def find_duplicate_resources(resources):
    """
    Returns a list of duplicate resources.
    """

    seen = set()
    duplicates = []

    for resource in resources:

        normalized = normalize_url(resource["url"])

        if normalized in seen:
            duplicates.append(resource)

        else:
            seen.add(normalized)

    return duplicates


def remove_duplicate_resources(resources):
    """
    Returns a new list with duplicates removed.
    """

    unique_resources = []
    seen = set()

    for resource in resources:

        normalized = normalize_url(resource["url"])

        if normalized not in seen:

            seen.add(normalized)
            unique_resources.append(resource)

    return unique_resources


def is_dead_link(url):
    """
    Checks whether a URL is reachable.
    """

    try:

        response = requests.head(
            url,
            allow_redirects=True,
            timeout=5
        )

        return response.status_code >= 400

    except requests.RequestException:

        return True


def find_dead_links(resources):
    """
    Returns all resources whose links are dead.
    """

    dead_resources = []

    for resource in resources:

        if is_dead_link(resource["url"]):
            dead_resources.append(resource)

    return dead_resources


def find_outdated_resources(resources):
    """
    Placeholder heuristic.

    Currently only flags archived GitHub repositories.
    More rules will be added later.
    """

    outdated = []

    for resource in resources:

        if resource["type"] == "github_repo":

            if resource.get("archived", False):
                outdated.append(resource)

    return outdated


def reduce_knowledge_debt(resources):
    """
    Performs all cleanup operations.
    """

    resources = remove_duplicate_resources(resources)

    dead = find_dead_links(resources)

    outdated = find_outdated_resources(resources)

    duplicates = find_duplicate_resources(resources)

    clean_resources = remove_duplicate_resources(resources)

    return {
        "resources": resources,
        "dead_links": dead,
        "outdated": outdated,
        "duplicates_removed": len(duplicates)
    }
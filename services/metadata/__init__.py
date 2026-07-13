from .detector import detect_resource_type

from .generic import extract_generic_metadata

from .github import (
    extract_github_repo_metadata,
    extract_github_profile_metadata
)

from .youtube import extract_youtube_metadata
from .arxiv import extract_arxiv_metadata


def extract_metadata(url):

    resource_type = detect_resource_type(url)

    if resource_type == "generic":
        return extract_generic_metadata(url)

    elif resource_type == "github_repo":
        return extract_github_repo_metadata(url)

    elif resource_type == "github_profile":
        return extract_github_profile_metadata(url)

    elif resource_type == "youtube":
        return extract_youtube_metadata(url)

    elif resource_type == "research_paper":
        return extract_arxiv_metadata(url)

    return None
import json
import uuid
from pathlib import Path
from datetime import datetime

from services.scoring import calculate_priority_score
from services.metadata import extract_metadata
from urllib.parse import urlparse

DATA_FILE = Path("data/resources.json")

def load_resources():

    try:

        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        return []
    
def save_resources(resources):

    with open(DATA_FILE, "w", encoding="utf-8") as file:

        json.dump(
            resources,
            file,
            indent=4,
            ensure_ascii=False
        )

def add_resource(url):

    if not is_valid_url(url):

        return None

    resources = load_resources()

    metadata = extract_metadata(url)

    if metadata is None:
        return None
    
    resource = metadata.copy()

    resource["details"] = []

    if resource["type"] == "github_repo":

        resource["details"] = [

            f"⭐ {resource.get('stars', 0)} Stars",

            resource.get("language", "Unknown Language"),

            "Archived"
            if resource.get("archived")
            else "Active Repository"

        ]

    elif resource["type"] == "github_profile":

        resource["details"] = [

            f"👥 {resource.get('followers',0)} Followers",

            f"📦 {resource.get('public_repos',0)} Public Repositories"

        ]

    elif resource["type"] == "research_paper":

        details = []

        if resource.get("authors"):
            details.append(resource["authors"])

        if resource.get("published"):
            details.append(resource["published"][:10])

        if resource.get("category"):
            details.append(resource["category"])

        resource["details"] = details

    elif resource["type"] == "youtube":

        resource["details"] = [

            "YouTube Video"

        ]

    else:

        resource["details"] = []

    resource["id"] = str(uuid.uuid4())

    resource["status"] = "saved"

    resource["priority_score"] = calculate_priority_score(resource)

    resource["knowledge_cluster"] = None

    resource["estimated_time"] = None

    resource["notes"] = ""

    resource["completed_at"] = None

    resource["date_added"] = datetime.now().isoformat(timespec="seconds")

    resources.append(resource)

    save_resources(resources)

    return resource

def is_valid_url(url):

    parsed = urlparse(url)

    return parsed.scheme in ("http", "https") and parsed.netloc != ""

def delete_resource(resource_id):


    resources = load_resources()

    resources = [

        resource

        for resource in resources

        if resource["id"] != resource_id

    ]

    save_resources(resources)

def get_resource(resource_id):

    resources = load_resources()

    for resource in resources:

        if resource["id"] == resource_id:

            return resource

    return None

def update_status(resource_id, status):

    resources = load_resources()

    for resource in resources:

        if resource["id"] == resource_id:

            resource["status"] = status

            break

    save_resources(resources)

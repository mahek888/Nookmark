import json
import uuid
from pathlib import Path
from datetime import datetime

from services.metadata import extract_metadata

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

    resources = load_resources()

    metadata = extract_metadata(url)

    if metadata is None:
        return None
    
    resource = {

        "id": str(uuid.uuid4()),

        "url": metadata["url"],

        "type": metadata["type"],

        "title": metadata["title"],

        "description": metadata["description"],

        "thumbnail": metadata["thumbnail"],

        "source": metadata["source"],

        "status": "saved",

        "priority_score": 0,

        "knowledge_cluster": None,

        "notes": "",

        "date_added": datetime.now().isoformat(timespec="seconds"),

        "estimated_time": None,

        "completed_at": None,

        "topic": None
    }

    resources.append(resource)

    save_resources(resources)

    return resource

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

            save_resources(resources)

            return resource

    return None
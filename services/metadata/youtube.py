import os
import requests

from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")


def extract_video_id(url):

    parsed = urlparse(url)

    if parsed.hostname == "youtu.be":

        return parsed.path[1:]

    if "youtube.com" in parsed.hostname:

        return parse_qs(parsed.query).get("v", [None])[0]

    return None


def extract_youtube_metadata(url):

    video_id = extract_video_id(url)

    if video_id is None:

        return None

    endpoint = "https://www.googleapis.com/youtube/v3/videos"

    params = {

        "part": "snippet,contentDetails,statistics",

        "id": video_id,

        "key": API_KEY

    }

    response = requests.get(endpoint, params=params)

    if response.status_code != 200:

        return None

    data = response.json()

    if not data["items"]:

        return None

    item = data["items"][0]

    snippet = item["snippet"]

    details = item["contentDetails"]

    stats = item["statistics"]

    metadata = {

        "url": url,

        "type": "youtube",

        "title": snippet["title"],

        "description": snippet["description"],

        "thumbnail": snippet["thumbnails"]["high"]["url"],

        "source": "YouTube",

        "channel": snippet["channelTitle"],

        "published": snippet["publishedAt"],

        "duration": details["duration"],

        "estimated_time": duration_to_minutes(
            details["duration"]
        ),

        "views": stats.get("viewCount", "0"),

        "details": [

            f"📺 {snippet['channelTitle']}",

            f"👀 {int(stats.get('viewCount',0)):,} views",

            f"⏱ {details['duration']}",

            f"📅 {snippet['publishedAt'][:10]}"

        ]

    }

    return metadata

import re

def duration_to_minutes(duration):

    hours = 0
    minutes = 0
    seconds = 0

    h = re.search(r'(\d+)H', duration)
    m = re.search(r'(\d+)M', duration)
    s = re.search(r'(\d+)S', duration)

    if h:
        hours = int(h.group(1))

    if m:
        minutes = int(m.group(1))

    if s:
        seconds = int(s.group(1))

    total = hours * 60 + minutes

    if seconds >= 30:
        total += 1

    return total
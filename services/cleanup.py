import requests


def remove_duplicates(resources):

    seen = set()

    cleaned = []

    for resource in resources:

        url = resource["url"].strip().lower()

        if url not in seen:

            seen.add(url)

            cleaned.append(resource)

    return cleaned


def remove_dead_links(resources):

    alive = []

    for resource in resources:

        try:

            response = requests.head(
                resource["url"],
                timeout=5,
                allow_redirects=True
            )

            if response.status_code < 400:

                alive.append(resource)

        except:

            pass

    return alive


def reduce_knowledge_debt(resources):

    resources = remove_duplicates(resources)

    resources = remove_dead_links(resources)

    return resources
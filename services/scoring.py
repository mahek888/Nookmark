from datetime import datetime


def calculate_priority_score(resource):

    score = 50

    resource_type = resource.get("type")

    if resource_type == "research_paper":
        score += 20

    elif resource_type == "documentation":
        score += 15

    elif resource_type == "github_repo":
        score += 10

    elif resource_type == "youtube":
        score += 5

    status = resource.get("status", "saved")

    if status == "saved":
        score += 20

    elif status == "in_progress":
        score += 10

    elif status == "completed":
        score = 0

    if resource.get("archived"):
        score -= 30

    return max(0, min(score, 100))


def calculate_knowledge_debt(resources):

    if not resources:
        return 0

    total = 0

    for resource in resources:

        total += calculate_priority_score(resource)

    return round(total / len(resources))
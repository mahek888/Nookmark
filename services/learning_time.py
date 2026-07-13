def estimate_resource_time(resource):

    if resource.get("estimated_time"):

        return resource["estimated_time"]

    resource_type = resource["type"]

    if resource_type == "research_paper":

        return 45

    elif resource_type == "github_repo":

        return 30

    elif resource_type == "github_profile":

        return 10

    else:

        return 15


def total_learning_time(resources):

    total = 0

    for resource in resources:

        total += estimate_resource_time(resource)

    return total
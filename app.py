from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from services.resource_manager import (
    add_resource,
    load_resources,
    save_resources
)

from services.cleanup import reduce_knowledge_debt

from services.scoring import (
    calculate_priority_score,
    calculate_knowledge_debt
)

# from services.ai import generate_learning_roadmap

from services.resource_manager import update_status

from services.resource_manager import delete_resource

from services.learning_time import total_learning_time

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():

    urls = request.form["urls"]

    url_list = urls.splitlines()

    invalid_urls = []
    added_urls = []

    for url in url_list:

        url = url.strip()

        if not url:
            continue

        if add_resource(url):

            added_urls.append(url)

        else:

            invalid_urls.append(url)

    if invalid_urls:

        return render_template(
            "index.html",
            error=(
                f"✅ Added {len(added_urls)} resource(s). "
                f"❌ Invalid URL(s): {', '.join(invalid_urls)}"
            )
        )

    return redirect(url_for("dashboard"))



@app.route("/dashboard")
def dashboard():

    resources = load_resources()

    # Recalculate priority scores
    for resource in resources:
        resource["priority_score"] = calculate_priority_score(resource)

    save_resources(resources)

    debt_score = calculate_knowledge_debt(resources)

    learning_minutes = total_learning_time(resources)

    hours = learning_minutes // 60

    minutes = learning_minutes % 60

    learning_time = f"{hours}h {minutes}m"

    completed = sum(
        1 for resource in resources
        if resource["status"] == "completed"
    )

    in_progress = sum(
        1 for resource in resources
        if resource["status"] == "in_progress"
    )

    saved = sum(
        1 for resource in resources
        if resource["status"] == "saved"
    )

    high_priority = sum(
        1 for resource in resources
        if resource["priority_score"] >= 80
    )

    # Resource type counts
    resource_types = {}

    for resource in resources:

        resource_type = resource["type"]

        resource_types[resource_type] = (
            resource_types.get(resource_type, 0) + 1
        )

    # Priority distribution
    high = sum(
        1 for r in resources
        if r["priority_score"] >= 80
    )

    medium = sum(
        1 for r in resources
        if 50 <= r["priority_score"] < 80
    )

    low = sum(
        1 for r in resources
        if r["priority_score"] < 50
    )

    return render_template(
        "dashboard.html",

        resources=resources,

        debt_score=debt_score,

        high_priority=high_priority,

        completed=completed,

        in_progress=in_progress,

        saved=saved,

        learning_time=learning_time,

        resource_types=resource_types,

        high=high,

        medium=medium,

        low=low
    )


@app.route("/reduce-knowledge-debt", methods=["POST"])
def reduce_knowledge_debt_route():

    resources = load_resources()

    resources = reduce_knowledge_debt(resources)

    # Recalculate priorities after cleanup
    for resource in resources:

        resource["priority_score"] = calculate_priority_score(resource)

    save_resources(resources)

    return redirect(url_for("dashboard"))

# WIP
# @app.route("/roadmap", methods=["POST"])

# def roadmap():

#     resources = load_resources()

#     roadmap = generate_learning_roadmap(resources)

#     return render_template(

#         "roadmap.html",

#         roadmap=roadmap
#     )

@app.route("/update-status/<resource_id>", methods=["POST"])
def update_resource_status(resource_id):

    status = request.form["status"]

    update_status(resource_id, status)

    return redirect(url_for("dashboard"))

@app.route("/delete/<resource_id>", methods=["POST"])
def delete(resource_id):

    delete_resource(resource_id)

    return redirect(url_for("dashboard"))


if __name__ == "__main__":

    app.run(debug=True)
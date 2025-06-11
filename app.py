import os
import requests
from flask import Flask, render_template_string

app = Flask(__name__)

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

auth = None
if JIRA_EMAIL and JIRA_API_TOKEN:
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)


def get_releases():
    """Return a list of versions (releases) for the project."""
    if not (JIRA_BASE_URL and JIRA_PROJECT_KEY):
        return []
    url = f"{JIRA_BASE_URL}/rest/api/3/project/{JIRA_PROJECT_KEY}/versions"
    resp = requests.get(url, auth=auth)
    resp.raise_for_status()
    return resp.json()


def get_issues_for_release(version_name):
    """Return issues associated with a release (version)."""
    if not JIRA_BASE_URL:
        return []
    jql = f'fixVersion="{version_name}"'
    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    params = {"jql": jql, "fields": "status"}
    resp = requests.get(url, auth=auth, params=params)
    resp.raise_for_status()
    return resp.json().get("issues", [])


def calculate_progress(issues):
    """Calculate progress value 0..1 for a list of issues."""
    total = len(issues)
    if total == 0:
        return 0
    score = 0
    for issue in issues:
        status_name = issue["fields"]["status"]["name"].upper()
        if status_name == "DONE":
            score += 100
        elif status_name in {"INPROGRESS", "IN PROGRESS"}:
            score += 50
    return score / (100 * total)


@app.route("/")
def index():
    releases = get_releases()
    data = []
    for release in releases:
        issues = get_issues_for_release(release["name"])
        progress = calculate_progress(issues)
        data.append({"name": release["name"], "progress": progress})
    html = """
    <h1>Release Progress</h1>
    <table border="1">
        <tr><th>Release</th><th>Progress</th></tr>
        {% for r in data %}
        <tr><td>{{ r.name }}</td><td>{{ '%0.2f' % (r.progress * 100) }}%</td></tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, data=data)


if __name__ == "__main__":
    app.run(debug=True)

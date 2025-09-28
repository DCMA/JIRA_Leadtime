# JIRA Leadtime

This repository contains a small Flask application that displays the
progress for each JIRA release (version). Progress is determined using
the following rules:

- Issues in **DONE** count as 100% complete.
- Issues in **INPROGRESS** (or "IN PROGRESS") count as 50% complete.
- Issues in **TODO** count as 0% complete.

For each release, the overall progress is calculated as:

```
progress = (100 * number_of_done_issues +
            50 * number_of_inprogress_issues) /
           (100 * total_number_of_issues)
```

For example, if a release has three issues, two in `INPROGRESS` and one
in `TODO`, progress will be `(50*2 + 0) / 300 = 0.33` (33%).

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Provide JIRA connection information via environment variables:

- `JIRA_BASE_URL` – base URL to your JIRA instance (e.g.
  `https://your-domain.atlassian.net`)
- `JIRA_EMAIL` – your JIRA account email
- `JIRA_API_TOKEN` – API token for authentication
- `JIRA_PROJECT_KEY` – project key to query

3. Run the application:

```bash
python app.py
```

Then open `http://localhost:5000/` in your browser to see the progress
for each release.

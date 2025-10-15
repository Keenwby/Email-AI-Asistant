# n8n Workflow Notes

The repository ships with sample n8n workflows under `workflows/`. Import them into your n8n instance to bootstrap orchestration.

## Recruiter Insights Collector

* **Manual Trigger** – start the flow on demand while iterating on filters.
* **Gmail - Fetch Messages** – runs the same recruiter query as the Python CLI. Adjust the `q` parameter to narrow or expand the search.
* **Transform to Insights** – mirrors the Python `extract_recruiter_insights` helper, implemented as a JavaScript Function node.
* **Google Sheets - Append** – persists the structured data to Google Sheets so you can pivot or share the report quickly.

### Suggested enhancements

1. Replace the manual trigger with a Cron node to run daily.
2. Add an HTTP Request node that enriches companies with data from services like Clearbit or People Data Labs.
3. Attach a Slack node to post a digest of new recruiters and job links.

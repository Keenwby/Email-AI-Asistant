---
title: User Guide
---

# Email AI Assistant – User Guide

This guide walks analysts and operators through running the assistant, interpreting reports, and sharing results. It assumes no deep knowledge of the codebase.

## Before You Start

| Requirement | Why It Matters | How to Check |
| ----------- | -------------- | ------------ |
| Python environment | CLI runs with Python 3.10+ | `python --version` |
| Dependencies installed | Ensures CLI and reporting utilities are available | `pip install -e .[dev]` (once per machine) |
| Gmail API credentials | Required for read-only access to Gmail data | Confirm `~/.credentials/email-ai-assistant/credentials.json` exists |
| `.env` configured | Supplies email address and credential path | Open `.env` and verify `PRIMARY_EMAIL` & `GOOGLE_APPLICATION_CREDENTIALS` |

## Running Reports

### Recruiter Insights

```bash
python scripts/run_mvp.py recruiters
```

- **What it does**: Finds recruiter-oriented emails (default query `from:(recruiter OR talent) has:attachment`), extracts company names and job links, and writes a Markdown report.
- **Where it lands**: `reports/recruiter_insights.md` (override with `--output-dir`).
- **When to tweak**: Adjust `--query` to narrow roles, locations, or companies (e.g., `--query "from:recruiter@example.com newer_than:6m"`).

### Subscription Summary

```bash
python scripts/run_mvp.py subscriptions
```

- **What it does**: Groups promotional emails by sender to highlight recurring newsletters or alerts.
- **Where it lands**: `reports/subscription_summary.md`.
- **Options**: Use `--limit` to cap the number of senders or `--query` to focus on specific labels/categories.

### Export Raw Messages

```bash
python scripts/run_mvp.py export-messages "<gmail-query>" --output reports/messages.json --limit 50
```

- **Use this when** you need to debug analyzer behavior or feed the data into another tool.
- **Output**: JSON file containing the raw Gmail payload for inspection or ad-hoc analysis.

## Interpreting Reports

| Report | Key Columns | How to Use |
| ------ | ----------- | ---------- |
| `recruiter_insights.md` | Subject, Sender, Company, Job Links, Received At | Prioritize follow-ups, track active pipelines, store links in a candidate tracker. |
| `subscription_summary.md` | Sender, Subject Example, Message Count | Identify noisy newsletters for potential unsubscribe automations. |

Tips:

- Sort the Markdown table in spreadsheet tools if you need more advanced filtering.
- `Job Links` may contain multiple URLs; scan for duplicates or long redirect URLs when sharing externally.

## Sharing Results

1. Open the Markdown report in VS Code or a Markdown viewer.
2. Copy the rendered table into Google Docs/Sheets if collaboration is needed.
3. Archive the report in a shared drive or wiki so stakeholders can track historical trends.

## Troubleshooting

| Issue | Likely Cause | Fix |
| ----- | ------------ | --- |
| OAuth browser window never opens | Local firewall or CLI running on remote host | Rerun command locally or ensure ports are open. |
| `google-auth` errors about expired token | `token.json` is stale | Delete `token.json` and rerun the command to re-authenticate. |
| Report file missing | Wrong output directory or permissions | Pass `--output-dir` to a writable location (e.g., `--output-dir ~/Desktop/reports`). |
| Empty report | Gmail query matches zero messages | Relax the search query or increase date range. |

## Automation via n8n

- Import `workflows/recruiter_insights.json` into n8n.
- Update Gmail credentials in the workflow and customize nodes for Sheets or Slack.
- Schedule the flow with a Cron node to receive daily or weekly digests.

## Need Help?

- Engineers: refer to the [System Introduction](../ghp/index.md).
- Operators: capture new questions here so we can expand this guide over time.

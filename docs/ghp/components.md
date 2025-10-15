---
title: Component Catalog
---

# Component Catalog

This section gives you a “what & why” breakdown of every major unit in the system. Use it as a map when you dive into the code.

## Runtime Components

| Component | Location | What it does | Why it exists | Key Dependencies |
| --------- | -------- | ------------ | ------------- | ---------------- |
| `GmailClient` | `src/email_ai_assistant/gmail_client.py` | Handles OAuth, wraps Gmail REST API, normalizes messages into `GmailMessage`. | Centralizes Google client usage and keeps analyzers decoupled from API noise. | `google-api-python-client`, `google-auth-oauthlib`, `python-dateutil` |
| `GmailMessage` | `src/email_ai_assistant/gmail_client.py` | Dataclass representing the subset of message fields the MVP needs. | Provides a stable contract for analyzers and reporters. | Python `dataclasses`, `datetime` |
| `Settings` | `src/email_ai_assistant/config.py` | Loads environment variables, enforces validation, caches settings. | Ensures consistent configuration across CLI and workflows. | `pydantic` |
| Recruiter Analyzer | `src/email_ai_assistant/analyzers/recruiter.py` | Extracts company names and job links from recruiter emails. | Delivers structured recruiter insights for reports or downstream enrichment. | Python `re` |
| Subscription Analyzer | `src/email_ai_assistant/analyzers/subscriptions.py` | Aggregates sender frequencies to surface high-volume newsletters. | Quantifies inbox clutter and future unsubscribe targets. | Python `collections.Counter` |
| `ReportBuilder` | `src/email_ai_assistant/reporting.py` | Renders analyzer output as Markdown tables and writes them to disk. | Provides human-readable artifacts for sharing and auditing. | `tabulate` (optional) |
| Typer CLI | `scripts/run_mvp.py` | Entry point exposing recruiter, subscription, and raw export commands. | Enables ad-hoc runs without n8n; orchestrates settings + components. | `typer`, `email_ai_assistant` package |

## Support Components

| Component | Location | What it does | Key Points |
| --------- | -------- | ------------ | ---------- |
| Test Suite | `tests/` | Validates analyzers and report formatting. | Run `pytest`; no live Gmail access required thanks to dataclass fixtures. |
| Documentation | `docs/` | Architecture notes (`architecture.md`), workflow instructions (`workflow.md`), and this GHP pack (`docs/ghp/`). | GitHub Pages compatible; start with `docs/ghp/index.md`. |
| Workflows | `workflows/recruiter_insights.json` | n8n export mirroring the recruiter pipeline. | Update Gmail node credentials; extend with Sheets/Slack nodes. |
| Scripts | `scripts/` | CLI wrappers and future automation helpers. | Keep side-effectful automation separate from `src/`. |

## Extension Points

- **New analyzers** – create a module under `email_ai_assistant/analyzers/`, expose a dataclass result, and register it via CLI or workflow.
- **Alternative outputs** – extend `ReportBuilder` to emit CSV or integrate with the Sheets API.
- **Workflow automations** – add n8n flows that call the CLI via the `Execute Command` node or reconstruct the pipeline using Function nodes.

Next: follow the data end-to-end in [Data Flow & Execution](data-flow.md).

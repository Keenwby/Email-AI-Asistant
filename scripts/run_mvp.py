"""Command-line entry point for the Email AI Assistant MVP."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import typer

from email_ai_assistant import GmailClient, ReportBuilder
from email_ai_assistant.analyzers.recruiter import extract_recruiter_insights
from email_ai_assistant.analyzers.subscriptions import summarize_subscriptions
from email_ai_assistant.config import get_settings

app = typer.Typer(add_completion=False, help="Email AI Assistant MVP commands")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


@app.command()
def recruiters(
    query: str = typer.Option(
        "from:(recruiter OR talent) has:attachment",
        help="Gmail search query that identifies recruiter emails.",
    ),
    output_dir: Path = typer.Option(Path("reports"), help="Directory where reports will be written."),
) -> None:
    """Generate recruiter insights report."""

    settings = get_settings()
    client = GmailClient(credentials_path=str(settings.google_application_credentials))
    messages = client.list_messages(query=query)
    insights = extract_recruiter_insights(messages)
    report = ReportBuilder(output_dir=output_dir)
    path = report.write_table(
        "recruiter_insights",
        insights,
        headers={
            "subject": "Subject",
            "sender": "Sender",
            "company": "Company",
            "job_links": "Job Links",
            "received_at": "Received At",
        },
    )
    typer.echo(f"Recruiter insights written to {path}")


@app.command()
def subscriptions(
    query: str = typer.Option(
        "category:promotions newer_than:1y",
        help="Gmail search query that identifies newsletter/subscription emails.",
    ),
    output_dir: Path = typer.Option(Path("reports"), help="Directory where reports will be written."),
    limit: int = typer.Option(50, help="Maximum number of senders to display."),
) -> None:
    """Summarize subscription usage."""

    settings = get_settings()
    client = GmailClient(credentials_path=str(settings.google_application_credentials))
    messages = client.list_messages(query=query, max_results=500)
    insights = summarize_subscriptions(messages)[:limit]
    report = ReportBuilder(output_dir=output_dir)
    path = report.write_table(
        "subscription_summary",
        insights,
        headers={
            "sender": "Sender",
            "subject_example": "Subject Example",
            "message_count": "Message Count",
        },
    )
    typer.echo(f"Subscription summary written to {path}")


@app.command()
def export_messages(
    query: str = typer.Argument(..., help="Gmail search query for raw message export."),
    output: Path = typer.Option(Path("reports/messages.json"), help="Path to write JSON payload."),
    limit: int = typer.Option(100, help="Maximum number of messages to export."),
) -> None:
    """Export raw Gmail messages for ad-hoc analysis."""

    settings = get_settings()
    client = GmailClient(credentials_path=str(settings.google_application_credentials))
    messages = client.list_messages(query=query, max_results=limit)
    serializable = [message.__dict__ for message in messages]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(serializable, indent=2, default=str), encoding="utf-8")
    typer.echo(f"Exported {len(messages)} messages to {output}")


if __name__ == "__main__":
    app()

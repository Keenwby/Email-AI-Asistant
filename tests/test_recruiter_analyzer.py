from datetime import datetime, timezone

from email_ai_assistant.analyzers.recruiter import extract_recruiter_insights
from email_ai_assistant.gmail_client import GmailMessage


def make_message(subject: str, body: str = "", sender: str = "recruiter@example.com") -> GmailMessage:
    return GmailMessage(
        id="1",
        thread_id="t1",
        subject=subject,
        sender=sender,
        received_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        snippet="snippet",
        body=body,
    )


def test_extracts_company_from_subject():
    message = make_message("Exciting role at OpenAI", "Body text")

    insights = extract_recruiter_insights([message])

    assert insights[0].company == "OpenAI"


def test_extracts_job_links_from_body():
    body = "Check https://example.com/jobs/123 and https://careers.example.com/apply"
    message = make_message("Opportunity", body)

    insights = extract_recruiter_insights([message])

    assert insights[0].job_links == [
        "https://example.com/jobs/123",
        "https://careers.example.com/apply",
    ]

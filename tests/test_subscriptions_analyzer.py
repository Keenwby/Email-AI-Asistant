from datetime import datetime, timezone

from email_ai_assistant.analyzers.subscriptions import summarize_subscriptions
from email_ai_assistant.gmail_client import GmailMessage


def make_message(sender: str, subject: str) -> GmailMessage:
    return GmailMessage(
        id=f"{sender}-{subject}",
        thread_id="t1",
        subject=subject,
        sender=sender,
        received_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        snippet="snippet",
        body="Body",
    )


def test_summarize_subscriptions_orders_by_frequency():
    messages = [
        make_message("newsletter@example.com", "Issue 1"),
        make_message("newsletter@example.com", "Issue 2"),
        make_message("alerts@example.com", "Alert"),
    ]

    summaries = summarize_subscriptions(messages)

    assert summaries[0].sender == "newsletter@example.com"
    assert summaries[0].message_count == 2
    assert summaries[1].sender == "alerts@example.com"
    assert summaries[1].message_count == 1

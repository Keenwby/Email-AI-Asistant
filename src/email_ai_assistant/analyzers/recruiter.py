"""Recruiter email analytics."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List, Optional

from ..gmail_client import GmailMessage

COMPANY_PATTERN = re.compile(r"\b(?:at|from)\s+(?P<company>[A-Z][A-Za-z0-9&'\- ]+)\b")
JD_PATTERN = re.compile(r"https?://\S+(?:jobs?|careers|apply)\S*", re.IGNORECASE)


@dataclass
class RecruiterInsight:
    """Structured information about a recruiter email."""

    subject: str
    sender: str
    company: Optional[str]
    job_links: List[str]
    received_at: str


def extract_recruiter_insights(messages: Iterable[GmailMessage]) -> List[RecruiterInsight]:
    """Build recruiter insights from Gmail messages."""

    insights: List[RecruiterInsight] = []
    for message in messages:
        company = _extract_company(message)
        job_links = JD_PATTERN.findall(message.body)
        insights.append(
            RecruiterInsight(
                subject=message.subject,
                sender=message.sender,
                company=company,
                job_links=job_links,
                received_at=message.received_at.isoformat(),
            )
        )
    return insights


def _extract_company(message: GmailMessage) -> Optional[str]:
    match = COMPANY_PATTERN.search(message.subject)
    if match:
        return match.group("company").strip()
    match = COMPANY_PATTERN.search(message.body)
    if match:
        return match.group("company").strip()
    return None

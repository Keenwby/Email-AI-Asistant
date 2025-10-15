"""Subscription usage analytics."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, List

from ..gmail_client import GmailMessage


@dataclass
class SubscriptionInsight:
    """Summary for a recurring newsletter or subscription."""

    sender: str
    subject_example: str
    message_count: int


def summarize_subscriptions(messages: Iterable[GmailMessage]) -> List[SubscriptionInsight]:
    """Aggregate messages by sender to determine high-volume subscriptions."""

    counter: Counter[str] = Counter()
    subject_examples: dict[str, str] = {}
    for message in messages:
        counter[message.sender] += 1
        subject_examples.setdefault(message.sender, message.subject)
    summaries: List[SubscriptionInsight] = []
    for sender, count in counter.most_common():
        summaries.append(
            SubscriptionInsight(
                sender=sender,
                subject_example=subject_examples[sender],
                message_count=count,
            )
        )
    return summaries

"""Email AI Assistant package exports."""

from .gmail_client import GmailClient
from .reporting import ReportBuilder

__all__ = ["GmailClient", "ReportBuilder"]

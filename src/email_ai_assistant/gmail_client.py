"""Utilities for interacting with the Gmail API."""

from __future__ import annotations

import base64
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import List, Optional

try:  # pragma: no cover - optional dependency for offline test environments
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ModuleNotFoundError:  # pragma: no cover - handled at runtime when client is used
    Request = None  # type: ignore
    Credentials = None  # type: ignore
    InstalledAppFlow = None  # type: ignore
    build = None  # type: ignore

    class HttpError(Exception):  # type: ignore
        """Fallback error type when Google client libraries are unavailable."""

        pass

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


@dataclass
class GmailMessage:
    """Simplified representation of a Gmail message."""

    id: str
    thread_id: str
    subject: str
    sender: str
    received_at: datetime
    snippet: str
    body: str


class GmailClient:
    """Thin wrapper around the Gmail API for read-only analytics use cases."""

    def __init__(self, credentials_path: str, token_path: Optional[str] = None) -> None:
        self.credentials_path = credentials_path
        self.token_path = token_path or "token.json"
        self._service = None

    def _build_service(self):
        if Credentials is None or InstalledAppFlow is None or Request is None or build is None:
            raise ImportError(
                "Google API client libraries are required to use GmailClient. "
                "Install the project with the 'dev' extras or run `pip install google-api-python-client google-auth-oauthlib`."
            )

        creds: Optional[Credentials] = None
        if Path(self.token_path).exists():
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            Path(self.token_path).write_text(creds.to_json())
        self._service = build("gmail", "v1", credentials=creds)

    @property
    def service(self):
        if self._service is None:
            self._build_service()
        return self._service

    def list_messages(self, query: str, max_results: int = 500) -> List[GmailMessage]:
        """Fetch messages using a Gmail search query."""

        try:
            response = (
                self.service.users()
                .messages()
                .list(userId="me", q=query, maxResults=max_results)
                .execute()
            )
        except HttpError as exc:
            logger.error("Failed to list Gmail messages: %s", exc)
            raise

        messages = response.get("messages", [])
        return [self.get_message(msg["id"]) for msg in messages]

    def get_message(self, message_id: str) -> GmailMessage:
        """Retrieve a full Gmail message."""

        response = (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )
        payload = response.get("payload", {})
        headers = {header["name"].lower(): header["value"] for header in payload.get("headers", [])}
        subject = headers.get("subject", "")
        sender = headers.get("from", "")
        received_at = self._parse_timestamp(response.get("internalDate"))
        snippet = response.get("snippet", "")
        body = self._extract_body(payload)
        return GmailMessage(
            id=response["id"],
            thread_id=response.get("threadId", ""),
            subject=subject,
            sender=sender,
            received_at=received_at,
            snippet=snippet,
            body=body,
        )

    def _parse_timestamp(self, value: Optional[str]) -> datetime:
        if not value:
            return datetime.now(tz=timezone.utc)
        try:
            return datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc)
        except (ValueError, TypeError):
            pass
        if isinstance(value, str):
            try:
                parsed = parsedate_to_datetime(value)
            except (TypeError, ValueError):
                return datetime.now(tz=timezone.utc)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed
        return datetime.now(tz=timezone.utc)

    def _extract_body(self, payload: dict) -> str:
        parts = payload.get("parts", [])
        if not parts:
            data = payload.get("body", {}).get("data")
            return self._decode_part(data)
        for part in parts:
            if part.get("mimeType") == "text/plain":
                return self._decode_part(part.get("body", {}).get("data"))
        return self._decode_part(parts[0].get("body", {}).get("data"))

    def _decode_part(self, data: Optional[str]) -> str:
        if not data:
            return ""
        return base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="ignore")

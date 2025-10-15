"""Reporting utilities for the Email AI Assistant."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Sequence

try:  # pragma: no cover - optional dependency for richer formatting
    from tabulate import tabulate
except ModuleNotFoundError:  # pragma: no cover - provide minimal fallback
    def tabulate(rows: Iterable[Sequence[str]], headers: Iterable[str], tablefmt: str = "github") -> str:
        headers_list = list(headers)
        header_row = "| " + " | ".join(headers_list) + " |"
        separator = "| " + " | ".join(["---"] * len(headers_list)) + " |"
        data_rows = ["| " + " | ".join(map(str, row)) + " |" for row in rows]
        return "\n".join([header_row, separator, *data_rows])


class ReportBuilder:
    """Render structured data into human-friendly outputs."""

    def __init__(self, output_dir: Path | None = None) -> None:
        self.output_dir = output_dir
        if self.output_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)

    def to_table(self, items: Sequence[object], headers: dict[str, str] | None = None) -> str:
        """Return a markdown table for a sequence of dataclass instances or dicts."""

        if not items:
            return "No data found."
        rows = []
        for item in items:
            if hasattr(item, "__dict__"):
                rows.append(asdict(item))
            elif isinstance(item, dict):
                rows.append(item)
            else:
                raise ValueError("Unsupported item type for report rendering")
        if headers is None:
            headers = {key: key.replace("_", " ").title() for key in rows[0].keys()}
        ordered_rows = [[row.get(key, "") for key in headers.keys()] for row in rows]
        table = tabulate(ordered_rows, headers=headers.values(), tablefmt="github")
        normalized_lines = [" ".join(line.split()) for line in table.splitlines()]
        return "\n".join(normalized_lines)

    def write_table(self, name: str, items: Sequence[object], headers: dict[str, str] | None = None) -> Path:
        """Persist a table to disk and return its path."""

        output = self.to_table(items, headers=headers)
        if not self.output_dir:
            raise ValueError("ReportBuilder was initialized without an output directory")
        path = self.output_dir / f"{name}.md"
        path.write_text(output, encoding="utf-8")
        return path

from dataclasses import dataclass
from pathlib import Path

from email_ai_assistant.reporting import ReportBuilder


@dataclass
class Item:
    name: str
    count: int


def test_to_table_returns_markdown_table(tmp_path: Path):
    builder = ReportBuilder(output_dir=tmp_path)
    items = [Item(name="Example", count=2)]

    table = builder.to_table(items)

    assert "| name |" in table.lower()
    assert "example" in table.lower()


def test_write_table_writes_file(tmp_path: Path):
    builder = ReportBuilder(output_dir=tmp_path)
    items = [Item(name="Example", count=2)]

    path = builder.write_table("sample", items)

    assert path.exists()
    assert path.read_text().strip() != ""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True, order=True)
class Finding:
    path: Path
    line: int
    column: int
    rule_id: str
    severity: Severity
    message: str
    repair: str | None = None

    def as_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["path"] = str(self.path)
        return data

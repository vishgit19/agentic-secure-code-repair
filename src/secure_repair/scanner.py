from __future__ import annotations

import ast
import difflib
from collections.abc import Iterable
from pathlib import Path

from .models import Finding
from .rules import inspect_tree

_IGNORED_PARTS = {".git", ".mypy_cache", ".pytest_cache", ".tox", ".venv", "venv", "node_modules"}


def scan_source(source: str, path: str | Path = "<memory>") -> list[Finding]:
    source_path = Path(path)
    try:
        tree = ast.parse(source, filename=str(source_path))
    except SyntaxError as exc:
        return [
            Finding(
                path=source_path,
                line=exc.lineno or 1,
                column=exc.offset or 1,
                rule_id="SR000",
                severity="low",
                message=f"File could not be parsed: {exc.msg}",
            )
        ]
    return sorted(inspect_tree(tree, source_path))


def _python_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        if path.suffix == ".py":
            yield path
        return
    for candidate in sorted(path.rglob("*.py")):
        if not any(part in _IGNORED_PARTS for part in candidate.parts):
            yield candidate


def scan_path(path: str | Path) -> list[Finding]:
    root = Path(path)
    findings: list[Finding] = []
    for candidate in _python_files(root):
        try:
            source = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            findings.append(Finding(candidate, 1, 1, "SR000", "low", f"File could not be read: {exc}"))
            continue
        findings.extend(scan_source(source, candidate))
    return sorted(findings)


def build_patch(findings: Iterable[Finding]) -> str:
    by_path: dict[Path, list[Finding]] = {}
    for finding in findings:
        if finding.repair:
            by_path.setdefault(finding.path, []).append(finding)

    chunks: list[str] = []
    for path, repairable in sorted(by_path.items(), key=lambda item: str(item[0])):
        try:
            original = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        updated_lines = original.splitlines(keepends=True)
        for finding in sorted(repairable, key=lambda item: item.line, reverse=True):
            index = finding.line - 1
            if not 0 <= index < len(updated_lines):
                continue
            line = updated_lines[index]
            if finding.rule_id == "SR003":
                updated_lines[index] = line.replace("verify=False", "verify=True", 1)
            elif finding.rule_id == "SR004":
                updated_lines[index] = line.replace("debug=True", "debug=False", 1)

        updated = "".join(updated_lines)
        if updated == original:
            continue
        chunks.extend(
            difflib.unified_diff(
                original.splitlines(keepends=True),
                updated.splitlines(keepends=True),
                fromfile=f"a/{path.as_posix()}",
                tofile=f"b/{path.as_posix()}",
            )
        )
    return "".join(chunks)

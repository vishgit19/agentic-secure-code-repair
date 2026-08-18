from __future__ import annotations

import ast
import re
from collections.abc import Iterable
from pathlib import Path

from .models import Finding

_SECRET_NAME = re.compile(r"(?:api[_-]?key|secret|token|password|passwd)", re.IGNORECASE)
_PLACEHOLDERS = {"", "changeme", "example", "password", "secret", "token", "your-token-here"}


def _call_name(node: ast.Call) -> str:
    parts: list[str] = []
    value: ast.AST = node.func
    while isinstance(value, ast.Attribute):
        parts.append(value.attr)
        value = value.value
    if isinstance(value, ast.Name):
        parts.append(value.id)
    return ".".join(reversed(parts))


def _keyword_bool(node: ast.Call, name: str, value: bool) -> bool:
    return any(
        keyword.arg == name
        and isinstance(keyword.value, ast.Constant)
        and keyword.value.value is value
        for keyword in node.keywords
    )


class SecurityVisitor(ast.NodeVisitor):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.findings: list[Finding] = []

    def add(
        self,
        node: ast.AST,
        rule_id: str,
        severity: str,
        message: str,
        repair: str | None = None,
    ) -> None:
        self.findings.append(
            Finding(
                path=self.path,
                line=getattr(node, "lineno", 1),
                column=getattr(node, "col_offset", 0) + 1,
                rule_id=rule_id,
                severity=severity,  # type: ignore[arg-type]
                message=message,
                repair=repair,
            )
        )

    def visit_Call(self, node: ast.Call) -> None:
        name = _call_name(node)
        if name in {"eval", "exec"}:
            self.add(node, "SR001", "high", f"Dynamic code execution through {name}()")
        if name in {"subprocess.call", "subprocess.run", "subprocess.Popen"} and _keyword_bool(
            node, "shell", True
        ):
            self.add(node, "SR002", "high", "Subprocess command uses shell=True")
        if _keyword_bool(node, "verify", False):
            self.add(
                node,
                "SR003",
                "high",
                "TLS certificate verification is disabled",
                "replace `verify=False` with `verify=True`",
            )
        if _keyword_bool(node, "debug", True):
            self.add(
                node,
                "SR004",
                "medium",
                "Debug mode is enabled",
                "replace `debug=True` with `debug=False`",
            )
        if name.endswith("yaml.load") or name == "yaml.load":
            has_loader = any(keyword.arg == "Loader" for keyword in node.keywords)
            if not has_loader:
                self.add(node, "SR005", "medium", "yaml.load() is used without an explicit safe loader")
        if name in {"hashlib.md5", "hashlib.sha1"}:
            self.add(node, "SR006", "medium", f"Weak cryptographic hash used through {name}()")
        if name in {"pickle.load", "pickle.loads"}:
            self.add(node, "SR008", "high", f"Untrusted data may execute code through {name}()")
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            value = node.value.value.strip()
            for target in node.targets:
                if isinstance(target, ast.Name) and _SECRET_NAME.search(target.id):
                    if len(value) >= 12 and value.lower() not in _PLACEHOLDERS:
                        self.add(node, "SR007", "high", f"Likely hard-coded secret assigned to {target.id}")
                        break
        self.generic_visit(node)


def inspect_tree(tree: ast.AST, path: Path) -> Iterable[Finding]:
    visitor = SecurityVisitor(path)
    visitor.visit(tree)
    return visitor.findings

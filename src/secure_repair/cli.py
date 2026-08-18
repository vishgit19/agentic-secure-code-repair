from __future__ import annotations

import argparse
import json
from pathlib import Path

from .scanner import build_patch, scan_path

_SEVERITY = {"low": 1, "medium": 2, "high": 3}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="secure-repair")
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan = subparsers.add_parser("scan", help="scan a Python file or directory")
    scan.add_argument("path", nargs="?", default=".")
    scan.add_argument("--format", choices=("text", "json"), default="text")
    scan.add_argument("--patch", type=Path, help="write supported repairs as a unified diff")
    scan.add_argument("--fail-on", choices=("low", "medium", "high"), default="high")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    findings = scan_path(args.path)
    if args.format == "json":
        print(json.dumps([finding.as_dict() for finding in findings], indent=2))
    else:
        for finding in findings:
            print(
                f"{finding.path}:{finding.line}:{finding.column} "
                f"{finding.rule_id} {finding.severity} {finding.message}"
            )
            if finding.repair:
                print(f"  repair: {finding.repair}")
        print(f"\n{len(findings)} finding(s)")
    if args.patch:
        args.patch.write_text(build_patch(findings), encoding="utf-8")
    threshold = _SEVERITY[args.fail_on]
    return int(any(_SEVERITY[finding.severity] >= threshold for finding in findings))


if __name__ == "__main__":
    raise SystemExit(main())

import argparse
import json
import sys
from pathlib import Path

from .pipeline import run


def main(argv=None):
    parser = argparse.ArgumentParser(description="GACL public-disclosure batch pipeline")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project directory with config/")
    parser.add_argument("--source", help="Reload only the specified source_id")
    parser.add_argument("--offline", action="store_true", help="Use checksum-verified cached PDFs only")
    parser.add_argument("--refresh", action="store_true", help="Re-download and verify against pinned checksums")
    args = parser.parse_args(argv)
    try:
        summary = run(args.root, args.source, args.offline, args.refresh)
    except Exception as exc:
        print(f"Pipeline failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2))
    return 0


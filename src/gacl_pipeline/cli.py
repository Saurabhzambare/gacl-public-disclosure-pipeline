import argparse
import json
import sys
from pathlib import Path

from .pipeline import run


def main(argv=None):
    parser = argparse.ArgumentParser(description="GACL public-disclosure batch pipeline")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project directory with config/")
    parser.add_argument("--source", help="Reload only the specified source_id")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--offline", action="store_true", help="Use checksum-verified cached PDFs only")
    mode.add_argument("--refresh", action="store_true", help="Re-download and verify against pinned checksums")
    mode.add_argument("--from-examples", action="store_true",
                      help="Use reviewed CSV extracts from the repository; no PDF download or verification")
    args = parser.parse_args(argv)
    try:
        summary = run(args.root, args.source, args.offline, args.refresh, args.from_examples)
    except Exception as exc:
        print(f"Pipeline failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2))
    return 0


"""Transactional local warehouse with version-preserving, duplicate-safe loads."""
import json
import sqlite3
from pathlib import Path

COLUMNS = ("observation_id", "source_id", "document_sha256", "source_url", "pdf_page",
           "printed_page", "reporting_scope", "metric_id", "period_start", "period_end",
           "frequency", "statistic_type", "unit", "raw_value", "value",
           "extraction_method", "parser_version")


def connect(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS observations (
        observation_id TEXT NOT NULL, source_id TEXT NOT NULL,
        document_sha256 TEXT NOT NULL, source_url TEXT NOT NULL,
        pdf_page INTEGER NOT NULL, printed_page INTEGER NOT NULL,
        reporting_scope TEXT NOT NULL, metric_id TEXT NOT NULL,
        period_start TEXT NOT NULL, period_end TEXT NOT NULL,
        frequency TEXT NOT NULL, statistic_type TEXT NOT NULL, unit TEXT NOT NULL,
        raw_value TEXT NOT NULL, value TEXT NOT NULL,
        extraction_method TEXT NOT NULL, parser_version TEXT NOT NULL,
        PRIMARY KEY (observation_id, source_id, document_sha256)
    )""")
    db.execute("""CREATE TABLE IF NOT EXISTS pipeline_runs (
        run_id TEXT PRIMARY KEY, started_at TEXT, ended_at TEXT,
        status TEXT, selected_sources TEXT, row_count INTEGER, error TEXT
    )""")
    db.commit()
    return db


def load(db, rows):
    with db:
        db.executemany(
            f"INSERT INTO observations ({','.join(COLUMNS)}) VALUES ({','.join('?' for _ in COLUMNS)}) "
            f"ON CONFLICT(observation_id,source_id,document_sha256) DO UPDATE SET "
            + ",".join(f"{k}=excluded.{k}" for k in COLUMNS if k not in ("observation_id", "source_id", "document_sha256")),
            [tuple(row[k] for k in COLUMNS) for row in rows])


def start_run(db, run_id, started, ids):
    with db:
        db.execute("INSERT INTO pipeline_runs VALUES (?,?,NULL,'running',?,0,NULL)",
                   (run_id, started, json.dumps(ids)))


def finish_run(db, run_id, ended, status, count, error=None):
    with db:
        db.execute("UPDATE pipeline_runs SET ended_at=?,status=?,row_count=?,error=? WHERE run_id=?",
                   (ended, status, count, error, run_id))


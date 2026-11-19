"""Data contract checks; these are data quality checks, not compliance rulings."""
from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
from .extract import parse_number


def validate_rows(rows, metrics, sources):
    definitions = {m["metric_id"]: m for m in metrics}
    source_map = {s["source_id"]: s for s in sources}
    valid, rejected, seen = [], [], set()
    required = ("observation_id", "source_id", "source_url", "document_sha256",
                "pdf_page", "printed_page", "reporting_scope", "metric_id",
                "period_start", "period_end", "frequency", "statistic_type",
                "unit", "raw_value", "value", "extraction_method", "parser_version")
    for row in rows:
        reasons = []
        if any(row.get(k) is None or row.get(k) == "" for k in required):
            reasons.append("missing_required_field")
        definition = definitions.get(row.get("metric_id"))
        if not definition:
            reasons.append("unknown_metric")
        else:
            for field in ("unit", "statistic_type", "frequency", "reporting_scope"):
                if row.get(field) != definition[field]:
                    reasons.append(f"invalid_{field}")
        source = source_map.get(row.get("source_id"))
        if not source or any(row.get(k) != source.get(k) for k in ("reporting_scope",)):
            reasons.append("invalid_source_scope")
        if source and (row.get("document_sha256") != source["sha256"] or row.get("source_url") != source["url"]):
            reasons.append("invalid_provenance")
        if source and not any(row.get("pdf_page") == p["pdf_page"] and row.get("printed_page") == p["printed_page"] for p in source["pages"]):
            reasons.append("invalid_source_page")
        try:
            start, end = date.fromisoformat(row["period_start"]), date.fromisoformat(row["period_end"])
            if start > end:
                reasons.append("invalid_period_order")
            if row.get("frequency") == "annual" and (start.month, start.day, end.month, end.day, end.year-start.year) != (4, 1, 3, 31, 1):
                reasons.append("invalid_financial_year")
            if row.get("frequency") == "monthly":
                import calendar
                if start.day != 1 or start.year != end.year or start.month != end.month or end.day != calendar.monthrange(start.year, start.month)[1]:
                    reasons.append("invalid_month_period")
        except (KeyError, TypeError, ValueError):
            reasons.append("invalid_period")
        try:
            value = Decimal(str(row["value"]))
            if not value.is_finite() or value < 0:
                reasons.append("invalid_numeric_value")
            if parse_number(row.get("raw_value", "")) != value:
                reasons.append("raw_value_mismatch")
        except (InvalidOperation, KeyError, TypeError, ValueError):
            reasons.append("invalid_numeric_value")
        identity = "|".join(str(row.get(k, "")) for k in
                            ("reporting_scope", "metric_id", "period_start", "period_end", "unit", "statistic_type"))
        if row.get("observation_id") != hashlib.sha256(identity.encode()).hexdigest():
            reasons.append("invalid_observation_identity")
        key = row.get("observation_id")
        if key in seen:
            reasons.append("duplicate_observation")
        seen.add(key)
        if reasons:
            rejected.append({"row": row, "reasons": reasons})
        else:
            valid.append(row)
    return valid, rejected


def reconcile(rows, selected_source_ids):
    checks = []
    if "gacl_dahej_plot3_ec_2025_h1" in selected_source_ids:
        monthly = [r for r in rows if r["source_id"] == "gacl_dahej_plot3_ec_2025_h1"]
        expected = {f"2025-{m:02d}-01" for m in range(4, 10)}
        checks.append({"check_id": "monthly_coverage", "passed": len(monthly) == 6 and {r["period_start"] for r in monthly} == expected,
                       "details": "Six unique months: April–September 2025"})
    if "gacl_brsr_2025_26" in selected_source_ids:
        annual = [r for r in rows if r["source_id"] == "gacl_brsr_2025_26"]
        checks.append({"check_id": "annual_coverage", "passed": len(annual) == 12,
                       "details": "Six annual totals for each of two financial years"})
        for start in ("2024-04-01", "2025-04-01"):
            values = {r["metric_id"]: Decimal(r["value"]) for r in annual if r["period_start"] == start}
            keys = {"energy_total", "energy_renewable_total", "energy_nonrenewable_total"}
            delta = abs(values["energy_total"] - values["energy_renewable_total"] - values["energy_nonrenewable_total"]) if keys <= values.keys() else None
            checks.append({"check_id": f"energy_reconciliation_{start}", "passed": delta is not None and delta <= Decimal("0.01"),
                           "details": f"Absolute difference {delta} GJ; tolerance 0.01 GJ"})
    return checks


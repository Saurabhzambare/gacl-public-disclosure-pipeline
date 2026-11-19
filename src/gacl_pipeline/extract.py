"""Layout-specific parsers for two checksum-pinned public reports."""
import calendar
import hashlib
import re
from datetime import date
from decimal import Decimal, InvalidOperation

NUMBER = r"\d[\d,]*(?:\.\d+)?"
MISSING = {"", "-", "—", "NA", "N/A", "NOT AVAILABLE"}


def parse_number(raw):
    """Preserve missingness; refuse malformed western or Indian grouping."""
    text = str(raw).strip()
    if text.upper() in MISSING:
        return None
    if not re.fullmatch(r"[+-]?(?:\d+|\d{1,3}(?:,\d{3})+|\d{1,2}(?:,\d{2})*,\d{3})(?:\.\d+)?", text):
        raise ValueError(f"Invalid numeric value: {text!r}")
    try:
        value = Decimal(text.replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError("Invalid numeric value") from exc
    if not value.is_finite():
        raise ValueError("Non-finite numeric value")
    return value


def observation(source, metric, start, end, frequency, statistic, unit, raw, page, printed):
    key = "|".join([source["reporting_scope"], metric, start, end, unit, statistic])
    value = parse_number(raw)
    return {
        "observation_id": hashlib.sha256(key.encode()).hexdigest(),
        "source_id": source["source_id"], "document_sha256": source["sha256"],
        "source_url": source["url"], "pdf_page": page, "printed_page": printed,
        "reporting_scope": source["reporting_scope"], "metric_id": metric,
        "period_start": start, "period_end": end, "frequency": frequency,
        "statistic_type": statistic, "unit": unit, "raw_value": raw,
        "value": None if value is None else str(value),
        "extraction_method": "pdf_text_regex", "parser_version": source["parser"],
    }


def extract_monthly(doc, source):
    text = doc[4].get_text(sort=True)
    if "Fresh water" not in text or "KL/day" not in text:
        raise ValueError("Monthly table context not found; review PDF layout")
    months = {"April": 4, "May": 5, "June": 6, "July": 7, "Aug": 8, "Sept": 9}
    pattern = rf"\b(April|May|June|July|Aug|Sept)-2025[ \t]+({NUMBER})"
    matches = re.findall(pattern, text)
    if len(matches) != 6 or len({m for m, _ in matches}) != 6:
        raise ValueError(f"Expected six unique monthly rows; got {len(matches)}")
    rows = []
    for name, raw in matches:
        month = months[name]
        rows.append(observation(
            source, "freshwater_average_daily", date(2025, month, 1).isoformat(),
            date(2025, month, calendar.monthrange(2025, month)[1]).isoformat(),
            "monthly", "monthly_average_daily_rate", "KL/day", raw, 5, 4))
    return rows


def extract_annual(doc, source):
    specs = [
        (36, 78, "energy_renewable_total", "GJ", r"Total energy consumed from renewable sources \(A\+B\+C\)"),
        (36, 78, "energy_nonrenewable_total", "GJ", r"Total energy consumed from non-renewable sources"),
        (36, 78, "energy_total", "GJ", r"Total energy consumed \(A\+B\+C\+D\+E\+F\)"),
        (37, 79, "water_withdrawal_total", "KL", r"Total volume of water withdrawal"),
        (37, 79, "water_consumption_total", "KL", r"Total volume of water consumption \(in kilolitres\)\*?"),
        (38, 80, "water_discharge_total", "KL", r"Total water discharged \(in kilolitres\)"),
    ]
    rows = []
    for page, printed, metric, unit, label in specs:
        text = doc[page - 1].get_text(sort=True)
        if not re.search(r"FY\s+2025-26\s+FY\s+2024-25", text):
            raise ValueError(f"Year-column order missing on PDF page {page}")
        matches = re.findall(label + rf"[ \t]+({NUMBER})[ \t]+({NUMBER})", text)
        if len(matches) != 1:
            raise ValueError(f"Expected one {metric} row on page {page}; found {len(matches)}")
        for start_year, raw in zip([2025, 2024], matches[0]):
            rows.append(observation(
                source, metric, f"{start_year}-04-01", f"{start_year + 1}-03-31",
                "annual", "annual_total", unit, raw, page, printed))
    return rows


def extract_pdf(path, source):
    import pymupdf
    with pymupdf.open(path) as doc:
        if source["parser"] == "monthly_water_v1":
            return extract_monthly(doc, source)
        if source["parser"] == "annual_totals_v1":
            return extract_annual(doc, source)
        raise ValueError(f"Unsupported parser: {source['parser']}")


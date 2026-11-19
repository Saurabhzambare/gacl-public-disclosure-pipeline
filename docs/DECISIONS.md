# Design decisions

1. **Public disclosures only.** No authorization or access to internal GACL systems is assumed.
2. **Core first.** Two reports and 18 observations keep the 22 November target realistic.
3. **Separate grains.** Monthly site KL/day rates and annual standalone company GJ/KL totals never share an aggregation.
4. **Exact values.** Decimal strings preserve disclosed precision; presentation rounding is separate.
5. **Pinned documents.** SHA-256 verification makes layout-specific extraction reproducible and flags revisions.
6. **Local first.** SQLite and CSV give a working demonstration before cloud authentication is configured.
7. **Targeted extraction.** Explicit labels, page references, expected row counts and year-column checks are easier to review than a general PDF parser.
8. **No invented scale.** Small data demonstrates correctness; there is no throughput, cost-saving or operational impact claim.
9. **No premature forecasting.** Six monthly averages are insufficient evidence for predictive maintenance.
10. **Public portfolio.** The user made the repository public after initial setup. Source attribution and current feature status remain explicit.
11. **Source licensing stays separate.** MIT applies only to original project code.


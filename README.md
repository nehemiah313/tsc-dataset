# SOC 2 Trust Services Criteria Dataset

Machine-readable dataset of the AICPA Trust Services Criteria: **61 criteria**
across the five Trust Services Categories.

| Category | Code | Criteria | In scope |
|---|---|---|---|
| Security (Common Criteria) | CC1-CC9 | 33 | Always required |
| Availability | A1 | 3 | Optional |
| Processing Integrity | PI1 | 5 | Optional |
| Confidentiality | C1 | 2 | Optional |
| Privacy | P1-P8 | 18 | Optional |

## Files

- `data/tsc.json` - full dataset: framework metadata, category definitions, series names, and all 61 criteria with plain-English summaries, typical evidence examples, and priority tiers
- `data/tsc.csv` - flat version of the same data for spreadsheets
- `build_tsc.py` - the script that generates both files from a single source of truth

## Fields

Each criterion has: `id`, `category`, `series`, `series_name`, `title`,
`summary` (original plain-English), `typical_evidence`, and `priority`
(`critical` for the access-control and operations criteria where audits most
often fail, `high` for everything else).

## Source and license note

Criterion structure verified against the AICPA 2017 Trust Services Criteria
(TSP Section 100), with 2022 revised points of focus. Summaries and evidence
suggestions are original plain-English guidance written for this dataset, not
AICPA text. This is a readiness aid, not an audit opinion, attestation, or
legal advice. SOC 2 examinations are performed by licensed CPA firms.

## Use

This dataset powers the AI Tech Pros SOC 2 readiness tool suite:
readiness calculator, remediation planner, system description generator,
evidence checklist, criteria decoder, incident checklist, vendor tracker,
and breach-cost tracker.

MIT License. Copyright (c) 2026 AI Tech Pros, Inc.

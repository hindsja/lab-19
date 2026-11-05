# Live validation

Executed by AI using downloaded SEC facts. The reference is from the supplied Lab 18 assignment.

| Fiscal year end | Metric | Instructor reference | SEC result | Match |
|---|---|---:|---:|---|
| 2022-08-28 | Revenue | 226,954 | 226,954 | yes |
| 2022-08-28 | Net income | 5,844 | 5,844 | yes |
| 2022-08-28 | Operating cash flow | 7,392 | 7,392 | yes |
| 2022-08-28 | Capital spending | 3,891 | 3,891 | yes |
| 2022-08-28 | Equity | 20,642 | 20,642 | yes |
| 2022-08-28 | ROE | 28.3% | 28.3% | yes |
| 2022-08-28 | Owner earnings | 3,501 | 3,501 | yes |
| 2023-09-03 | Revenue | 242,290 | 242,290 | yes |
| 2023-09-03 | Net income | 6,292 | 6,292 | yes |
| 2023-09-03 | Operating cash flow | 11,068 | 11,068 | yes |
| 2023-09-03 | Capital spending | 4,323 | 4,323 | yes |
| 2023-09-03 | Equity | 25,058 | 25,058 | yes |
| 2023-09-03 | ROE | 25.1% | 25.1% | yes |
| 2023-09-03 | Owner earnings | 6,745 | 6,745 | yes |
| 2024-09-01 | Revenue | 254,453 | 254,453 | yes |
| 2024-09-01 | Net income | 7,367 | 7,367 | yes |
| 2024-09-01 | Operating cash flow | 11,339 | 11,339 | yes |
| 2024-09-01 | Capital spending | 4,710 | 4,710 | yes |
| 2024-09-01 | Equity | 23,622 | 23,622 | yes |
| 2024-09-01 | ROE | 31.2% | 31.2% | yes |
| 2024-09-01 | Owner earnings | 6,629 | 6,629 | yes |
| 2025-08-31 | Revenue | 275,235 | 275,235 | yes |
| 2025-08-31 | Net income | 8,099 | 8,099 | yes |
| 2025-08-31 | Operating cash flow | 13,335 | 13,335 | yes |
| 2025-08-31 | Capital spending | 5,498 | 5,498 | yes |
| 2025-08-31 | Equity | 29,164 | 29,164 | yes |
| 2025-08-31 | ROE | 27.8% | 27.8% | yes |
| 2025-08-31 | Owner earnings | 7,837 | 7,837 | yes |
| 2026-08-30 | Revenue | 303,154 | 303,154 | yes |
| 2026-08-30 | Net income | 9,226 | 9,226 | yes |
| 2026-08-30 | Operating cash flow | 15,817 | 15,817 | yes |
| 2026-08-30 | Capital spending | 6,435 | 6,435 | yes |
| 2026-08-30 | Equity | 35,803 | 35,803 | yes |
| 2026-08-30 | ROE | 25.8% | 25.8% | yes |
| 2026-08-30 | Owner earnings | 9,382 | 9,382 | yes |

Reference discrepancies: 0. Actual SEC periods: 2022-08-28, 2023-09-03, 2024-09-01, 2025-08-31, 2026-08-30.

## COST checks

{
  "ROE of 15% or more every year": "pass",
  "Owner earnings positive every year": "pass",
  "Owner earnings grew, first year to last": "pass"
}

## JPM missing-data probe

Expected missing-data behavior: PASS.

{
  "ROE of 15% or more every year": "fail",
  "Owner earnings positive every year": "not known",
  "Owner earnings grew, first year to last": "not known"
}

COST memo unsupported numbers: []

JPM memo unsupported numbers: []

Injected ROE probe: [{"number": "40.0%", "position": 7}]

Matching tokens do not verify correct attribution or interpretation. A reference discrepancy is disclosed, not overwritten.

## Reproducibility and app verification

Rechecked November 3, 2026 by Codex. Both saved raw SEC snapshots match their recorded SHA-256 hashes and regenerate their saved reports exactly. All eleven unit/integration tests pass, including the Streamlit COST/JPM switch and injected-number warning. The COST trust decision is AI-assisted and included in the memo.

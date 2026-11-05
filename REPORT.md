# Lab 19 — Legend Panel

**Question:** When three investors' skills read the same annual filing facts, where do they agree, where do they split — and would the panel be trusted?

**Decision — AI-assisted proposal:** Use the panel only for preliminary research triage, conditional on verifying source periods and unknowns, investigating cash-backing and leverage failures, and separately assessing valuation and fund-level diversification before any Project 2 allocation decision.

## Company selection and scope

FNDX is the Schwab Fundamental U.S. Large Company ETF. Its largest holding by portfolio weight is Apple (AAPL), at 4.85% as of November 4, 2026, according to [Schwab's holdings page](https://www.schwabassetmanagement.com/allholdings/FNDX?page=0), accessed November 5, 2026. Apple files annual reports on EDGAR, so no next-largest-company substitution was required. This interprets "largest company inside the fund" as the largest fund holding, rather than the largest issuer by market capitalization.

The analysis uses the latest five eligible annual periods in downloaded SEC facts. COST reuses the preserved November 3 Lab 18 source; Apple was retrieved November 5. Exact retrieval timestamps, original-source hashes, filing accessions, tags and the source observations needed for offline reconstruction are retained in `results.json`. These are latest-filed histories, not historical investment backtests. Investor memos below are separate model judgments produced by OpenAI Codex under each skill, not statements by the real investors or independent model votes.

## Calculations and honest gaps

The existing Lab 18 reader is reused unchanged: USD facts in 10-Ks only; annual flows cover 350–380 days; latest filing wins within each tag and period; the prescribed tag priority applies per period. All flows share a row's start/end dates and balance-sheet values use its fiscal end. Revenue growth = (last revenue / first revenue)^(1/4) − 1; it requires five annual observations and a positive starting revenue. R&D uses `ResearchAndDevelopmentExpense`, then the handout's fallback `ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost`. Liabilities use `Liabilities` and are not substituted with debt.

ROE = net income / year-end equity; owner earnings = operating cash flow − total capital spending; R&D intensity = R&D / revenue; leverage = liabilities / year-end equity. Missing source amounts remain **not found**; ratios/checks with missing inputs remain **not known**. Nonpositive equity makes ROE and leverage unknown. COST's R&D ratio is shown as not known because its reported R&D is not found; this preserves the same gap shown as "not found" in the instructor's reference. No unknown is counted as a fail or a pass. All checks use unrounded values.

## Executed panels and model memos


## COST — COSTCO WHOLESALE CORP /NEW

Amounts in USD millions; ratios are dimensionless. Missing R&D is not found; its ratio and check are not known.

| FY end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE | Owner earnings | Liabilities | R&D | R&D / revenue | Liabilities / equity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022-08-28 | 226,954 | 5,844 | 7,392 | 3,891 | 20,642 | 28.3% | 3,501 | 43,519 | not found | not known | 2.11 |
| 2023-09-03 | 242,290 | 6,292 | 11,068 | 4,323 | 25,058 | 25.1% | 6,745 | 43,936 | not found | not known | 1.75 |
| 2024-09-01 | 254,453 | 7,367 | 11,339 | 4,710 | 23,622 | 31.2% | 6,629 | 46,209 | not found | not known | 1.96 |
| 2025-08-31 | 275,235 | 8,099 | 13,335 | 5,498 | 29,164 | 27.8% | 7,837 | 47,935 | not found | not known | 1.64 |
| 2026-08-30 | 303,154 | 9,226 | 15,817 | 6,435 | 35,803 | 25.8% | 9,382 | 53,242 | not found | not known | 1.49 |

Revenue growth a year: **7.51%**.
Thresholds: growth 15%; R&D 5%; ROE 15%; liabilities / equity 2.

| Investor | Check | Result |
|---|---|---|
| Buffett | ROE of 15% or more every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew, first year to last | pass |
| Cathie Wood | Revenue grew 15% or more a year, first year to last | fail |
| Cathie Wood | R&D 5% or more of revenue, latest year | not known |
| Burry | Operating cash flow at least net income every year | pass |
| Burry | Liabilities no more than twice equity, latest year | pass |
Buffett: 3 of 3 checks pass.
Cathie Wood: 0 of 2 checks pass.
Burry: 2 of 2 checks pass.

SEC source: https://data.sec.gov/api/xbrl/companyfacts/CIK0000909832.json
Retrieved UTC: 20261103T201714Z
SHA-256: b675ced201b27ede2b0d26ca6fd873befe96a1afa9679339a2d0b964187dcdff

### COST: Buffett

**Verdict: watch it.** AI-generated Buffett-style simulation; amounts are USD millions.

COST passes all the prescribed business-quality checks. ROE remains above 15%, owner earnings remain positive, and owner earnings increase from 3,501 to 9,382. This supports sustained earning power and cash generation after total capital spending.

The path is uneven: owner earnings fall from 6,745 to 6,629 before recovering. Latest ROE of 25.8% is attractive, but year-end equity is a sensitive denominator and the numbers alone do not establish a durable moat or good capital allocation. I would watch the business pending evidence of durable competitive advantage and prudent reinvestment; weakening cash generation would reduce confidence. No purchase price is assessed.

### COST: Cathie Wood

**Verdict: pass for this growth screen.** AI-generated Cathie Wood-style simulation.

Revenue grows 7.51% a year, below the retained 15% threshold. R&D is not found, so research intensity is not known; missing disclosure is not evidence of zero innovation. The printed facts do not establish the rapid expansion and research commitment this screen seeks.

This verdict does not reject the business's cash-generating quality. Historical growth is only a proxy for future innovation, and a retailer need not report research like a technology company. I would reconsider if faster sustained growth and reported research evidence supported the innovation thesis; no forecast or valuation is inferred.

Threshold retained: 15%, to preserve a demanding growth screen rather than tune it to make COST pass.

### COST: Burry

**Verdict: watch it.** AI-generated Burry-style simulation; amounts are USD millions.

Operating cash flow meets or exceeds net income in every observed year, and latest liabilities/equity of 1.49 passes the ceiling of 2. Latest operating cash flow of 15,817 exceeds net income of 9,226, providing reassuring cash backing for reported earnings.

Earlier liabilities/equity of 2.11 exceeds the latest-year ceiling, although that earlier observation does not fail a rule explicitly applied only to the latest year. Total liabilities are not the same as interest-bearing debt, and aggregate operating cash flow cannot resolve footnote risks or working-capital timing. I would watch pending a closer review of obligations and cash-flow composition; persistent cash shortfalls or worsening leverage would weaken the case. These checks establish neither undervaluation nor an absence of accounting risk.

## AAPL — Apple Inc.

Amounts in USD millions; ratios are dimensionless. Missing R&D is not found; its ratio and check are not known.

| FY end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE | Owner earnings | Liabilities | R&D | R&D / revenue | Liabilities / equity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022-09-24 | 394,328 | 99,803 | 122,151 | 10,708 | 50,672 | 197.0% | 111,443 | 302,083 | 26,251 | 6.66% | 5.96 |
| 2023-09-30 | 383,285 | 96,995 | 110,543 | 10,959 | 62,146 | 156.1% | 99,584 | 290,437 | 29,915 | 7.80% | 4.67 |
| 2024-09-28 | 391,035 | 93,736 | 118,254 | 9,447 | 56,950 | 164.6% | 108,807 | 308,030 | 31,370 | 8.02% | 5.41 |
| 2025-09-27 | 416,161 | 112,010 | 111,482 | 12,715 | 73,733 | 151.9% | 98,767 | 285,508 | 34,550 | 8.30% | 3.87 |
| 2026-09-26 | 478,834 | 132,175 | 145,097 | 9,041 | 112,093 | 117.9% | 136,056 | 292,455 | 45,765 | 9.56% | 2.61 |

Revenue growth a year: **4.97%**.
Thresholds: growth 15%; R&D 5%; ROE 15%; liabilities / equity 2.

| Investor | Check | Result |
|---|---|---|
| Buffett | ROE of 15% or more every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew, first year to last | pass |
| Cathie Wood | Revenue grew 15% or more a year, first year to last | fail |
| Cathie Wood | R&D 5% or more of revenue, latest year | pass |
| Burry | Operating cash flow at least net income every year | fail |
| Burry | Liabilities no more than twice equity, latest year | fail |
Buffett: 3 of 3 checks pass.
Cathie Wood: 1 of 2 checks pass.
Burry: 0 of 2 checks pass.

SEC source: https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json
Retrieved UTC: 2026-11-05T21:59:27.431153+00:00
SHA-256: 75a78f918313f3336823517d6c34908d23dd07f07e90e625c61e705e3bb6d27b

### AAPL: Buffett

**Verdict: watch it.** AI-generated Buffett-style simulation; amounts are USD millions.

Apple passes all the Buffett checks: ROE exceeds 15% throughout, owner earnings stay positive, and owner earnings rise from 111,443 to 136,056. This provides evidence of cash-generating capacity after total capital spending, although the path includes a decline to 98,767 before the final recovery.

Latest ROE of 117.9% must be read beside the equity denominator and liabilities/equity of 2.61. High ROE alone is not proof of a durable competitive advantage, and the printed facts do not establish why equity is relatively small. I would watch pending evidence on competitive durability, capital allocation and balance-sheet resilience; persistent deterioration in cash after investment would change the judgment. This is a business assessment without a valuation.

### AAPL: Cathie Wood

**Verdict: pass for this growth screen.** AI-generated Cathie Wood-style simulation.

Revenue growth of 4.97% a year fails the 15% threshold, while latest R&D/revenue of 9.56% passes the 5% research threshold. Apple demonstrates reported research commitment, but that spending has not coincided with the historical revenue expansion required by this screen.

Research spending is an input, not proof of successful innovation. The facts do not establish new-product adoption, addressable-market expansion or future growth, so I would not turn research intensity into an unsupported forecast. I would reconsider if sustained growth accelerated and evidence connected research investment with commercially successful innovation.

Threshold retained: 15%, to preserve the same demanding growth standard across companies rather than tune it after seeing the result.

### AAPL: Burry

**Verdict: pass pending investigation.** AI-generated Burry-style simulation; amounts are USD millions.

Apple fails both checks. At 2025-09-27, operating cash flow of 111,482 is below net income of 112,010, breaking the every-year cash-backing requirement. Latest liabilities/equity of 2.61 exceeds the ceiling of 2.

The contrary evidence matters: at 2026-09-26, operating cash flow of 145,097 exceeds net income of 132,175, and liabilities/equity is below its earlier 5.96 reading. A historical cash shortfall and high liabilities relative to book equity warrant investigation; they do not prove fraud or insolvency. I would review working-capital movements, obligations and the equity base before changing this cautious verdict. No short position or price target follows from this screen.

## Threshold probe and known-answer validation

COST matches all five supplied liabilities/equity ratios (2.11, 1.75, 1.96, 1.64, 1.49), revenue growth of 7.51%, absent R&D in every year, and all seven panel checks. Buffett passes 3 of 3, Cathie Wood fails growth with R&D unknown, and Burry passes 2 of 2. Reference digits are assertions in verification, never inputs to the calculation.

The Cathie Wood skill's actual growth threshold was temporarily lowered to 5%, and COST's growth result changed from fail to pass while R&D stayed not known. The retained threshold is 15%, because the purpose is to apply a demanding growth criterion consistently, not fit a favorable answer after seeing a company. Apple's 4.97% growth still falls below the lower threshold. The facts do not change when a threshold changes; only the classification does.

## Apple: agreement, disagreement, bull and bear

The panel agrees on the underlying facts but applies different priorities. Buffett's tests accept Apple's returns and positive, endpoint-growing cash after capital spending; Cathie Wood accepts research intensity while rejecting the historical growth rate; Burry rejects the historical cash shortfall and latest liabilities relative to equity. This is not a majority vote on one proposition: the checks ask different questions, and the memos use the same source with correlated limitations. Buffett's watch verdict also shows that passing a screen need not mean owning the business.

**Bull case — AI-assisted analytical argument:** Apple passes every Buffett check, with owner earnings rising from 111,443 to 136,056 USD millions while remaining positive throughout. Its latest R&D intensity of 9.56% and operating cash flow above net income support continued business research despite the more skeptical screens.

**Bear case — AI-assisted analytical argument:** Revenue growth of 4.97% fails the growth screen, and the cash shortfall in the year ended 2025-09-27 breaks Burry's every-year earnings-backing requirement. Latest liabilities/equity of 2.61 also exceeds the ceiling, so strong ROE cannot by itself resolve balance-sheet risk or justify an investment.

These are prepared analytical arguments, not a record of a partner exchange. The decision above follows the disagreement: use the panel to identify questions, preserve unknowns, and investigate the flagged issues before a broader investment decision. Screening one holding does not establish the suitability of FNDX as a whole.

## What an agent panel means

An agent panel applies several role-specific instructions to common evidence, then compares their conclusions. Here code gathers and calculates the facts once, the investor skills guide separate model-written memos, and Streamlit displays them side by side. The app does not call a live language model or pretend a template generated an independent judgment; new data require fresh model memos. The skills use different objectives: durable cash earning power, innovation-oriented growth, and skeptical cash/balance-sheet analysis. They can disagree without any arithmetic disagreement.

The threshold probe demonstrates that a verdict depends on both evidence and a chosen rule. Passing is not a discovery of an objective dividing line between good and bad investments. Conversely, a failed rule does not establish fraud, insolvency, poor future returns or an unattractive price. The panel contains no price data, forecasts, maintenance-capital estimates or portfolio-risk model.

## Verification and reproducibility

`python lab19/panel.py --verify` checks the COST reference, missing inputs, inclusive thresholds, nonpositive equity, cash-flow failure, reconstruction from preserved SEC observations, every saved memo and an injected unsupported number in each investor's memo. Streamlit's AppTest checks both companies, three memo columns, the growth probe, and unsupported numbers in each editor. Existing Lab 18 tests are rerun to verify that its behavior is preserved. Verification is performed by the AI-assisted workflow; no student-performed check is claimed.

The number flag compares numeric tokens against printed amounts, percentages, dates, thresholds and check counts across every memo. It catches unsupported digits, but cannot establish that a printed value was attached to the right metric, year, unit or conclusion. Semantic review remains necessary.

From the repository root, with the existing environment:

```powershell
.venv-lab15/Scripts/python.exe lab19/panel.py --verify
.venv-lab15/Scripts/python.exe lab19/panel.py --print AAPL
.venv-lab15/Scripts/python.exe -m streamlit run lab19/panel.py
```

The compact Lab 19 deliverables are this report, `panel.py`, `results.json`, and the two `skills/*/SKILL.md` files. Keep the existing `lab18/skills/buffett-sec/scripts/buffett.py` and `lab18/requirements.txt` at their repository paths. No duplicate Lab 18 files are needed. The skills can be invoked by their explicit file paths. `--rebuild` recomputes results offline from preserved source observations and the current skill threshold; it clears memos if the threshold changed. The app supports new SEC downloads with a locally supplied name/email User-Agent and clears outdated memos when facts are refreshed.

## Sources and attribution

- [Lab 19 assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md) and [weekly handout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/student-handout.md), accessed November 5, 2026.
- [AI Boundary Card](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/AI-BOUNDARY-CARD.md): Project 2 has no Edition A checkpoint; the lab's expressly AI-off partner/code phases remain personal activities.
- FAskills philosophy sources: [Buffett](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md), [Cathie Wood](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/cathie_wood.md), [Burry](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md). FAskills was read, not installed; lab requirements override its broader data and valuation instructions.
- [SEC API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces); company-specific source links and timestamps appear with the printed panels.
- [Streamlit columns](https://docs.streamlit.io/develop/api-reference/layout/st.columns) supports the side-by-side memo layout.

OpenAI Codex assisted with implementation, source retrieval, calculations, validation, simulated investor memos and the proposed analytical decision. Reported amounts originate in SEC data; check thresholds and known-answer targets originate in course materials; memo judgments and the proposed decision are AI-assisted interpretations. Personal no-screen explanations, partner discussions, reflection delivery and Brightspace quiz completion are not represented as completed.


---
name: buffett-sec
description: Evaluate a ticker with the Lab 18 Buffett business-quality screen using five annual SEC 10-K periods, deterministic calculations, and a grounded qualitative memo. Use for Buffett-style business analysis, not stock-price valuation.
---

# Buffett business quality from SEC facts

Run the bundled `scripts/buffett.py` with the requested ticker. For this user's requested demonstration, set `SEC_USER_AGENT` to `placeholder placeholder@email.com`. This is a placeholder, not a verified SEC contact identity. No keys or paid sources are used. From the repository root:

```powershell
python .agents/skills/buffett-sec/scripts/buffett.py COST --out lab18/output
```

Read the printed report before judging. The script selects only annual flows in 10-K filings, uses the latest filing for the same period, follows the assignment's tag priorities, and computes all ratios and checks. Missing reported values stay `not found`; indeterminate ratios and checks stay `not known`. Do not substitute estimates, alternative tags, or the instructor's answer table for downloaded facts. Report discrepancies honestly.

Write `lab18/output/<TICKER>_memo.md` as a short, explicitly AI-generated Buffett-style simulation. Choose **own the business**, **watch it**, or **pass**. Use the printed report as the sole numerical source. Copy numeric expressions exactly, including percent signs and units; do not calculate extra numbers in prose. Explain earnings quality, consistency, limitations, and what would change the judgment. Missing owner earnings must explicitly prevent an owner-earnings judgment. Do not automatically equate passing checks with owning a business.

Adapt the philosophy of [Buffett's FAskills page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md): understandable businesses, durable earning power, prudent capital allocation, and patient ownership. The numbers alone do not establish a moat, management integrity, or financial strength. The lab overrides the page's maintenance-capital estimates, forecasts, scoring, prices, holdings and valuation instructions. Do not install FAskills or use its data services. Owner earnings here means operating cash flow less total capital spending, a classroom proxy rather than estimated maintenance spending.

Validate the memo with:

```powershell
python .agents/skills/buffett-sec/scripts/buffett.py COST --out lab18/output --check-memo lab18/output/COST_memo.md
```

Fix any unprinted numeric tokens, then run `python -m streamlit run lab18/app.py`. A token match establishes only that a number appeared, not that its financial interpretation is correct. When the user authorizes a proposed trust decision, append a clearly labeled AI-assisted decision for review. Never invent partner discussion or student-performed checks.

Discovery: install this directory in `.agents/skills/buffett-sec` at the repository root. [Official Codex skill documentation](https://developers.openai.com/codex/skills) describes discovery by name and description, followed by loading full instructions when needed.

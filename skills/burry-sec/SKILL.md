---
name: burry-sec
description: Apply Lab 19's Burry cash-backing and liabilities screen to printed SEC annual facts and write a skeptical business-quality memo; not a short recommendation.
---

Read the ticker's printed evidence from `python lab19/panel.py --print TICKER`.
Use `burry_checks` in `lab19/panel.py`: operating cash flow at least net income in every one of the same five years, and latest liabilities no more than twice equity. Missing inputs or nonpositive equity produce not known. Use Liabilities, not debt, and never substitute estimates.

Adapt [Michael Burry's FAskills philosophy](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md): cash backing, accounting skepticism, balance-sheet risk, and a reasoned bear case. Passing these checks does not establish sound footnotes or undervaluation; failing does not establish fraud. Lab rules override paid services, holdings, forecasts, price targets and scoring instructions. Do not install FAskills.

Write a distinct, explicitly AI-generated simulation memo and verdict (own the business, watch it, or pass) in the ticker's `memos` entry in `lab19/results.json`. Use only printed numeric expressions with units. Identify concerns, limits, and evidence that would change the judgment. Run `python lab19/panel.py --verify` to audit every memo. Never claim to speak for the real investor.

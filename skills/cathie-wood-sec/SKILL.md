---
name: cathie-wood-sec
description: Apply Lab 19's Cathie Wood growth and research screen to printed SEC annual facts and write a business-quality memo; not a stock valuation.
---

Read the ticker's printed evidence from `python lab19/panel.py --print TICKER`.
Use `cathie_checks` in `lab19/panel.py` for deterministic checks on the same five annual periods as Buffett and Burry. Growth threshold: **15%** (`growth_threshold: 0.15`). For the required probe temporarily set it to `0.05`, rebuild, inspect COST, and restore the retained threshold. R&D threshold is 5% of latest revenue. Missing inputs remain not known; never estimate R&D.

Adapt [Cathie Wood's FAskills philosophy](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/cathie_wood.md): innovation, research investment, long horizons, and skepticism toward interpreting short-term volatility as business deterioration. Historical growth and research spending alone do not establish disruption or future returns. Lab rules override the source's forecasts, price targets, holdings and paid data instructions. Do not install FAskills.

Write a distinct, explicitly AI-generated simulation memo and a verdict (own the business, watch it, or pass) in the ticker's `memos` entry in `lab19/results.json`. Use only printed numeric expressions with their units; explain contrary evidence, unknowns and what would change the judgment. Under the memo retain one threshold-choice line and reason. Run `python lab19/panel.py --verify` to audit every memo. Do not represent this as the real investor's opinion or a purchase-price judgment.

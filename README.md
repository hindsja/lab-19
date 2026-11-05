# Lab 18 — Legend Investor as Skill

Code computes the financial evidence; an AI-generated Buffett-style memo judges business quality. COST receives **watch it**: every numerical check passes, but these facts alone cannot establish a durable moat or prudent capital allocation. The trust decision appears directly below the COST memo and is labeled AI-assisted.

## Run

Extract the entire archive into a project folder, including `.agents`. From that folder:

```powershell
python -m pip install -r lab18/requirements.txt
python -m streamlit run lab18/app.py
```

Saved COST and JPM results load immediately. Select a ticker to view the chart, annual table, tags, checks and memo. Edit the memo to test `40.0%`; the app flags it. Save only the reviewed version.

To refresh SEC data and print the complete report with tags:

```powershell
$env:SEC_USER_AGENT = 'placeholder placeholder@email.com'
python .agents/skills/buffett-sec/scripts/buffett.py COST --out lab18/output
python .agents/skills/buffett-sec/scripts/buffett.py JPM --out lab18/output
```

The requested placeholder identity is prefilled in the app. It is not a verified contact identity; SEC may reject requests. The saved-data demonstration needs no contact entry or download. After refreshing, invoke the skill to regenerate the memo; the app does not substitute a fixed template for AI judgment.

```text
Use $buffett-sec on COST. Run the bundled script, read the printed evidence,
write lab18/output/COST_memo.md, and audit its numbers. Judge business quality,
not price. Repeat for JPM without estimating missing data.
```

## Method and limitations

Only USD facts from 10-K filings qualify. Annual flows span 350–380 days, allowing retail 52/53-week years. The latest five fiscal period ends are selected; the latest filing wins within each prescribed tag and matching period. Tag fallback follows the assignment independently each year. ROE equals net income divided by year-end equity; owner earnings equals operating cash flow less total capital spending. Missing values remain `not found`; indeterminate checks and invalid ROE remain `not known`.

The numeric audit compares memo tokens with printed values; it cannot detect a supported number attached to the wrong year or financial concept. The owner-earnings proxy includes expansion spending. Historical returns do not prove a moat, and no price-based conclusion is made.

## What the skill teaches

A skill packages reusable instructions with executable tools. Codex initially reads its name and description to select relevant skills, then loads detailed instructions when needed, reducing irrelevant context. Code fixes data selection, formulas and checks; the model judges the strength and limits of the evidence. Missing evidence is more informative than an estimate disguised as a reported fact.

In `year_row`, the script initializes the period, selects each metric using its allowed tags, extracts the input values, computes ROE only with positive equity and available income, and subtracts spending from cash flow only when both exist. `select_fact` returns a value of `None` when no eligible observation exists; `display` renders it as `not found` or `not known`.

## Evidence and sources

The validation file records all COST reference comparisons, JPM gaps and numeric probes. Raw SEC responses and their hashes preserve the downloaded evidence; JSON reports drive the app. AI assistance: OpenAI Codex generated/revised code, memos and the proposed decision and executed verification on November 3, 2026. No student-performed checks or partner exchanges are claimed.

- [Assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-18-legend-investor-as-skill.md)
- [Buffett philosophy](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md), read only; no FAskills installation or paid data
- [Codex skills](https://developers.openai.com/codex/skills)
- [SEC API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces); specific companyfacts URLs and retrieval times are in each report
- [Streamlit](https://docs.streamlit.io/develop/api-reference/charts/st.line_chart)

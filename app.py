"""Run from repository root: python -m streamlit run lab18/app.py."""
import json
import os
from pathlib import Path
import sys
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
skill_scripts = ROOT.parent / '.agents/skills/buffett-sec/scripts'
if not skill_scripts.exists():
    skill_scripts = ROOT / 'skills/buffett-sec/scripts'
sys.path.insert(0, str(skill_scripts))
from buffett import LABELS, clean_ticker, display, run, unsupported_numbers

st.set_page_config(page_title='Buffett business screen', layout='wide')
st.title('Buffett business screen')
st.caption('data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.')
ticker_input = st.text_input('Ticker', 'COST')
try:
    ticker = clean_ticker(ticker_input)
except ValueError as exc:
    st.error(str(exc))
    st.stop()
out = ROOT / 'output'
with st.expander('Download SEC facts'):
    contact = st.text_input('SEC User-Agent: your name and contact email',
                            value=os.environ.get('SEC_USER_AGENT', 'placeholder placeholder@email.com'), type='password')
    st.caption('Sent to SEC only. Not saved in reports. Existing saved results load without a new download.')
    if st.button('Download latest SEC facts'):
        try:
            with st.spinner('Reading SEC annual facts...'):
                run(ticker, out, contact)
            st.success('Facts updated. Review or regenerate the memo against the new report.')
        except Exception as exc:
            st.error(f'Download failed: {exc}')
report_path = out / f'{ticker}_facts.json'
if not report_path.exists():
    st.info('Download SEC facts above to begin. Then ask Codex to use $buffett-sec for this ticker and save its memo.')
    st.stop()
report = json.loads(report_path.read_text(encoding='utf-8'))
st.caption(f"{report['company']} | Retrieved UTC: {report['source']['retrieved_utc']}")
chart = pd.DataFrame([{'Fiscal year end': r['end'],
                       'Owner earnings': None if r['owner_earnings']['value'] is None else r['owner_earnings']['value'] / 1_000_000,
                       'Net income': None if r['net_income']['value'] is None else r['net_income']['value'] / 1_000_000}
                      for r in report['rows']])
st.line_chart(chart, x='Fiscal year end', y=['Owner earnings', 'Net income'], y_label='USD millions')
st.subheader('Annual facts')
st.caption('Amounts in USD millions. Missing data remain missing; ROE uses year-end equity.')
st.dataframe([{'Fiscal year end': r['end'], **{LABELS[m]: display(m, r[m]['value']) for m in LABELS}}
              for r in report['rows']], hide_index=True)
st.subheader('Code-computed checks')
st.table([{'Check': k, 'Result': v} for k, v in report['checks'].items()])
with st.expander('XBRL tags and filing evidence'):
    st.dataframe([{'Fiscal year end': r['end'], 'Metric': LABELS[m], 'Tag / formula': r[m]['tag'],
                   'Filed': r[m].get('filed', 'derived'), 'Accession': r[m].get('accession', '')}
                  for r in report['rows'] for m in LABELS], hide_index=True)
    st.link_button('SEC source JSON', report['source']['url'])
st.subheader('Buffett-style memo')
memo_path = out / f'{ticker}_memo.md'
memo = memo_path.read_text(encoding='utf-8') if memo_path.exists() else ''
edited = st.text_area('Memo editor — try adding ROE 40.0% to test the audit', memo,
                      height=260, key=f'memo_{ticker}_{report["source"]["sha256"]}')
if edited:
    st.markdown(edited)
    bad = unsupported_numbers(edited, report)
    if bad:
        st.error('Numbers not printed in the data report: ' + ', '.join(b['number'] for b in bad))
        st.dataframe(bad, hide_index=True)
    else:
        st.success('All numeric tokens appear in the printed data evidence.')
    st.caption('This audit checks numeric membership, not whether the memo attached a value to the correct metric or year. Review meaning too.')
    if st.button('Save memo'):
        memo_path.write_text(edited, encoding='utf-8')
        st.success('Memo saved locally.')
    st.download_button('Download memo', edited, f'{ticker}_memo.md', 'text/markdown')
else:
    st.info('Ask Codex to use $buffett-sec and write this ticker’s memo from the printed report. The app does not invent a model verdict.')

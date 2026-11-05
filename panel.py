"""Lab 19: shared SEC evidence, deterministic screens, model-written saved memos.

python lab19/panel.py --print COST
python lab19/panel.py --verify
python -m streamlit run lab19/panel.py
"""
import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'lab18/skills/buffett-sec/scripts'))
import buffett as base

RESULTS = ROOT / 'results.json'
INVESTORS = ('Buffett', 'Cathie Wood', 'Burry')
EXTRA = {'liabilities': 'Liabilities', 'rd': 'R&D',
         'rd_ratio': 'R&D / revenue', 'leverage': 'Liabilities / equity'}
LABELS = {**base.LABELS, **EXTRA}


def retained_threshold():
    text = (ROOT / 'skills/cathie-wood-sec/SKILL.md').read_text(encoding='utf-8')
    return float(re.search(r'growth_threshold: ([0-9.]+)', text).group(1))


def ratio(numerator, denominator):
    return numerator / denominator if numerator is not None and denominator is not None and denominator > 0 else None


def cathie_checks(growth, rd_ratio, threshold):
    # Missing evidence is unknown, never a zero or an automatic failure.
    growth_result = 'not known' if growth is None else ('pass' if growth >= threshold else 'fail')
    rd_result = 'not known' if rd_ratio is None else ('pass' if rd_ratio >= 0.05 else 'fail')
    return {f'Revenue grew {threshold:.0%} or more a year, first year to last': growth_result,
            'R&D 5% or more of revenue, latest year': rd_result}


def burry_checks(rows):
    pairs = [(r['operating_cash_flow']['value'], r['net_income']['value']) for r in rows]
    cash_result = 'not known'
    if len(pairs) == 5 and all(c is not None and n is not None for c, n in pairs):
        cash_result = 'pass' if all(c >= n for c, n in pairs) else 'fail'
    leverage = rows[-1]['leverage']['value'] if rows else None
    return {'Operating cash flow at least net income every year': cash_result,
            'Liabilities no more than twice equity, latest year':
                'not known' if leverage is None else ('pass' if leverage <= 2 else 'fail')}


def build(ticker, facts, source, threshold=None):
    report = base.build_report(ticker, facts, source)
    tags = {t for group in base.TAGS.values() for t in group} | {'Liabilities', 'ResearchAndDevelopmentExpense', 'ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost'}
    # Preserve the source observations needed for offline reconstruction in one file.
    report['input_facts'] = {'entityName': facts.get('entityName', ''), 'facts': {'us-gaap': {
        tag: value for tag, value in facts.get('facts', {}).get('us-gaap', {}).items() if tag in tags}}}
    for row in report['rows']:
        row['liabilities'] = base.select_fact(facts, ['Liabilities'], row['start'], row['end'], instant=True)
        row['rd'] = base.select_fact(facts, ['ResearchAndDevelopmentExpense',
            'ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost'], row['start'], row['end'])
        for metric, numerator, denominator in [('rd_ratio', 'rd', 'revenue'), ('leverage', 'liabilities', 'equity')]:
            row[metric] = {'value': ratio(row[numerator]['value'], row[denominator]['value']),
                           'tag': f"derived: {row[numerator]['tag']} / {row[denominator]['tag']}"}
    rows = report['rows']
    growth = None
    if len(rows) == 5:
        relative = ratio(rows[-1]['revenue']['value'], rows[0]['revenue']['value'])
        if relative is not None and relative >= 0:
            growth = relative ** 0.25 - 1
    report['growth'] = growth
    report['threshold'] = retained_threshold() if threshold is None else threshold
    report['panel'] = {'Buffett': report['checks'],
        'Cathie Wood': cathie_checks(growth, rows[-1]['rd_ratio']['value'], report['threshold']),
        'Burry': burry_checks(rows)}
    report['memos'] = {}
    return report


def display(metric, value):
    if metric in ('rd_ratio', 'leverage', 'growth'):
        if value is None:
            return 'not known'
        return f'{value:.2%}' if metric != 'leverage' else f'{value:.2f}'
    return base.display(metric, value)


def panel_rows(report):
    return [{'Investor': investor, 'Check': check, 'Result': result}
            for investor, checks in report['panel'].items() for check, result in checks.items()]


def evidence(report):
    lines = [f"## {report['ticker']} — {report['company']}", '',
        'Amounts in USD millions; ratios are dimensionless. Missing R&D is not found; its ratio and check are not known.', '',
        '| FY end | ' + ' | '.join(LABELS.values()) + ' |', '|---|' + '---:|' * len(LABELS)]
    for row in report['rows']:
        lines.append('| ' + row['end'] + ' | ' + ' | '.join(display(m, row[m]['value']) for m in LABELS) + ' |')
    lines += ['', f"Revenue growth a year: **{display('growth', report['growth'])}**.",
        f"Thresholds: growth {report['threshold']:.0%}; R&D 5%; ROE 15%; liabilities / equity 2.", '',
        '| Investor | Check | Result |', '|---|---|---|']
    lines += [f"| {r['Investor']} | {r['Check']} | {r['Result']} |" for r in panel_rows(report)]
    for investor, checks in report['panel'].items():
        lines.append(f"{investor}: {list(checks.values()).count('pass')} of {len(checks)} checks pass.")
    lines += ['', f"SEC source: {report['source']['url']}",
              f"Retrieved UTC: {report['source']['retrieved_utc']}", f"SHA-256: {report['source']['sha256']}"]
    return '\n'.join(lines)


def audit(memos, report):
    # Allow only printed financial expressions, dates, thresholds and printed counts.
    tokens = ['15%', '5%', '2', f"{report['threshold']:.0%}", display('growth', report['growth'])]
    for row in report['rows']:
        tokens += [row['end']] + [display(m, row[m]['value']) for m in LABELS]
    for checks in report['panel'].values():
        tokens += [str(len(checks)), str(list(checks.values()).count('pass'))]
    allowed = {base.normalize(t) for t in tokens if base.NUMBER.fullmatch(t)}
    return [{'Investor': investor, 'number': match.group(), 'position': match.start()}
            for investor, memo in memos.items() for match in base.NUMBER.finditer(memo)
            if base.normalize(match.group()) not in allowed]


def load():
    return json.loads(RESULTS.read_text(encoding='utf-8')) if RESULTS.exists() else {}


def save(data):
    RESULTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def verify(data):
    cost = data['COST']
    assert [r['end'] for r in cost['rows']] == ['2022-08-28', '2023-09-03', '2024-09-01', '2025-08-31', '2026-08-30']
    assert [display('leverage', r['leverage']['value']) for r in cost['rows']] == ['2.11', '1.75', '1.96', '1.64', '1.49']
    assert display('growth', cost['growth']) == '7.51%'
    assert all(r['rd']['value'] is None for r in cost['rows'])
    assert [r['Result'] for r in panel_rows(cost)] == ['pass', 'pass', 'pass', 'fail', 'not known', 'pass', 'pass']
    assert list(cathie_checks(cost['growth'], None, .05).values()) == ['pass', 'not known']
    assert list(cathie_checks(None, None, .15).values()) == ['not known', 'not known']
    assert list(cathie_checks(.15, .05, .15).values()) == ['pass', 'pass']
    assert ratio(10, 0) is None and ratio(10, -1) is None
    missing = deepcopy(cost['rows'])
    missing[0]['net_income']['value'] = None
    assert list(burry_checks(missing).values())[0] == 'not known'
    failing = deepcopy(cost['rows'])
    failing[0]['operating_cash_flow']['value'] = 0
    assert list(burry_checks(failing).values())[0] == 'fail'
    for ticker, report in data.items():
        rebuilt = build(ticker, report['input_facts'], report['source'], report['threshold'])
        assert rebuilt['rows'] == report['rows'] and rebuilt['panel'] == report['panel'], f'{ticker}: offline reconstruction mismatch'
        assert set(report['memos']) == set(INVESTORS), f'{ticker}: missing memo'
        assert not audit(report['memos'], report), audit(report['memos'], report)
        for investor in INVESTORS:
            probe = dict(report['memos'])
            probe[investor] += '\nInvented ratio 98765.43%.'
            assert any(x['Investor'] == investor for x in audit(probe, report))
    return 'PASS: COST reference, threshold probe, missing inputs, inclusive thresholds, nonpositive equity, cash failure, all memo audits and injected-number probes.'


def app():
    import pandas as pd
    import streamlit as st
    st.set_page_config(page_title='Legend Panel', layout='wide')
    st.title('Legend Panel')
    st.caption('data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.')
    data = load()
    ticker = st.text_input('Ticker', 'COST').strip().upper()
    with st.expander('Download SEC facts'):
        contact = st.text_input('SEC User-Agent: your name and contact email', os.environ.get('SEC_USER_AGENT', ''), type='password')
        if st.button('Download latest SEC facts'):
            try:
                facts, source = base.fetch(ticker, ROOT / 'output', contact)
                data[ticker] = build(ticker, facts, source)
                save(data)
                st.success('Facts updated; regenerate model memos from the new printed evidence.')
            except Exception as exc:
                st.error(str(exc))
    if ticker not in data:
        st.info('Download this ticker to begin. Ask the three skills to write memos from its printed evidence.')
        st.stop()
    report = data[ticker]
    st.caption(f"{report['company']} | Retrieved UTC: {report['source']['retrieved_utc']}")
    st.line_chart(pd.DataFrame([{'FY end': r['end'], **{LABELS[m]: None if r[m]['value'] is None else r[m]['value']/1e6
        for m in ('owner_earnings', 'net_income')}} for r in report['rows']]), x='FY end', y_label='USD millions')
    st.subheader('Annual facts — USD millions')
    st.dataframe([{'FY end': r['end'], **{LABELS[m]: display(m, r[m]['value']) for m in LABELS}} for r in report['rows']], hide_index=True)
    st.write(f"Revenue growth a year: {display('growth', report['growth'])}")
    st.table(panel_rows(report))
    edited = {}
    for column, investor in zip(st.columns(3), INVESTORS):
        with column:
            st.subheader(investor)
            checks = report['panel'][investor]
            st.caption(f"{list(checks.values()).count('pass')} of {len(checks)} checks pass")
            memo = report['memos'].get(investor, '')
            edited[investor] = st.text_area('Memo editor', memo, height=290, key=f'{ticker}_{investor}_{report["source"]["sha256"]}')
            if edited[investor]:
                st.markdown(edited[investor])
            else:
                st.info('Model memo and verdict not yet written.')
            if investor == 'Cathie Wood':
                st.caption(f"Retain {report['threshold']:.0%}: preserve the demanding growth screen; do not tune the rule to make COST pass.")
    bad = audit(edited, report)
    if bad:
        st.error('Unprinted numbers across panel: ' + ', '.join(f"{b['Investor']}: {b['number']}" for b in bad))
        st.dataframe(bad, hide_index=True)
    elif all(edited.values()):
        st.success('All memo numeric tokens appear in printed evidence.')
    else:
        st.warning('Panel incomplete: a memo is missing.')
    st.caption('Numeric membership does not verify meaning, units, the correct year, or the judgment.')
    if st.button('Save all memos'):
        data[ticker]['memos'] = edited
        save(data)
        st.success('Saved locally.')
    st.download_button('Download panel and memos', evidence(report) + '\n\n' + '\n\n'.join(edited.values()), f'{ticker}_panel.md')
    with st.expander('Growth threshold probe'):
        threshold = st.slider('Growth threshold (%)', 0, 30, int(report['threshold']*100)) / 100
        st.table(cathie_checks(report['growth'], report['rows'][-1]['rd_ratio']['value'], threshold))
        st.caption('Preview only; retained threshold lives in the Cathie Wood skill. Saved memos describe the retained rule.')
    with st.expander('XBRL tags and filing evidence'):
        st.dataframe([{'FY end': r['end'], 'Metric': LABELS[m], **r[m]} for r in report['rows'] for m in LABELS], hide_index=True)
        st.link_button('SEC source JSON', report['source']['url'])
    st.download_button('Download saved results', json.dumps(data, indent=2), 'results.json')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--print', dest='ticker')
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--rebuild', action='store_true')
    args = parser.parse_args()
    if args.rebuild:
        data = load()
        for ticker, old in list(data.items()):
            new = build(ticker, old['input_facts'], old['source'])
            new['memos'] = old['memos'] if new['threshold'] == old['threshold'] else {}
            if 'selection' in old:
                new['selection'] = old['selection']
            data[ticker] = new
        save(data)
        print('Rebuilt from preserved source observations; changed-threshold memos cleared.')
    elif args.ticker:
        print(evidence(load()[base.clean_ticker(args.ticker)]))
    elif args.verify:
        print(verify(load()))
    else:
        app()


if __name__ == '__main__':
    main()

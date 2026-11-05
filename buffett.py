"""SEC annual facts and deterministic Lab 18 Buffett checks; standard library only."""
import argparse
from datetime import date, datetime, timezone
from decimal import Decimal
import hashlib
import json
import math
import os
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen

TAGS = {
    'revenue': ['RevenueFromContractWithCustomerExcludingAssessedTax', 'Revenues'],
    'net_income': ['NetIncomeLoss'],
    'operating_cash_flow': ['NetCashProvidedByUsedInOperatingActivities'],
    'capital_spending': ['PaymentsToAcquirePropertyPlantAndEquipment', 'PaymentsToAcquireProductiveAssets'],
    'equity': ['StockholdersEquity'],
}
LABELS = {'revenue': 'Revenue', 'net_income': 'Net income',
          'operating_cash_flow': 'Operating cash flow', 'capital_spending': 'Capital spending',
          'equity': 'Equity', 'roe': 'ROE', 'owner_earnings': 'Owner earnings'}
TICKERS_URL = 'https://www.sec.gov/files/company_tickers.json'


def clean_ticker(ticker):
    ticker = ticker.strip().upper()
    if not re.fullmatch(r'[A-Z][A-Z0-9.-]{0,14}', ticker):
        raise ValueError('Enter a ticker using letters, digits, dots or hyphens.')
    return ticker


def download(url, user_agent):
    if not re.search(r'\S+@\S+\.\S+', user_agent or '') or len(user_agent.split()) < 2:
        raise ValueError('Set SEC_USER_AGENT to your name and contact email before downloading.')
    time.sleep(0.2)  # Remain below SEC's request-rate ceiling, even for tiny responses.
    request = Request(url, headers={'User-Agent': user_agent, 'Accept': 'application/json'})
    with urlopen(request, timeout=60) as response:
        raw = response.read()
    return json.loads(raw), raw


def fetch(ticker, out, user_agent):
    ticker = clean_ticker(ticker)
    tickers, _ = download(TICKERS_URL, user_agent)
    matches = [v for v in tickers.values() if v['ticker'].upper() == ticker]
    if len(matches) != 1:
        raise ValueError(f'Ticker {ticker} not uniquely found in SEC ticker list.')
    cik = str(matches[0]['cik_str']).zfill(10)
    url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
    facts, raw = download(url, user_agent)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    raw_path = out / 'sources' / f'{ticker}_{stamp}.json'
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_bytes(raw)
    return facts, {'url': url, 'retrieved_utc': stamp, 'sha256': hashlib.sha256(raw).hexdigest(),
                   'raw_file': 'sources/' + raw_path.name}


def annual(fact):
    if fact.get('form') != '10-K' or not fact.get('start'):
        return False
    days = (date.fromisoformat(fact['end']) - date.fromisoformat(fact['start'])).days + 1
    # Allows calendar years and retail 52/53-week years, excludes quarterly/YTD flows.
    return 350 <= days <= 380


def entries(facts, tag):
    return facts.get('facts', {}).get('us-gaap', {}).get(tag, {}).get('units', {}).get('USD', [])


def fiscal_periods(facts):
    periods = {}
    for metric, tags in TAGS.items():
        if metric == 'equity':
            continue
        for tag in tags:
            for fact in entries(facts, tag):
                if annual(fact):
                    key = (fact['filed'], fact.get('accn', ''))
                    end = fact['end']
                    if end not in periods or key > periods[end][0]:
                        periods[end] = (key, fact['start'])
    return [(periods[end][1], end) for end in sorted(periods)[-5:]]


def select_fact(facts, tags, start, end, instant=False):
    for tag in tags:  # Priority is per period, not across the entire history.
        candidates = [f for f in entries(facts, tag)
                      if f.get('form') == '10-K' and f.get('end') == end
                      and (not f.get('start') if instant else annual(f) and f['start'] == start)]
        if not candidates:
            continue
        latest = max(f['filed'] for f in candidates)
        candidates = [f for f in candidates if f['filed'] == latest]
        values = {f['val'] for f in candidates}
        if len(values) != 1:
            raise ValueError(f'Conflicting latest-filed values for {tag} at {end}. Inspect source.')
        f = max(candidates, key=lambda item: item.get('accn', ''))
        if not isinstance(f['val'], (int, float)) or not math.isfinite(f['val']):
            raise ValueError(f'Invalid numeric value for {tag} at {end}.')
        return {'value': f['val'], 'tag': 'us-gaap:' + tag, 'filed': f['filed'],
                'accession': f.get('accn'), 'start': f.get('start'), 'end': end}
    return {'value': None, 'tag': 'not found (searched ' + ', '.join(tags) + ')'}


def year_row(facts, start, end):
    """Turn one annual period into a row; the partner-explanation entry point."""
    row = {'start': start, 'end': end}
    for metric, tags in TAGS.items():
        row[metric] = select_fact(facts, tags, start, end, instant=metric == 'equity')
    income = row['net_income']['value']
    equity = row['equity']['value']
    cash = row['operating_cash_flow']['value']
    capex = row['capital_spending']['value']
    row['roe'] = {'value': income / equity if income is not None and equity is not None and equity > 0 else None,
                  'tag': 'derived: ' + row['net_income']['tag'] + ' / ' + row['equity']['tag']}
    row['owner_earnings'] = {'value': cash - capex if cash is not None and capex is not None else None,
                            'tag': 'derived: ' + row['operating_cash_flow']['tag'] + ' - ' + row['capital_spending']['tag']}
    return row


def checks(rows):
    def every(metric, predicate):
        vals = [r[metric]['value'] for r in rows]
        if len(vals) != 5 or any(v is None for v in vals):
            return 'not known'
        return 'pass' if all(predicate(v) for v in vals) else 'fail'
    growth = 'not known'
    if len(rows) == 5:
        first, last = rows[0]['owner_earnings']['value'], rows[-1]['owner_earnings']['value']
        if first is not None and last is not None:
            growth = 'pass' if last > first else 'fail'
    return {'ROE of 15% or more every year': every('roe', lambda v: v >= 0.15),
            'Owner earnings positive every year': every('owner_earnings', lambda v: v > 0),
            'Owner earnings grew, first year to last': growth}


def display(metric, value):
    if value is None:
        return 'not known' if metric == 'roe' else 'not found'
    if metric == 'roe':
        return f'{value * 100:.1f}%'
    return f'{value / 1_000_000:,.6f}'.rstrip('0').rstrip('.')


def report_text(report):
    lines = [f"# {report['ticker']} — SEC annual facts", '',
             'Amounts in USD millions; ROE uses year-end equity. Fiscal-year-end dates identify periods.', '',
             '| FY end | ' + ' | '.join(LABELS.values()) + ' |',
             '|---|' + '---:|' * len(LABELS)]
    for row in report['rows']:
        lines.append('| ' + row['end'] + ' | ' + ' | '.join(display(m, row[m]['value']) for m in LABELS) + ' |')
    lines += ['', '## Code-computed checks', '']
    lines += [f'- {label}: **{value}**' for label, value in report['checks'].items()]
    lines += ['', '## Tags and filing provenance', '']
    for row in report['rows']:
        lines += [f"### Fiscal year ended {row['end']} (flows start {row['start']})", '']
        for metric in LABELS:
            fact = row[metric]
            suffix = f"; filed {fact['filed']}; accession {fact['accession']}" if fact.get('filed') else ''
            lines.append(f"- {LABELS[metric]}: {display(metric, fact['value'])}; {fact['tag']}{suffix}")
        lines.append('')
    lines += ['## Source', '', report['source']['url'],
              'Retrieved UTC: ' + report['source']['retrieved_utc'],
              'Source SHA-256: ' + report['source']['sha256'], '',
              'Latest eligible filing wins per period and tag. This is a current/revised history, not a historical trading backtest.',
              'Owner earnings is the lab cash-flow proxy. It does not separate maintenance from growth capital spending.']
    return '\n'.join(lines) + '\n'


# Strict printed-token audit: retains percent units and treats dates as entire tokens.
NUMBER = re.compile(r'\d{4}-\d{2}-\d{2}|(?<![\w.])[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:\s*%)?(?!\w|\.\d)')


def normalize(token):
    token = token.replace(',', '').replace(' ', '')
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', token):
        return token
    percent = token.endswith('%')
    return (str(Decimal(token.rstrip('%')).normalize()), percent)


def unsupported_numbers(memo, report):
    # Only displayed data values, dates and the printed check threshold are evidence.
    tokens = ['15%']
    for row in report['rows']:
        tokens += [row['end'], row['start']]
        tokens += [display(metric, row[metric]['value']) for metric in LABELS if row[metric]['value'] is not None]
    allowed = {normalize(t) for t in tokens}
    return [{'number': m.group(), 'position': m.start()} for m in NUMBER.finditer(memo)
            if normalize(m.group()) not in allowed]


def build_report(ticker, facts, source):
    rows = [year_row(facts, start, end) for start, end in fiscal_periods(facts)]
    if not rows:
        raise ValueError('No eligible annual USD facts in 10-K filings.')
    return {'ticker': clean_ticker(ticker), 'company': facts.get('entityName', ''),
            'rows': rows, 'checks': checks(rows), 'source': source}


def run(ticker, out, user_agent):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    facts, source = fetch(ticker, out, user_agent)
    report = build_report(ticker, facts, source)
    (out / f'{ticker}_facts.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    (out / f'{ticker}_facts.md').write_text(report_text(report), encoding='utf-8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ticker')
    parser.add_argument('--out', type=Path, default=Path('lab18/output'))
    parser.add_argument('--check-memo', type=Path)
    args = parser.parse_args()
    ticker = clean_ticker(args.ticker)
    if args.check_memo:
        report = json.loads((args.out / f'{ticker}_facts.json').read_text(encoding='utf-8'))
        bad = unsupported_numbers(args.check_memo.read_text(encoding='utf-8'), report)
        print(json.dumps({'unsupported_numbers': bad}, indent=2))
        return bool(bad)
    report = run(ticker, args.out, os.environ.get('SEC_USER_AGENT', ''))
    print(report_text(report))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

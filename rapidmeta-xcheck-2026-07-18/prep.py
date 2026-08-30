"""Build the checkable universe: app -> trials(NCT, per-arm counts) from the served corpus."""
import json, os, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

W = os.path.dirname(os.path.abspath(__file__))
# Corpus location is configuration, not a literal. The previous value was an
# absolute path on one machine, so this script could only ever run there, and
# anywhere else it died on the open() below with a bare FileNotFoundError.
SRC = os.environ.get('BIAS_SHADOW_CORPUS') or os.path.join(W, 'corpus_records.jsonl')
if not os.path.isfile(SRC):
    sys.exit(
        'corpus not found: ' + SRC
        + ' -- set BIAS_SHADOW_CORPUS to the corpus_records.jsonl produced by'
        + ' the bias-shadow lane, or place that file next to this script.'
    )

recs = [json.loads(l) for l in open(SRC, encoding='utf-8')]
ok = [r for r in recs if r.get('status') == 'ok']

ncts = set()
app_trials = {}
for r in ok:
    rows = []
    for t in (r.get('trials') or []):
        i = t.get('id')
        if isinstance(i, str) and i.upper().startswith('NCT'):
            n = i.upper()
            ncts.add(n)
            rows.append({'nct': n, 'tE': t.get('tE'), 'cE': t.get('cE'),
                         'tN': t.get('tN'), 'cN': t.get('cN'),
                         'y': t.get('y'), 'v': t.get('v')})
    if rows:
        app_trials[r['app']] = {'measure': r.get('measure'), 'k': len(rows), 'trials': rows}

json.dump(sorted(ncts), open(os.path.join(W, 'ncts.json'), 'w'))
json.dump(app_trials, open(os.path.join(W, 'app_trials.json'), 'w'))

n_pairs = sum(len(v['trials']) for v in app_trials.values())
n_counts = sum(1 for v in app_trials.values() for t in v['trials']
               if t['tE'] is not None and t['cE'] is not None)
n_denom = sum(1 for v in app_trials.values() for t in v['trials']
              if t['tN'] is not None and t['cN'] is not None)
print('total html      ', len(recs))
print('analyzable apps ', len(ok))
print('apps with >=1 NCT', len(app_trials))
print('unique NCTs     ', len(ncts))
print('(app,trial) pairs', n_pairs)
print('  with both event counts tE&cE:', n_counts)
print('  with both denominators tN&cN:', n_denom)

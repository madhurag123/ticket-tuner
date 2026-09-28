import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_no_template_leakage():
 rows=json.loads((ROOT/'data/tickets.json').read_text());groups={s:{r['template_group'] for r in rows if r['split']==s} for s in ['train','validation','test']}
 assert not (groups['train']&groups['test'] or groups['train']&groups['validation'] or groups['test']&groups['validation'])
def test_unique_texts():
 rows=json.loads((ROOT/'data/tickets.json').read_text());assert len({r['text'] for r in rows})==len(rows)
def test_evaluation_bounds():
 p=ROOT/'artifacts/evaluation.json'
 if not p.exists():return
 m=json.loads(p.read_text());assert 0<=m['holdout_finetuned']['macro_f1']<=1

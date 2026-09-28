from pathlib import Path
from functools import lru_cache
import json
ROOT=Path(__file__).parent
@lru_cache(maxsize=1)
def load():
 from transformers import AutoTokenizer,AutoModelForSeq2SeqLM
 import torch
 torch.set_num_threads(4);path=ROOT/'artifacts/model'
 if not path.exists():raise ValueError('Trained model missing. Run python generate.py then python train.py first.')
 return AutoTokenizer.from_pretrained(path),AutoModelForSeq2SeqLM.from_pretrained(path).eval()
def analyze(p):
 text=p.get('text','I need a refund for a duplicate charge.')
 if not isinstance(text,str) or not 5<=len(text)<=2000:raise ValueError('Enter 5–2,000 characters')
 import torch
 tokenizer,model=load();x=tokenizer('Classify the support request as billing, access, or bug. Reply with only the category. Request: '+text,return_tensors='pt',truncation=True,max_length=96)
 with torch.no_grad():label=tokenizer.decode(model.generate(**x,max_new_tokens=5)[0],skip_special_tokens=True).strip().lower()
 report=json.loads((ROOT/'artifacts/evaluation.json').read_text());valid=label in ['billing','access','bug']
 return dict(metrics={'Routing category':label if valid else 'needs review','Holdout macro F1':round(report['holdout_finetuned']['macro_f1'],3),'Training examples':report['split_sizes']['train']},answer=('Suggested routing: '+label+'. Human review required.') if valid else 'The model produced an unsupported label; route to a human.',notice='Actual locally fine-tuned small language model output. No ticket is sent to a service. Long inputs are truncated at 96 tokens.',details=report)

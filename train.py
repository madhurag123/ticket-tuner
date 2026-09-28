from pathlib import Path
import os
os.environ.setdefault('HF_HOME', str(Path(__file__).resolve().parent/'var/hf-cache'))
"""Real seq2seq fine-tuning with validation-only checkpoint selection."""
import os,json,random,time
from pathlib import Path
os.environ.setdefault('TOKENIZERS_PARALLELISM','false')
import numpy as np,torch
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix
ROOT=Path(__file__).parent;torch.set_num_threads(4);random.seed(28);np.random.seed(28);torch.manual_seed(28)
meta=json.loads((ROOT/'model-source.json').read_text());source=os.environ.get('BASE_MODEL',meta['model'])
kwargs={} if Path(source).exists() else {'revision':meta['revision']}
tokenizer=AutoTokenizer.from_pretrained(source,**kwargs);model=AutoModelForSeq2SeqLM.from_pretrained(source,**kwargs)
rows=json.loads((ROOT/'data/tickets.json').read_text());splits={s:[r for r in rows if r['split']==s] for s in ['train','validation','test']}
for a,b in [('train','validation'),('train','test'),('validation','test')]:assert not {r['template_group'] for r in splits[a]}&{r['template_group'] for r in splits[b]}
def prompt(t):return 'Classify the support request as billing, access, or bug. Reply with only the category. Request: '+t

def infer(data):
 model.eval();pred=[]
 with torch.no_grad():
  for i in range(0,len(data),16):
   x=tokenizer([prompt(r['text']) for r in data[i:i+16]],padding=True,truncation=True,max_length=96,return_tensors='pt')
   pred.extend(s.strip().lower() for s in tokenizer.batch_decode(model.generate(**x,max_new_tokens=5),skip_special_tokens=True))
 return pred

def metrics(data,pred):
 y=[r['label'] for r in data];return {'accuracy':float(accuracy_score(y,pred)),'macro_f1':float(f1_score(y,pred,labels=['billing','access','bug'],average='macro',zero_division=0)),'invalid_labels':sum(x not in ['billing','access','bug'] for x in pred)}
start=time.monotonic();zero_val=metrics(splits['validation'],infer(splits['validation']));opt=torch.optim.AdamW(model.parameters(),lr=1e-4);best=-1;history=[];out=ROOT/'artifacts/model';out.mkdir(parents=True,exist_ok=True)
for epoch in range(5):
 model.train();batch=list(splits['train']);random.shuffle(batch);losses=[]
 for i in range(0,len(batch),8):
  part=batch[i:i+8];x=tokenizer([prompt(r['text']) for r in part],padding=True,truncation=True,max_length=96,return_tensors='pt');labels=tokenizer([r['label'] for r in part],padding=True,return_tensors='pt').input_ids;labels[labels==tokenizer.pad_token_id]=-100
  opt.zero_grad();loss=model(**x,labels=labels).loss;loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.0);opt.step();losses.append(loss.item())
 val=metrics(splits['validation'],infer(splits['validation']));history.append({'epoch':epoch+1,'train_loss':float(np.mean(losses)),**val});print(history[-1],flush=True)
 if val['macro_f1']>best:best=val['macro_f1'];model.save_pretrained(out,safe_serialization=True);tokenizer.save_pretrained(out)
model=AutoModelForSeq2SeqLM.from_pretrained(out);pred=infer(splits['test']);base=make_pipeline(TfidfVectorizer(ngram_range=(1,2)),LogisticRegression(max_iter=1000)).fit([r['text'] for r in splits['train']],[r['label'] for r in splits['train']]);bp=base.predict([r['text'] for r in splits['test']])
report={'model_source':meta,'seed':28,'split_sizes':{k:len(v) for k,v in splits.items()},'split_unit':'template family; all item expansions remain in one split','validation_zero_shot':zero_val,'epochs':history,'holdout_finetuned':metrics(splits['test'],pred),'holdout_tfidf_baseline':metrics(splits['test'],bp),'holdout_majority_accuracy':1/3,'seconds':round(time.monotonic()-start,2),'predictions':[{'id':r['id'],'expected':r['label'],'predicted':p} for r,p in zip(splits['test'],pred)],'limitations':'Authored synthetic language only; no user tickets; tiny heldout template set. Test was used once after validation checkpoint selection.'}
(ROOT/'artifacts/evaluation.json').write_text(json.dumps(report,indent=2));print(report['holdout_finetuned'],flush=True)

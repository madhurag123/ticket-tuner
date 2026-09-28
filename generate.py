from pathlib import Path
import json,random
ROOT=Path(__file__).parent
# Distinct phrasings are allocated before expansion, so template groups never cross splits.
patterns={
'billing':['I was charged twice for {item}.','Please refund the payment for {item}.','The invoice for {item} has the wrong amount.','Why did my bill increase for {item}?','Cancel the renewal charge for {item}.','My credit card was debited but {item} is unpaid.','Can I get a receipt for {item}?','I need to change the payment method for {item}.','An unexpected fee appeared on {item}.','The subscription price for {item} is incorrect.','Please reverse the duplicate transaction for {item}.','Explain the tax included in {item}.','The discount was not applied to {item}.','My account shows an overdue invoice for {item}.','Can you correct the billing address on {item}?'],
'access':['I cannot sign in to {item}.','Reset my password for {item}.','The login code for {item} never arrived.','My account is locked out of {item}.','I lost my authenticator for {item}.','My credentials are rejected by {item}.','How can I recover access to {item}?','The verification link for {item} expired.','I need to update the email used to log into {item}.','Two factor authentication blocks {item}.','The sign-in page keeps rejecting me for {item}.','I forgot which username I use for {item}.','My session expires immediately in {item}.','The invitation to access {item} does not work.','I cannot verify my identity for {item}.'],
'bug':['The export button crashes {item}.','A blank screen appears in {item}.','The search results are broken in {item}.','An error appears when saving {item}.','The chart does not load in {item}.','The application freezes while opening {item}.','The file upload fails in {item}.','I found a display defect in {item}.','The download generates an empty file for {item}.','Data disappears after refreshing {item}.','The page returns a server error in {item}.','The filters show incorrect results in {item}.','The date selector is not responding in {item}.','The mobile layout is unreadable in {item}.','The application hangs during synchronization of {item}.']}
items=['the team workspace','the monthly plan','the reporting portal','the shared dashboard','the project account','the starter service','the analysis tool','the customer portal']
rows=[]
for label,templates in patterns.items():
 for group,template in enumerate(templates):
  split='train' if group<9 else 'validation' if group<12 else 'test'
  for item in items:rows.append({'id':f'{label}-{group}-{items.index(item)}','text':template.format(item=item),'label':label,'template_group':f'{label}-{group}','split':split})
(ROOT/'data').mkdir(exist_ok=True);(ROOT/'data/tickets.json').write_text(json.dumps(rows,indent=2))

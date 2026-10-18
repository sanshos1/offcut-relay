import json,os,re
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));WORKSPACE=os.path.abspath(os.path.join(ROOT,'..','..','..','..'))
def value(name):
 text=open(os.path.join(WORKSPACE,'accounts.env'),encoding='utf-8').read();m=re.search(rf'^\s*{name}\s*=\s*"?([^"\r\n]+)',text,re.M)
 if not m:raise SystemExit(name+' missing')
 return m.group(1).strip()
def address_from(x):
 if isinstance(x,dict):
  if x.get('recipient') and str(x.get('tx_execution_result',''))=='1':return x['recipient']
  for k,v in x.items():
   if k in ('contract_address','contractAddress') and isinstance(v,str):return v
   found=address_from(v)
   if found:return found
 if isinstance(x,list):
  for v in x:
   found=address_from(v)
   if found:return found
def main():
 if value('ACCOUNT_3_GITHUB_USERNAME')!='sanshos1':raise SystemExit('Account slot mismatch')
 account=create_account(account_private_key=value('ACCOUNT_3_GENLAYER_PRIVATE_KEY'));client=create_client(chain=studionet,account=account)
 expected='0xAD049E0Edc298C97552eD60071a35bfc60181FD4'
 if account.address.lower()!=expected.lower():raise SystemExit('Wallet mismatch')
 code=open(os.path.join(ROOT,'contracts','contract.py'),encoding='utf-8').read();tx=client.deploy_contract(code=code,args=[]);print('deployTx',tx,flush=True)
 receipt=client.wait_for_transaction_receipt(transaction_hash=tx,wait_until='finalized',retries=180,interval=5000,full_transaction=True);address=address_from(receipt)
 leaders=receipt.get('consensus_data',{}).get('leader_receipt')or[];leaders=[leaders] if isinstance(leaders,dict) else leaders
 if not address or receipt.get('result_name')!='MAJORITY_AGREE' or not any(x.get('execution_result')=='SUCCESS' for x in leaders):raise SystemExit('Deployment did not finalize successfully')
 out={'contract':address,'deployTx':tx,'network':'StudioNet','deployer':account.address,'status':'FINALIZED','consensus':receipt.get('result_name'),'execution':'SUCCESS'}
 open(os.path.join(ROOT,'deployment.json'),'w',encoding='utf-8').write(json.dumps(out,indent=2));print(json.dumps(out),flush=True)
if __name__=='__main__':main()

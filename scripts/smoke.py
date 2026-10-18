import json,os,re,time
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet
import genlayer_py.contracts.actions as contract_actions
def compatible_calldata(method=None,args=None,kwargs=None):
 out={}
 if method is not None:out['method']=method
 if args:out['args']=args
 if kwargs:out['kwargs']=kwargs
 return out
contract_actions.make_calldata_object=compatible_calldata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));WORKSPACE=os.path.abspath(os.path.join(ROOT,'..','..','..','..'))
def value(name):
 text=open(os.path.join(WORKSPACE,'accounts.env'),encoding='utf-8').read();return re.search(rf'^\s*{name}\s*=\s*"?([^"\r\n]+)',text,re.M).group(1).strip()
account=create_account(account_private_key=value('ACCOUNT_3_GENLAYER_PRIVATE_KEY'));client=create_client(chain=studionet,account=account);dep=json.load(open(os.path.join(ROOT,'deployment.json')));address=dep['contract'];stamp=str(int(time.time()));offer='OFFCUT-'+stamp;route='ROUTE-'+stamp;base='https://raw.githubusercontent.com/sanshos1/offcut-relay/main/evidence/'
if compatible_calldata('probe',[])!={'method':'probe'}:raise SystemExit('calldata compatibility check failed')
def write(name,args):
 tx=client.write_contract(address=address,function_name=name,args=args);print(name+'Tx',tx,flush=True);receipt=client.wait_for_transaction_receipt(transaction_hash=tx,wait_until='finalized',retries=180,interval=5000,full_transaction=True);leaders=receipt.get('consensus_data',{}).get('leader_receipt')or[];leaders=[leaders] if isinstance(leaders,dict) else leaders
 if receipt.get('result_name')!='MAJORITY_AGREE' or not any(x.get('execution_result')=='SUCCESS' for x in leaders):raise SystemExit(name+' failed')
 return str(tx)
txs={'place':write('place_offcut',[offer,'Birch shelf pair','Birch plywood, 820 by 460 by 18 millimetres, two dry sheets with two factory edges.',2,base+'material-sheet.txt',604800]),'screen':write('test_fit',[route,offer,'Two decorative wall shelves, each 760 by 180 by 18 millimetres, clear-oil finish and maximum load of 8 kilograms.',2,base+'project-brief.txt',base+'workshop-record.txt'])}
screened=client.read_contract(address=address,function_name='get_route',args=[route])
if screened.get('verdict')=='MISMATCH':raise SystemExit('demo fixture unexpectedly mismatched')
txs['reserve']=write('reserve',[route]);txs['handover']=write('hand_over',[route]);stored=client.read_contract(address=address,function_name='get_route',args=[route]);offer_state=client.read_contract(address=address,function_name='get_offer',args=[offer])
if stored.get('state')!='HANDED_OVER' or offer_state.get('state')!='HANDED_OVER':raise SystemExit('canonical readback mismatch')
out={'offerId':offer,'routeId':route,'contractAddress':address,'transactions':txs,'state':stored.get('state'),'verdict':stored.get('verdict'),'conditions':stored.get('conditions'),'routeReadback':stored,'offerReadback':offer_state};os.makedirs(os.path.join(ROOT,'evidence'),exist_ok=True);open(os.path.join(ROOT,'evidence','live-run.json'),'w',encoding='utf-8').write(json.dumps(out,indent=2));print(json.dumps(out),flush=True)

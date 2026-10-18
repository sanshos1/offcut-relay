import ast,pathlib,re
P=pathlib.Path(__file__).parents[1]/'contracts'/'contract.py';S=P.read_text(encoding='utf-8')
def test_contract_parses():ast.parse(S)
def test_surface():
 for name in ('place_offcut','test_fit','reserve','hand_over','expire_offer','get_offer','get_route'):assert f'def {name}' in S
def test_source_attribution_and_frozen_offer():
 assert 'digest!=o.sheet_digest' in S and 'len(set(x.lower() for x in urls))!=3' in S
 assert 'hashlib.sha256' in S and 'prompt_comparative' in S
def test_verdict_backstops():
 assert "verdict=='FIT' and conditions" in S
 assert "verdict=='MISMATCH' and 'NO_SAFE_ROUTE' not in conditions" in S
def test_authorization_and_permissionless_expiry():
 assert 'r.owner!=gl.message.sender_address' in S and 'o.owner!=gl.message.sender_address' in S
 body=re.search(r'def expire_offer\(.*?\n @gl.public.view',S,re.S).group(0)
 assert 'gl.message.sender_address' not in body
def test_contract_initializes_public_surface():assert 'def __init__(self):pass' in S

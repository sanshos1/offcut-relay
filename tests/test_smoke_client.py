import ast,pathlib
S=(pathlib.Path(__file__).parents[1]/'scripts'/'smoke.py').read_text(encoding='utf-8')
def test_smoke_script_parses():ast.parse(S)
def test_studionet_calldata_uses_method_key():
 assert "out['method']=method" in S
 assert "contract_actions.make_calldata_object=compatible_calldata" in S

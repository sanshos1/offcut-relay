"""Resume the documented Offcut Relay lifecycle after a transient RPC failure."""

import json
import os
import re
import time

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
import genlayer_py.contracts.actions as contract_actions


def compatible_calldata(method=None, args=None, kwargs=None):
    output = {}
    if method is not None:
        output["method"] = method
    if args:
        output["args"] = args
    if kwargs:
        output["kwargs"] = kwargs
    return output


contract_actions.make_calldata_object = compatible_calldata
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE = os.path.abspath(os.path.join(ROOT, "..", "..", "..", ".."))
STAMP = "1792344758"
OFFER = "OFFCUT-" + STAMP
ROUTE = "ROUTE-" + STAMP
PLACE_TX = "0x1a7bea631006c43ca42bc7641782bc4b45b3796e9404b2aed4fc4eddc35e8c1c"
SCREEN_TX = "0x9ff4bad621252283dd69de76e1d062d73e0e8b858aa343c962261901091fa709"


def value(name):
    with open(os.path.join(WORKSPACE, "accounts.env"), encoding="utf-8") as handle:
        text = handle.read()
    return re.search(rf'^\s*{name}\s*=\s*"?([^"\r\n]+)', text, re.M).group(1).strip()


def wait_finalized(client, tx_hash):
    for attempt in range(6):
        try:
            return client.wait_for_transaction_receipt(
                transaction_hash=tx_hash,
                wait_until="finalized",
                retries=180,
                interval=5000,
                full_transaction=True,
            )
        except Exception:
            if attempt == 5:
                raise
            time.sleep(5 * (attempt + 1))


account = create_account(account_private_key=value("ACCOUNT_3_GENLAYER_PRIVATE_KEY"))
client = create_client(chain=studionet, account=account)
with open(os.path.join(ROOT, "deployment.json"), encoding="utf-8") as handle:
    address = json.load(handle)["contract"]


def verify(name, tx_hash):
    receipt = wait_finalized(client, tx_hash)
    leaders = receipt.get("consensus_data", {}).get("leader_receipt") or []
    leaders = [leaders] if isinstance(leaders, dict) else leaders
    if receipt.get("result_name") != "MAJORITY_AGREE" or not any(
        item.get("execution_result") == "SUCCESS" for item in leaders
    ):
        raise SystemExit(name + " failed")
    return str(tx_hash)


def write(name, args):
    tx_hash = client.write_contract(address=address, function_name=name, args=args)
    print(name + "Tx", tx_hash, flush=True)
    return verify(name, tx_hash)


transactions = {
    "place": verify("place_offcut", PLACE_TX),
    "screen": verify("test_fit", SCREEN_TX),
}
screened = client.read_contract(address=address, function_name="get_route", args=[ROUTE])
if screened.get("verdict") == "MISMATCH":
    raise SystemExit("demo fixture unexpectedly mismatched")

transactions["reserve"] = write("reserve", [ROUTE])
transactions["handover"] = write("hand_over", [ROUTE])
stored = client.read_contract(address=address, function_name="get_route", args=[ROUTE])
offer_state = client.read_contract(address=address, function_name="get_offer", args=[OFFER])
if stored.get("state") != "HANDED_OVER" or offer_state.get("state") != "HANDED_OVER":
    raise SystemExit("canonical readback mismatch")

output = {
    "offerId": OFFER,
    "routeId": ROUTE,
    "contractAddress": address,
    "transactions": transactions,
    "state": stored.get("state"),
    "verdict": stored.get("verdict"),
    "conditions": stored.get("conditions"),
    "routeReadback": stored,
    "offerReadback": offer_state,
}
os.makedirs(os.path.join(ROOT, "evidence"), exist_ok=True)
with open(os.path.join(ROOT, "evidence", "live-run.json"), "w", encoding="utf-8") as handle:
    json.dump(output, handle, indent=2)
print(json.dumps(output), flush=True)

# OFFCUT RELAY / bench record 01

**Live application:** https://offcut-relay.ranko5180.chatgpt.site

The useful object is already on the bench. The uncertainty is whether it fits the next job.

Offcut Relay lets a donor measure a reusable material remainder once, bind it to a public material sheet, and leave it open for multiple project routes. A recipient brings a project brief and a workshop capability record. GenLayer validators retrieve all three records, confirm that the donor's sheet has not changed, and settle `FIT`, `CONDITIONAL`, or `MISMATCH` with closed preparation conditions and a short handoff sequence.

## Bench rules

- `place_offcut` freezes label, material notes, quantity, source digest, and a bounded open window.
- `test_fit` belongs to the route proposer and never consumes the offer by itself.
- only `FIT` or `CONDITIONAL` may be reserved; a mismatch cannot be waved through.
- the route owner reserves; the donor records handoff; anyone may expire an abandoned open offer after its deadline.
- the record is a coordination pre-screen, not structural engineering or safety certification.

## What a visitor does

The page begins as a cutting mat. The visitor measures the offcut visually, opens a project stencil, and places it over the material. Evidence lives in a tool drawer, not in a wall of URL inputs. A successful screen tears off a pickup ticket carrying the actual verdict, conditions, steps, digests, and StudioNet transaction.

## Bench check

```text
genvm-lint lint contracts/contract.py
python -m pytest -q
node --check site/app.js
```

The three text files in `evidence/` are operator-created fixtures. They demonstrate the lifecycle but are not independent authorities. The reviewed contract is deployed on StudioNet at [`0x62321B4e17E716dE0B63B9FB7775bB2B6A308dd5`](https://explorer-studio.genlayer.com/address/0x62321B4e17E716dE0B63B9FB7775bB2B6A308dd5). The finalized deployment receipt is in `deployment.json`; the live route record is written only after canonical readback. The earlier `0xDFE7…001E` rehearsal deployment is retired and is not used by the interface.

# StudioNet proof ledger

Network: **StudioNet**, chain **61999**. These are public test-network demonstrations, not completed remediation or service-delivery proofs.

Contract: [`0x7CE96B689CC7EcAF7639B22eB9F93A84025D0C78`](https://explorer-studio.genlayer.com/address/0x7CE96B689CC7EcAF7639B22eB9F93A84025D0C78).

`gen_getContractCode` matched the deployed contract against the local source after normalizing line endings and the final newline. Normalized SHA-256: `7536137d99568ef77d83b931a5e3d5776a6bfb1b524f30427f65a72dc520bfc9`.

## Inspected proof matrix

Every listed transaction has an inspected **FINALIZED** receipt. SUCCESS/ERROR refers to **leader execution**, not transaction finality. Consensus result was **MAJORITY_AGREE**, not unanimous agreement. Some validator execution attempts errored; finality alone is not evidence that every validator succeeded.

| Scenario | Execution and observed outcome | Transaction |
| --- | --- | --- |
| Deployment | SUCCESS; deployed source matches | [Deploy](https://explorer-studio.genlayer.com/tx/0xc1fa2367044f90e834b1b4bbda3074d2e8686234b70c6db5c14983f49f7e19a7) |
| Immutable upstream pool | SUCCESS; `python-statistics` binds `python/cpython`, `Lib/statistics.py` | [Create pool](https://explorer-studio.genlayer.com/tx/0xae7a647af63e9e9d9c74bb082bf2c952c41b224120391e1b9a555a50bef74dfc) |
| Independently fetched semantic admission | SUCCESS; actual return/exception changes produce URGENT and QUEUED | [Assess](https://explorer-studio.genlayer.com/tx/0x9a2c555fa48ba1aa05a3c6e30b268160d4adcfb42ed828e88c1bd52a1c53b553) |
| First worker assignment | SUCCESS; LEASED, fence 1, authenticated holder | [Lease](https://explorer-studio.genlayer.com/tx/0x3e7585a6011bbeac66f64edaf9172c6420f21411a33f912acc9cad7ad7a21503) |
| Holder release | SUCCESS; requeued without changing the evidence report | [Release](https://explorer-studio.genlayer.com/tx/0x6ad67abfb19110f6e2ab6941caf10af16b5115d80c0870dab93e323d35106483) |
| Reassignment | SUCCESS; LEASED, fence 2 | [Reassign](https://explorer-studio.genlayer.com/tx/0xce2d19c477828228335e63f6d1428668b61dfa9eac574fca0c52863a7c807db9) |
| Expired assignment acknowledgment | Expected ERROR: `[EXPECTED] invalid, stale or expired lease`; no acknowledgment recorded | [Rejected acknowledgment](https://explorer-studio.genlayer.com/tx/0xff261c2f5dfad3fea5a4a286556818f9af6c25137348352ae058707ecbc1ba22) |
| Expired lease recovery | SUCCESS; unresolved work can be returned to dispatch before its review deadline | [Recover](https://explorer-studio.genlayer.com/tx/0x7aa336159a2ee6add4578e25716029a08d14176a84a9b3f7f34096d5d74a7723) |

The expired acknowledgment also supplied an older fence. Because the live lease was already expired, that row does **not** isolate fence mismatch from deadline enforcement. A separate stale-fence test against a live assignment is required to demonstrate that distinction onchain.

## Acquired evidence

The selected function is CPython `statistics.quantiles`. The contract fetched these real upstream files, not project-owned demonstration summaries:

| Revision | Full response bytes | Independently computed SHA-256 |
| --- | --- | --- |
| `2dc476bcb9142cd25d7e1d52392b73a3dcdf1756` | 50227 | `5845851a5833a1436bfdfd19001f7cd6b4d95a438b76c47162897106d29449c6` |
| `067145177975eadd61a0c907d0d177f7b6a5a3de` | 61831 | `0f618d7c13e99f5289d5e2a20ba8b7340be27ab424f2bffb739ab3be291fe261` |

Both HTTP statuses were 200, and both commitments matched. Acquired implementations differed in single-data-point behavior. Stored impact vector:

```json
{"deprecation_added":false,"effects_change":"UNCHANGED","exception_change":"CHANGED","priority":"URGENT","return_change":"CHANGED","signature_changed":false}
```

Job ID: `d29ba0e9bbbadb2d893c250208ffefd0c4742a779fe84f6a9ca6693a91d8da5c`.

Immutable assessment root: `bfd764d7dc1687440234e339aea421eeeeefc91577ecde2d5fbbd2c544229587`.

Holder: `0x3161CCB0182EB20aF5b38cBDec54a79179525aEA`. ACK denotes receipt of a work item, not completed migration, formal semantic equivalence, or verified service delivery.

## Local validation

- GenVM lint: 3 checks passed; SDK validation passed, 11 methods.
- Direct/unit tests: **20 passed**, including hash mismatch, UNKNOWN, NOOP, cross-pool substitution, wrong holder, old fence, expiration, recovery, duplicate evidence, capacity and priority aging.
- Direct tests mock web/model calls; they are not multi-validator integration tests.
- Production assurance requires independent review; these tests do not promise steward acceptance or points.

Recheck receipts with `node --require ./scripts/rpc_read_retry.cjs scripts/verify_receipts.mjs TX_HASH`. Use `--expect-error` for the explicitly labeled rejected acknowledgment. Recheck source with `node --require ./scripts/rpc_read_retry.cjs scripts/verify_source.mjs 0x7CE96B689CC7EcAF7639B22eB9F93A84025D0C78`.

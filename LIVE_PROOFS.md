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
| Expired lease recovery | SUCCESS; queue can recover unresolved work before its review deadline | [Recover](https://explorer-studio.genlayer.com/tx/0x7aa336159a2ee6add4578e25716029a08d14176a84a9b3f7f34096d5d74a7723) |
| Reassignment after recovery | SUCCESS; LEASED at fence 3 | [Lease again](https://explorer-studio.genlayer.com/tx/0x338288d792945803b91472d83d5878a29ad649c048cb79b2fb6e98d1b8ad298a) |
| Old fence during live assignment | Expected ERROR; fence 2 cannot acknowledge current fence 3 | [Stale fence rejected](https://explorer-studio.genlayer.com/tx/0x5a1f23e2d6ce6d1216eae2869ee722a66c90cfc1cc0474bf992bfacb0f734064) |
| Current holder and fence | SUCCESS; ACKNOWLEDGED at fence 3, unchanged evidence root | [Acknowledge](https://explorer-studio.genlayer.com/tx/0x45f92110351e7b5054a8348010d19c74e76de132345a204ccb9876147f8bf1cf) |
| Independently fetched unchanged function | SUCCESS; NOOP, never queue-admitted | [No-op assessment](https://explorer-studio.genlayer.com/tx/0x4a5392d061a1b5b47145d8d78f80b7dfd26ebe5332caa6be639e30541e56496b) |
| Nonparticipant submission | Expected ERROR: `[EXPECTED] unauthorized pool participant`; no item created | [Unauthorized submission](https://explorer-studio.genlayer.com/tx/0x5eb0aabfa8c0f4f6b10a2567ccc31b891b679ab3cd378d4f78f222d1922a32c8) |
| Incorrect content commitment | SUCCESS records BLOCKED, not a dispatchable item; actual bytes/hash contradict the submitted commitment | [Hash mismatch](https://explorer-studio.genlayer.com/tx/0x7d265567920d30c74a8f4420c1bceb111084707806b8ab23ecac9af115b9630a) |

The first rejected acknowledgment also supplied an older fence, but its assignment had expired. It does **not** isolate fence mismatch from deadline enforcement. The separate live-assignment test does: lease 3 expires at Unix `1790936958`, and the subsequent fence-2 attempt was rejected before the successful fence-3 acknowledgment. No summary, outcome or priority supplied by the caller determined either semantic assessment.

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

Final readbacks:

| Job | State / priority | Evidence root |
| --- | --- | --- |
| `d29ba0e9bbbadb2d893c250208ffefd0c4742a779fe84f6a9ca6693a91d8da5c` | ACKNOWLEDGED / URGENT; fence 3 | `bfd764d7dc1687440234e339aea421eeeeefc91577ecde2d5fbbd2c544229587` |
| `40f058a01f7d9b5ebda8056cac2d9c9e3832d8c462528e476ce6b78aac41e6b3` | NOOP / NOOP | `e0dce79c1b23550229dc586458798690c2ee1fb66440212b9e85bc9d484b13a0` |
| `476b7e4c112ebc7c9293a37aa40b324534cdac24a7f30e36c714f00b57ea4237` | BLOCKED / BLOCKED; old commitment mismatched | `ace8683e46b0512d084a3e4e8ad0afbaaad166366b881a35acf9c37e9a460f20` |

The NOOP compares Python 3.10.14 (`976ea78599d71f22e9c0fefc2dc37c1d9fc835a4`) against 3.12.8. Full file hashes differ, but the acquired `quantiles` implementation hashes are identical: `022cecdca5ff5d580a3be5da9b32cf5dd2ff3d363acb62b428934b6e8ea771c6`. Consensus independently classifies all three semantic change dimensions as UNCHANGED.

The incorrect-commitment attempt was first sent by a different globally active wallet and was rejected as unauthorized. That receipt is labeled as an authority test, not a BLOCKED assessment. The intended wallet then submitted the same negative evidence under a process-local CLI account pin, producing the separately listed BLOCKED report. No shared wallet setting or keystore was modified by the pinning helper.

## Local validation

- GenVM lint: 3 checks passed; SDK validation passed, 11 methods.
- Direct/unit tests: **20 passed**, including hash mismatch, UNKNOWN, NOOP, cross-pool substitution, wrong holder, old fence, expiration, recovery, duplicate evidence, capacity and priority aging.
- Direct tests mock web/model calls; they are not multi-validator integration tests.
- Production assurance requires independent review; these tests do not promise steward acceptance or points.

Recheck receipts with `node --require ./scripts/rpc_read_retry.cjs scripts/verify_receipts.mjs TX_HASH`. Use `--expect-error` for the explicitly labeled rejected acknowledgment. Recheck source with `node --require ./scripts/rpc_read_retry.cjs scripts/verify_source.mjs 0x7CE96B689CC7EcAF7639B22eB9F93A84025D0C78`.

`npm ci --ignore-scripts` followed by `npm run verify:live` rechecks the receipt matrix and all three terminal job states, reconstructing report roots and pool-bound specification hashes. It is read-only and requires no signing key. Expected state and receipt outcomes are machine-readable in [docs/proof-manifest.json](docs/proof-manifest.json).

# Submission

Contribution type: Builder → Intelligent Contracts.

## Title

SourceDeltaQueue — Evidence-Grounded Dispatch and Fenced Worker Leases

## Notes / Description

SourceDeltaQueue is a reusable leased dispatch queue, not a graph or certificate variant. A pool fixes an upstream repository and source path. Participants submit commit-pinned Python revisions and SHA-256 commitments, never priority or change summaries. Leader and validators independently fetch both files, extract the named function and evaluate return, exception and side-effect changes. Exact complete-report equality determines admission: URGENT/NORMAL, NOOP, or fail-closed BLOCKED.

Priority, FIFO and aging schedule work. Pool-bound permissions, one lease per worker, increasing fencing tokens, deadlines and public expiry recovery prevent substitution and stranded assignments. Reports and events are immutable. 14 finalized StudioNet proofs cover CPython admission, release/reassignment, expiry recovery, stale-fence rejection, acknowledgment, NOOP, unauthorized submission and hash mismatch. 20 direct/unit tests and lint pass. ACK means work-item receipt, not completed remediation.

## Evidence

- Repository: https://github.com/ehsandto/source-delta-queue
- Contract: https://github.com/ehsandto/source-delta-queue/blob/main/contracts/SourceDeltaQueue.py
- README: https://github.com/ehsandto/source-delta-queue/blob/main/README.md
- Inspected proof matrix: https://github.com/ehsandto/source-delta-queue/blob/main/LIVE_PROOFS.md
- Deployment: https://explorer-studio.genlayer.com/address/0x7CE96B689CC7EcAF7639B22eB9F93A84025D0C78
- Deployment transaction: https://explorer-studio.genlayer.com/tx/0xc1fa2367044f90e834b1b4bbda3074d2e8686234b70c6db5c14983f49f7e19a7
- Semantic admission: https://explorer-studio.genlayer.com/tx/0x9a2c555fa48ba1aa05a3c6e30b268160d4adcfb42ed828e88c1bd52a1c53b553
- Lease: https://explorer-studio.genlayer.com/tx/0x3e7585a6011bbeac66f64edaf9172c6420f21411a33f912acc9cad7ad7a21503
- Release: https://explorer-studio.genlayer.com/tx/0x6ad67abfb19110f6e2ab6941caf10af16b5115d80c0870dab93e323d35106483
- Reassignment: https://explorer-studio.genlayer.com/tx/0xce2d19c477828228335e63f6d1428668b61dfa9eac574fca0c52863a7c807db9
- Expired acknowledgment rejection (ERROR, not successful acknowledgment): https://explorer-studio.genlayer.com/tx/0xff261c2f5dfad3fea5a4a286556818f9af6c25137348352ae058707ecbc1ba22
- Pool registration: https://explorer-studio.genlayer.com/tx/0xae7a647af63e9e9d9c74bb082bf2c952c41b224120391e1b9a555a50bef74dfc
- Expired lease recovery: https://explorer-studio.genlayer.com/tx/0x7aa336159a2ee6add4578e25716029a08d14176a84a9b3f7f34096d5d74a7723
- Recovered assignment, fence 3: https://explorer-studio.genlayer.com/tx/0x338288d792945803b91472d83d5878a29ad649c048cb79b2fb6e98d1b8ad298a
- Stale fence rejected during a live lease (ERROR): https://explorer-studio.genlayer.com/tx/0x5a1f23e2d6ce6d1216eae2869ee722a66c90cfc1cc0474bf992bfacb0f734064
- Current-fence acknowledgment: https://explorer-studio.genlayer.com/tx/0x45f92110351e7b5054a8348010d19c74e76de132345a204ccb9876147f8bf1cf
- Semantic NOOP: https://explorer-studio.genlayer.com/tx/0x4a5392d061a1b5b47145d8d78f80b7dfd26ebe5332caa6be639e30541e56496b
- Unauthorized submission rejected (ERROR): https://explorer-studio.genlayer.com/tx/0x5eb0aabfa8c0f4f6b10a2567ccc31b891b679ab3cd378d4f78f222d1922a32c8
- Hash-mismatch assessment records BLOCKED: https://explorer-studio.genlayer.com/tx/0x7d265567920d30c74a8f4420c1bceb111084707806b8ab23ecac9af115b9630a

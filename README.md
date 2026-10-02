# SourceDeltaQueue

A reusable GenLayer dispatch queue whose admission and priority come from independently acquired upstream code, not caller-assigned urgency.

## Problem and why GenLayer

A conventional queue faithfully schedules whatever priority its submitter supplies. A source diff shows changed characters, not whether observable return values, exceptions or side effects changed. SourceDeltaQueue makes semantic assessment a consensus-controlled admission boundary, then offers ordinary bounded scheduling and robust worker leases.

```text
Two commit-pinned upstream files + expected full-body hashes
                           |
       leader and validators independently fetch both bodies
                           |
          bounded AST extraction; source is never executed
                           |
      independently derived return / exception / effect vector
                           |
                  exact complete-report comparison
                           |
     URGENT / NORMAL queue admission, or NOOP / BLOCKED
                           |
              priority + FIFO + anti-starvation aging
                           |
       authenticated worker -> expiring fenced lease -> ACK
```

Unlike a graph/proposal contract, there are no mutable nodes, graph heads, evolution versions or graph transition approvals. Unlike SourceTariffVM, it installs no executable program. Unlike a certificate contract, it creates no capability or settlement authorization. Its reusable state is a bounded scheduling pool with worker slots, expiry recovery and monotonically increasing lease fences.

## Evidence and semantic consensus

Each pool pins an upstream GitHub repository and Python source path. A member submits two immutable 40-hex commits, full-response SHA-256 commitments and an exact top-level function name. The contract fetches both complete files inside the nondeterministic flow, checks status, hashes, UTF-8/AST validity and size, then extracts the actual function implementations. No caller summary, outcome, confidence or priority is accepted.

The LLM independently analyzes three dimensions (`return_change`, `exception_change`, `effects_change`) as CHANGED, UNCHANGED or UNKNOWN, plus whether a deprecation was introduced. Signature differences are derived from the acquired AST. Each validator refetches, reconstructs and re-evaluates the evidence. The entire source/report vector and derived priority must match exactly. No confidence tolerance can cross an admission boundary. Exhausted consensus or transport exceptions abort the transaction; they do not fabricate a stored conflict.

- Any UNKNOWN dimension -> BLOCKED, never dispatchable.
- Any return, exception or side-effect change -> URGENT.
- Signature/deprecation-only change -> NORMAL.
- No observed change -> NOOP, never dispatchable.
- Missing function, invalid source, non-200 HTTP or hash mismatch -> BLOCKED.

These are static compatibility-risk assessments, not formal equivalence proofs or claims that a program was executed. Source content is treated as untrusted data; shared model mistakes remain possible. Consumers choose an applicable source revision and trusted publisher.

## Queue lifecycle and security

```text
Evidence assessment -> BLOCKED / NOOP (terminal)
                   -> QUEUED -> LEASED -> ACKNOWLEDGED (terminal)
                          ^       |
                          |       +-> holder releases
                          |       +-> anyone recovers expired lease
                          +-------+
QUEUED or LEASED -> review deadline -> EXPIRED (terminal)
```

Jobs, worker permissions and active lease slots are bound to their pool. Every lookup rejects a mismatched pool ID. One worker holds at most one live assignment per pool. URGENT precedes NORMAL, with FIFO ordering; NORMAL ages into the urgent tier after 600 seconds. Release/recovery renews the item's FIFO position. Every new lease increments its fencing token. Acknowledgment requires the exact current fence, authenticated lease holder and unexpired assignment. Neither a stale worker nor an old token can close a newer lease.

Anyone can recover expired jobs; a deadline takes precedence over requeueing. The owner cannot revoke a worker's live assignment. A dispatch with no candidate returns an empty string, allowing expiry cleanup to commit. Each pool is explicitly capped at **64 historical submissions**, not an unbounded scan. Reports and event history are immutable; repeated source comparisons in the same pool cannot be resampled.

ACK means an assigned work item was received by its lease holder. It does **not** prove completed migration, service delivery or remediation. No funds, escrow, token approvals or external execution adapters exist.

## Real upstream example

The demo compares CPython's `statistics.quantiles` between [Python 3.12.8](https://github.com/python/cpython/blob/2dc476bcb9142cd25d7e1d52392b73a3dcdf1756/Lib/statistics.py) and [Python 3.13.1](https://github.com/python/cpython/blob/067145177975eadd61a0c907d0d177f7b6a5a3de/Lib/statistics.py). The changed handling of a single data point is documented in the [official Python reference](https://docs.python.org/3.13/library/statistics.html#statistics.quantiles). The live contract evaluates the implementations, not this README or a submitted change description.

StudioNet deployment: [`0x7CE96B689CC7EcAF7639B22eB9F93A84025D0C78`](https://explorer-studio.genlayer.com/address/0x7CE96B689CC7EcAF7639B22eB9F93A84025D0C78). [LIVE_PROOFS.md](LIVE_PROOFS.md) identifies inspected finalized receipts and stored-state results. Source verification compares normalized UTF-8 text, including line-ending normalization.

## API

- `create_pool(pool_id, owner, repository, path)` fixes the source domain and enrolls the creator.
- `set_worker(pool_id, address, enabled)` manages membership without revoking live leases.
- `enqueue_change(pool_id, old_commit, new_commit, old_hash, new_hash, function, review_by)` independently assesses evidence and records an item.
- `lease_next(pool_id, lease_seconds)` selects the highest effective priority; duration is 2–3600 seconds, capped by the job deadline.
- `release(pool_id, job_id, fence)` returns the current holder's assignment to the queue.
- `recover(pool_id, job_id)` lets anyone recover expired leases or expire overdue items.
- `acknowledge(pool_id, job_id, fence)` records receipt by the current holder only.
- `get_pool`, `get_job`, `event_count`, `get_event` expose auditable state.

Review deadlines are transaction-time-bound, 30 seconds to seven days from admission. Source files are limited to 96 KiB and extracted top-level functions to 12 KiB. Methods, missing helper behavior and arbitrary runtime dependencies may be unsupported/UNKNOWN; source code is never evaluated or imported.

## Install, validate and deploy

```powershell
python -m pip install -r requirements-dev.txt
npm install -g genlayer@0.39.2
genvm-lint check contracts/SourceDeltaQueue.py
python -m pytest tests/direct tests/unit -q
genlayer network set studionet
genlayer deploy --contract contracts/SourceDeltaQueue.py
genlayer write CONTRACT_ADDRESS create_pool --args python-statistics python cpython Lib/statistics.py
$deadline = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds() + 7200
genlayer write CONTRACT_ADDRESS enqueue_change --args python-statistics 2dc476bcb9142cd25d7e1d52392b73a3dcdf1756 067145177975eadd61a0c907d0d177f7b6a5a3de 5845851a5833a1436bfdfd19001f7cd6b4d95a438b76c47162897106d29449c6 0f618d7c13e99f5289d5e2a20ba8b7340be27ab424f2bffb739ab3be291fe261 quantiles $deadline
genlayer call CONTRACT_ADDRESS get_job --args python-statistics JOB_ID
genlayer write CONTRACT_ADDRESS lease_next --args python-statistics 300
genlayer write CONTRACT_ADDRESS acknowledge --args python-statistics JOB_ID CURRENT_FENCE
genlayer receipt TRANSACTION_HASH
```

StudioNet is gasless. Use an encrypted local keystore; never commit a wallet key, password or GitHub token. The concrete runner is pinned in the contract's first line. Direct tests mock web and model calls, and a documented shim synchronizes the direct runner's cached transaction timestamp. They do not simulate validator agreement. Real StudioNet receipts provide the separate consensus evidence. Inspect both FINALIZED and leader SUCCESS; an expected rejection has ERROR and must be labeled accordingly.

Read-only verifier scripts check receipts and exact deployed source. They retry only reads, never automatically rebroadcast a transaction.

### Reproduce public integration checks

```powershell
npm ci --ignore-scripts
npm run verify:live
node --require ./scripts/rpc_read_retry.cjs scripts/verify_source.mjs 0x7CE96B689CC7EcAF7639B22eB9F93A84025D0C78
```

The read-only integration checker inspects 14 finalized receipts, three terminal jobs and reconstructed evidence/specification roots. It requires no signing key. The live matrix includes explicitly labeled expected execution errors; these are not successful acknowledgments. [SUBMISSION.md](SUBMISSION.md) contains the title, description under 1000 characters and all evidence links.

### Avoid a shared active-wallet race

CLI 0.39.2 `write` has no `--account` option. If other terminals change the global active account, use this process-local compatibility shim after inspecting its short source. It overrides only public account/network selection in memory, not the persisted configuration or keystore. Do not use it for account/config management commands.

```powershell
$env:SOURCE_DELTA_ACCOUNT = 'YOUR_EXISTING_KEYSTORE_NAME'
$cli = Join-Path (npm root -g) 'genlayer/dist/index.js'
node --require ./scripts/pin_cli_context.cjs --require ./scripts/rpc_read_retry.cjs $cli account
# Inspect address and network before signing; the CLI prompts for the keystore password.
node --require ./scripts/pin_cli_context.cjs --require ./scripts/rpc_read_retry.cjs $cli write CONTRACT_ADDRESS lease_next --args POOL_ID 300
```

Validation: 20 direct/unit tests pass, GenVM lint/SDK validation pass, and read-only live verification passes. This is an experimental test-network release, not an independently audited production deployment.

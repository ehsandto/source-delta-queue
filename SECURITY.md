# Security and trust model

- No funds, arbitrary code execution, delegate calls, proxy upgrades or token approvals.
- GitHub source coordinates and paths are bounded and sanitized; commits and body hashes are exact. Raw full-response commitments are checked before semantic analysis.
- Each validator reacquires and independently assesses all consequential evidence. Complete exact comparison includes both the semantic vector and derived scheduling tier. UNKNOWN blocks admission.
- Untrusted code is parsed, never executed. Prompts explicitly separate source data from instructions. Shared semantic errors and prompt injection remain model-layer risks; no formal equivalence claim is made.
- Immutable source-comparison keys include the pool ID, source domain, revisions, commitments, function and policy. They cannot be overwritten or resampled. A different pool is a different authorization namespace, not a migration of the original job.
- Every job lookup enforces its stored pool association. Worker roles and active slots are scoped by authenticated address and pool.
- A lease has an exact holder, deadline and monotonically increasing fence. Release/reassignment and timeout recovery invalidate prior tokens. ACKNOWLEDGED, EXPIRED, BLOCKED and NOOP cannot be reopened.
- The owner can enroll workers, but cannot revoke a live assignment. Anyone can recover expired assignments. These mechanisms provide recovery paths, not a guarantee of transaction inclusion or worker availability.
- Upstream revisions are immutable evidence, not a claim of freshness or a verified deployed runtime. The queue deadline limits scheduling lifetime, not source age.
- Each pool is capped at 64 historical jobs. Membership assumes a trusted admission group; an authorized participant can exhaust that explicit capacity. Create a separately scoped pool when its history is full.
- Transport/consensus failures abort without a false recorded outcome. HTTP failures and missing/invalid evidence can produce a recorded BLOCKED assessment.
- Queue acknowledgment proves receipt by a lease holder, not completed work. Do not connect it to an irreversible payment or external action without a separate delivery-verification design.

Tests cover scope substitution, priority/decision disagreement, unknown evidence, bad commitments, stale fences, wrong principals, expired leases and deadlines. These checks are not an independent professional security audit. Report sensitive defects privately to the repository owner.

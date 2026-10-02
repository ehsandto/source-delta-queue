# Consensus boundary

User action -> two commit-pinned upstream source files -> independent HTTP acquisition and full-body hash checks -> bounded AST extraction (never execution) -> independent semantic comparison -> exact report agreement -> scheduling admission and priority -> worker lease with an expiring fencing token.

External GitHub publishers own the code. A caller identifies revisions and a top-level function, not the compatibility outcome. The contract owns evidence binding, semantic decision, immutable assessment, priority selection, worker identity, lease expiry and stale-ack rejection. Clients own presentation, indexing and actual migration work.

This is a work-dispatch primitive, not an owner-controlled graph, source compiler, settlement ledger or consumable certificate. UNKNOWN or invalid acquisition creates a BLOCKED item that cannot be leased. NOOP does not enter the queue. Return/exception/side-effect changes are URGENT; signature/deprecation-only changes are NORMAL. NORMAL items age into the urgent tier after 600 seconds.

Acknowledgment confirms receipt of an assigned work item only. It does not prove that software was migrated or that a service was delivered. No funds move. Static semantic analysis is not a formal equivalence proof. Models can share a mistake, and consumers select trusted publishers and applicable source revisions.

Each pool is independently keyed and capped at 64 historical submissions. Each worker has at most one live lease per pool. Expired leases can be recovered by anyone; expired jobs become EXPIRED. Release returns an item to the queue and renews its FIFO position. Every new lease increments a fencing token; an old acknowledgment cannot close a newer assignment. A deadline takes precedence over requeueing.

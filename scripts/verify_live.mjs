// Read-only integration check. No signing key, write API or automatic rebroadcast.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';

const manifest = JSON.parse(fs.readFileSync('docs/proof-manifest.json', 'utf8'));
const canonical = value => {
  if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
  if (value && typeof value === 'object') return '{' + Object.keys(value).sort()
    .map(key => JSON.stringify(key) + ':' + canonical(value[key])).join(',') + '}';
  return JSON.stringify(value);
};
const digest = value => crypto.createHash('sha256').update(canonical(value)).digest('hex');
const client = createClient({chain: studionet});
const read = async (functionName, args) => JSON.parse(await client.readContract({
  address: manifest.address, functionName, args,
}));

for (const proof of manifest.transactions) {
  const response = await fetch('https://studio.genlayer.com/api', {
    method: 'POST', headers: {'content-type': 'application/json'},
    body: JSON.stringify({jsonrpc: '2.0', id: 1, method: 'eth_getTransactionByHash', params: [proof.hash]}),
    signal: AbortSignal.timeout(20000),
  });
  assert.ok(response.ok, 'RPC HTTP failure');
  const json = await response.json();
  assert.equal(json.error, undefined);
  assert.equal(json.result?.status, 'FINALIZED', proof.label);
  const leader = json.result.consensus_data?.leader_receipt?.find(item => item.mode === 'leader');
  assert.equal(leader?.execution_result, proof.execution, proof.label);
  console.log(`${proof.label}: FINALIZED/${proof.execution}`);
}

const pool = await read('get_pool', [manifest.pool]);
for (const expected of manifest.jobs) {
  assert.ok(pool.jobs.includes(expected.job_id));
  const job = await read('get_job', [manifest.pool, expected.job_id]);
  assert.equal(job.pool_id, manifest.pool);
  assert.equal(job.state, expected.state);
  assert.equal(job.priority, expected.priority);
  assert.equal(job.report.root, expected.report_root);
  const {root: reportRoot, ...report} = job.report;
  assert.equal(digest(report), reportRoot, 'Report fingerprint must reconstruct');
  assert.equal(digest(job.report.spec), expected.job_id, 'Pool-bound source specification must reconstruct');
  if (expected.fence !== undefined) assert.equal(job.fence, expected.fence);
  if (expected.priority === 'URGENT') {
    assert.equal(job.report.impact.return_change, 'CHANGED');
    assert.equal(job.report.impact.exception_change, 'CHANGED');
    assert.ok(job.report.sources.every(source => source.status === 200 && source.hash_match));
  } else if (expected.priority === 'NOOP') {
    for (const field of ['return_change', 'exception_change', 'effects_change'])
      assert.equal(job.report.impact[field], 'UNCHANGED');
  } else if (expected.priority === 'BLOCKED') {
    assert.equal(job.report.impact, null);
    assert.ok(job.report.sources.some(source => !source.hash_match));
  }
  console.log(`${expected.job_id}: ${job.state}/${job.priority}; roots reconstruct`);
}
console.log('Read-only live proof checks passed. These are stored assessment/dispatch checks, not service-completion proofs.');

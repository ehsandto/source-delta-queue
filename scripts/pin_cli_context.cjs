// Scoped compatibility shim for genlayer CLI 0.39.2 (write lacks --account).
// Overrides public config in memory only. Never modifies shared config or keys.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const account = process.env.SOURCE_DELTA_ACCOUNT;
if (!/^[A-Za-z0-9_-]{1,64}$/.test(account ?? ''))
  throw new Error('Set SOURCE_DELTA_ACCOUNT to the intended existing keystore name');
const configPath = path.resolve(os.homedir(), '.genlayer', 'genlayer-config.json');
const original = fs.readFileSync;
fs.readFileSync = function(file, options) {
  const result = original.apply(this, arguments);
  if (typeof file !== 'string' || path.resolve(file) !== configPath) return result;
  const config = JSON.parse(result.toString());
  const updated = JSON.stringify({...config, activeAccount: account, network: 'studionet'});
  return typeof result === 'string' ? updated : Buffer.from(updated);
};
require('node:module').syncBuiltinESMExports();

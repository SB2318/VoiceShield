const crypto = require('crypto');
const SECRET = process.env.CHAIN_SIGNING_SECRET || 'dev-only-secret-change-me';
const GENESIS_HASH = '0'.repeat(64);
function computeHash(record) {
  const payload = JSON.stringify({
    call_id: record.call_id,
    number: record.number,
    timestamp: record.timestamp,
    decision: record.decision,
    explanation: record.explanation,
    prev_hash: record.prev_hash,
  });
  return crypto.createHash('sha256').update(payload).digest('hex');
}
function signHash(hash) {
  return crypto.createHmac('sha256', SECRET).update(hash).digest('hex');
}
function createRecord({ call_id, number, decision, explanation }, prevHash) {
  if (!call_id || !decision) {
    throw new Error('call_id and decision are required');
  }
  const record = {
    call_id,
    number: number || 'unknown',
    timestamp: new Date().toISOString(),
    decision,
    explanation: explanation || '',
    prev_hash: prevHash || GENESIS_HASH,
  };
  record.hash = computeHash(record);
  record.signature = signHash(record.hash);
  return record;
}
function verifyRecord(record) {
  const expectedHash = computeHash(record);
  const expectedSig = signHash(expectedHash);
  return expectedHash === record.hash && expectedSig === record.signature;
}
function verifyChain(chain) {
  for (let i = 0; i < chain.length; i++) {
    const record = chain[i];

    if (!verifyRecord(record)) {
      return { valid: false, brokenAt: record.call_id, reason: 'hash/signature mismatch — record contents were altered' };
    }

    const expectedPrevHash = i === 0 ? GENESIS_HASH : chain[i - 1].hash;
    if (record.prev_hash !== expectedPrevHash) {
      return { valid: false, brokenAt: record.call_id, reason: 'chain link mismatch — a record was inserted, removed, or reordered' };
    }
  }
  return { valid: true, length: chain.length };
}
module.exports = { createRecord, verifyRecord, verifyChain, GENESIS_HASH };
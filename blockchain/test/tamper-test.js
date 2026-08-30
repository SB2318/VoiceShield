const fs = require('fs');
const path = require('path');
const BASE_URL = process.env.BASE_URL || 'http://localhost:4000';
const DATA_FILE = path.join(__dirname, '..', 'data', 'chain.json');
async function post(url, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json();
}

async function get(url) {
  const res = await fetch(url);
  return res.json();
}
async function run() {
  console.log('--- Step 1: inserting sample decisions ---');
  await post(`${BASE_URL}/log`, {
    call_id: 'call-101',
    number: '+91XXXXXXXX01',
    decision: 'real',
    explanation: 'Passed multi-view ensemble check.',
  });
  await post(`${BASE_URL}/log`, {
    call_id: 'call-102',
    number: '+91XXXXXXXX02',
    decision: 'suspected_clone',
    explanation: 'Unnatural harmonic structure in 2-4kHz band; liveness challenge failed.',
  });
  await post(`${BASE_URL}/log`, {
    call_id: 'call-103',
    number: '+91XXXXXXXX03',
    decision: 'unverified',
    explanation: 'Low confidence, escalated to challenge, user did not respond.',
  });

  console.log('--- Step 2: verifying chain (should be valid) ---');
  console.log(await get(`${BASE_URL}/verify`));

  console.log('--- Step 3: tampering with call-102 directly in storage ---');
  const chain = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  const target = chain.find((r) => r.call_id === 'call-102');
  target.decision = 'real';
  fs.writeFileSync(DATA_FILE, JSON.stringify(chain, null, 2), 'utf8');
  console.log('call-102 decision silently changed from "suspected_clone" to "real".');

  console.log('--- Step 4: verifying chain again (should now report tampering) ---');
  console.log(await get(`${BASE_URL}/verify`));
}

run().catch(console.error);
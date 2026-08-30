const fs = require('fs');
const path = require('path');
const DATA_FILE = path.join(__dirname, '..', 'data', 'chain.json');
function ensureDataFile() {
  const dir = path.dirname(DATA_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  if (!fs.existsSync(DATA_FILE)) fs.writeFileSync(DATA_FILE, '[]', 'utf8');
}
function readChain() {
  ensureDataFile();
  const raw = fs.readFileSync(DATA_FILE, 'utf8');
  return JSON.parse(raw);
}
function appendRecord(record) {
  const chain = readChain();
  chain.push(record);
  fs.writeFileSync(DATA_FILE, JSON.stringify(chain, null, 2), 'utf8');
  return record;
}
// IMPORTANT: there is deliberately no updateRecord() or deleteRecord()
// function in this file. That omission is what makes "append-only"
// actually true, not just a label — don't add one later, even for
// "just fixing a typo."
module.exports = { readChain, appendRecord };
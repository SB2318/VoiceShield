const express = require('express');
const router = express.Router();
const { createRecord, verifyRecord, verifyChain } = require('./chain');
const { readChain, appendRecord } = require('./db');
router.post('/log', (req, res) => {
  try {
    const chain = readChain();
    const prevHash = chain.length ? chain[chain.length - 1].hash : null;
    const record = createRecord(req.body, prevHash);
    appendRecord(record);
    res.status(201).json(record);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});
router.get('/verify', (req, res) => {
  const chain = readChain();
  const result = verifyChain(chain);
  res.json(result);
});
router.get('/log/:call_id', (req, res) => {
  const chain = readChain();
  const record = chain.find((r) => r.call_id === req.params.call_id);
  if (!record) return res.status(404).json({ error: 'not found' });
  res.json({ record, valid: verifyRecord(record) });
});
router.get('/log', (req, res) => {
  res.json(readChain());
});
module.exports = router;
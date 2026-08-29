require('dotenv').config();
const express = require('express');
const auditRoutes = require('./routes');
const app = express();
app.use(express.json());
app.use('/', auditRoutes);
app.get('/health', (req, res) => res.json({ status: 'ok', service: 'blockchain-service' }));
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`blockchain-service running on http://localhost:${PORT}`);
});
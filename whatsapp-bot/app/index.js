require('dotenv').config();
const express = require('express');
const webhookRoutes = require('./webhook');

const app = express();
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

app.use('/', webhookRoutes);

app.get('/health', (req, res) => res.json({ status: 'ok', service: 'whatsapp-bot' }));

const PORT = process.env.PORT || 4001;
app.listen(PORT, () => {
  console.log(`whatsapp-bot running on http://localhost:${PORT}`);
});
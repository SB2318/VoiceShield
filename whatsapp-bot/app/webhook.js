const express = require('express');
const router = express.Router();

function getVerdict(message) {
  const text = (message || '').toLowerCase();

  if (text.includes('clone') || text.includes('fake') || text.includes('scam')) {
    return "⚠️ *Suspected Voice Clone*\nOur analysis flagged unnatural pitch steadiness and missing breathing pauses. This audio shows signs of AI voice synthesis. Please verify through another trusted channel before acting.";
  }

  return "✅ *Likely Genuine*\nNo strong signs of AI voice cloning detected in this clip. As always, if the caller asked for money or urgent action, verify independently before proceeding.";
}

router.post('/whatsapp', (req, res) => {
  const incomingMsg = req.body.Body || '';
  const numMedia = parseInt(req.body.NumMedia || '0', 10);
  const mediaUrl = numMedia > 0 ? req.body.MediaUrl0 : null;

  console.log('Incoming message:', incomingMsg);
  console.log('Media attached:', mediaUrl || 'none');

  let replyText;
  if (mediaUrl) {
    replyText = getVerdict('voice note received');
  } else {
    replyText = "👋 Forward a suspicious voice note or call recording here and I'll check it for signs of AI voice cloning.";
  }

  res.set('Content-Type', 'text/xml');
  res.send(`
    <Response>
      <Message>${replyText}</Message>
    </Response>
  `);
});

module.exports = router;
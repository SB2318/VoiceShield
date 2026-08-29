# VoiceShield — Frontend (SIH26104)

Real-time voice-clone detection UI: live call screening, liveness challenges,
panic-aware response, and an analyst dashboard.

## Views
- **Call Screen** — live confidence score, risk badge, XAI branch breakdown
- **Challenge** — cough/laugh/hum, phrase, and semantic liveness checks
- **Panic Mode** — safe-word setup, guided verification, cooldown timer
- **Dashboard** — analyst live feed, case overrides, EER/latency metrics, codec-collapse chart
- **Demo Shell** — phone-frame mock of the banking-app stage demo
- **Elderly Mode** — large-text, single-action variant

## Run locally
\`\`\`bash
npm install
npm run dev
\`\`\`

## Integration
All views consume a single hook, `src/hooks/useRiskStream.js`, which currently
serves mock data matching the shared decision contract. To connect a real
backend, set `USE_MOCK = false` and point `SOCKET_URL` at the WebSocket endpoint —
no component changes needed.

## Status
Frontend UI complete against the team execution plan. Backend integration pending.

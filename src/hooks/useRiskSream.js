import { useState, useEffect, useRef } from "react";
import { mockDecision } from "../mocks/decisionMock";

const USE_MOCK = true; // flip to false once a real backend URL exists
const SOCKET_URL = "ws://localhost:8000/ws/risk-stream"; // placeholder — Backend 2 gives you the real one

export function useRiskStream() {
  const [decision, setDecision] = useState(mockDecision);
  const wsRef = useRef(null);

  useEffect(() => {
    if (USE_MOCK) {
      // Simulate live updates the same way CallScreen already did
      const interval = setInterval(() => {
        setDecision((prev) => {
          const jitter = (Math.random() - 0.5) * 0.05;
          const newScore = Math.min(1, Math.max(0, prev.fused_score + jitter));
          return { ...prev, fused_score: newScore };
        });
      }, 300);
      return () => clearInterval(interval);
    }

    // Real WebSocket path — activates once USE_MOCK is false
    const ws = new WebSocket(SOCKET_URL);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setDecision(data); // backend must send an object matching the Section 2 contract
      } catch (err) {
        console.error("Failed to parse risk stream message:", err);
      }
    };

    ws.onerror = (err) => console.error("WebSocket error:", err);

    return () => ws.close();
  }, []);

  return decision;
}
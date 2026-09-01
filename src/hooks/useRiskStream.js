import { useState, useEffect, useRef } from "react";
import { mockDecision } from "../fixtures/decisions";

const USE_MOCK = false;
const SOCKET_URL = "ws://localhost:8002/ws/risk-stream"; // was 8000

export function useRiskStream() {
  const [decision, setDecision] = useState(mockDecision);
  const [status, setStatus] = useState(USE_MOCK ? "mock" : "connecting"); // mock | connecting | connected | error
  const wsRef = useRef(null);

  useEffect(() => {
    if (USE_MOCK) {
      const interval = setInterval(() => {
        setDecision((prev) => {
          const jitter = (Math.random() - 0.5) * 0.05;
          const newScore = Math.min(1, Math.max(0, prev.fused_score + jitter));
          return { ...prev, fused_score: newScore };
        });
      }, 300);
      return () => clearInterval(interval);
    }

    const ws = new WebSocket(SOCKET_URL);
    wsRef.current = ws;

    ws.onopen = () => setStatus("connected");

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setDecision(data);
      } catch (err) {
        console.error("Failed to parse risk stream message:", err);
      }
    };

    ws.onerror = () => setStatus("error");
    ws.onclose = () => setStatus("error");

    return () => ws.close();
  }, []);

  return { decision, status };
}
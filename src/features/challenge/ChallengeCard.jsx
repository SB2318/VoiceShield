import { useState } from "react";
import { challengePrompts } from "./challengePrompts";
import { Card } from "../../ui/Card";
import { Label } from "../../ui/Label";
import { Button } from "../../ui/Button";

function ChallengeCard({ challengeType, onResult }) {
  const [result, setResult] = useState("not_triggered");
  const challenge = challengePrompts[challengeType] || challengePrompts.none;
  if (challengeType === "none") return null;

  return (
    <Card className="w-full max-w-xs flex flex-col items-center gap-4 text-center">
      <Label>{challenge.title}</Label>
      <p className="text-ink font-semibold leading-snug">{challenge.prompt}</p>
      {result === "not_triggered" && (
        <div className="flex gap-3 w-full">
          <Button variant="sage" className="flex-1" onClick={() => { setResult("pass"); onResult?.("pass"); }}>Simulate pass</Button>
          <Button variant="primary" className="flex-1" onClick={() => { setResult("fail"); onResult?.("fail"); }}>Simulate fail</Button>
        </div>
      )}
      {result === "pass" && (
        <div className="flex items-center gap-2 text-sage-deep font-semibold text-sm">
          <span className="w-2 h-2 rounded-full bg-sage-deep" />Challenge passed
        </div>
      )}
      {result === "fail" && (
        <div className="flex items-center gap-2 text-terracotta-deep font-semibold text-sm">
          <span className="w-2 h-2 rounded-full bg-terracotta" />Challenge failed
        </div>
      )}
    </Card>
  );
}
export default ChallengeCard;
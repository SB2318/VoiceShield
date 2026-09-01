import PhoneFrame from "./PhoneFrame";
import CallScreen from "../call/CallScreen";
import ConsentBanner from "./ConsentBanner";

function DemoShell() {
  return (
    <PhoneFrame>
      <div className="px-4 py-2">
        <p className="text-center text-ink-faint text-xs mb-2 font-medium">SecureBank — Incoming Call Screening</p>
      </div>
      <ConsentBanner />
      <CallScreen embedded />
    </PhoneFrame>
  );
}
export default DemoShell;
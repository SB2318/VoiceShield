import PhoneFrame from "./PhoneFrame";
import CallScreen from "../CallScreen/CallScreen";
import ConsentBanner from "./ConsentBanner";

function DemoShell() {
  return (
    <PhoneFrame>
      <ConsentBanner />
      <CallScreen embedded />
      <div className="px-4 py-2">
        <p className="text-center text-slate-500 text-xs mb-2">
          SecureBank — Incoming Call Screening
        </p>
      </div>
      <CallScreen embedded />
    </PhoneFrame>
  );
}

export default DemoShell;
import PhoneFrame from "./PhoneFrame";
import CallScreen from "../CallScreen/CallScreen";

function DemoShell() {
  return (
    <PhoneFrame>
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
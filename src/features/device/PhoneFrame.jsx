import { AuroraBackground } from "../../ui/AuroraBackground";

function PhoneFrame({ children }) {
  return (
    <div className="min-h-screen flex items-center justify-center py-10 relative">
      <AuroraBackground />
      <div className="w-[375px] h-[720px] bg-white/40 rounded-[2.5rem] p-3
                      shadow-[0_20px_60px_-15px_rgba(61,64,91,0.35)] border-4 border-white/70 relative z-10">
        <div className="w-full h-full bg-canvas rounded-[2rem] overflow-hidden relative flex flex-col">
          <div className="flex justify-between items-center px-6 py-2 text-ink text-xs font-mono bg-white/40">
            <span>9:41</span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-2 border border-ink-faint rounded-[1px]" />
              <span className="w-3 h-2 border border-ink-faint rounded-[1px]" />
            </span>
          </div>
          <div className="flex-1 overflow-y-auto">{children}</div>
        </div>
      </div>
    </div>
  );
}
export default PhoneFrame;
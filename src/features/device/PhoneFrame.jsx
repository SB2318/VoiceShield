function PhoneFrame({ children }) {
  return (
    <div className="min-h-screen bg-[#0B0F19] flex items-center justify-center py-10">
      <div className="w-[375px] h-[720px] bg-black rounded-[2.5rem] p-3 shadow-2xl shadow-black/60 border-4 border-[#1A2030]">
        <div className="w-full h-full bg-[#0B0F19] rounded-[2rem] overflow-hidden relative flex flex-col">
          {/* Fake status bar */}
          <div className="flex justify-between items-center px-6 py-2 text-[#E8ECF4] text-xs font-mono bg-black/40">
            <span>9:41</span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-2 border border-[#8993A8] rounded-[1px]" />
              <span className="w-3 h-2 border border-[#8993A8] rounded-[1px]" />
            </span>
          </div>
          <div className="flex-1 overflow-y-auto">{children}</div>
        </div>
      </div>
    </div>
  );
}
export default PhoneFrame;

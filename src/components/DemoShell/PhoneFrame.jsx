function PhoneFrame({ children }) {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center py-10">
      <div className="w-[375px] h-[720px] bg-black rounded-[2.5rem] p-3 shadow-2xl border-4 border-slate-800">
        <div className="w-full h-full bg-slate-900 rounded-[2rem] overflow-hidden relative flex flex-col">
          {/* Fake status bar */}
          <div className="flex justify-between items-center px-6 py-2 text-white text-xs bg-black/40">
            <span>9:41</span>
            <span>📶 🔋</span>
          </div>
          <div className="flex-1 overflow-y-auto">{children}</div>
        </div>
      </div>
    </div>
  );
}

export default PhoneFrame;
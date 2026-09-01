export function AuroraBackground() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
      <div className="absolute -top-32 -left-24 w-[36rem] h-[36rem] rounded-full
                      bg-terracotta/35 blur-[110px] animate-aurora-a" />
      <div className="absolute top-1/3 -right-32 w-[32rem] h-[32rem] rounded-full
                      bg-sage/40 blur-[110px] animate-aurora-b" />
      <div className="absolute -bottom-40 left-1/4 w-[38rem] h-[38rem] rounded-full
                      bg-gold/35 blur-[120px] animate-aurora-c" />
      <div className="absolute inset-0 grain" />
    </div>
  );
}
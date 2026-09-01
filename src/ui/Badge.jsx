const TONES = {
  verified: "bg-sage/16      text-sage-deep       border-sage/40",
  caution:  "bg-gold/22      text-gold-deep       border-gold/45",
  alert:    "bg-terracotta/14 text-terracotta-deep border-terracotta/35",
  severe:   "bg-rose/16      text-rose            border-rose/40",
  neutral:  "bg-raised       text-ink-soft        border-hairline",
};

export function Badge({ tone = "neutral", children }) {
  return (
    <span className={`inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border
                       text-[11px] font-bold uppercase tracking-[0.1em] ${TONES[tone]}`}>
      <span className="w-1.5 h-1.5 rounded-full bg-current" />
      {children}
    </span>
  );
}
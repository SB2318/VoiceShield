export function Stat({ label, value, unit, hint }) {
  return (
    <div className="glass rounded-[20px] p-6 shadow-[0_6px_28px_-10px_rgba(61,64,91,0.18)]">
      <p className="label">{label}</p>
      <p className="mt-2 font-display font-semibold text-3xl text-ink tabular-nums">
        {value}{unit && <span className="text-ink-faint text-lg ml-1 font-sans font-normal">{unit}</span>}
      </p>
      {hint && <p className="mt-1.5 text-xs text-ink-faint">{hint}</p>}
    </div>
  );
}
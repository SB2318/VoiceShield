export function Button({ children, variant = "primary", className = "", ...props }) {
  const base = "px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300";
  const variants = {
    primary: "bg-gradient-to-r from-terracotta to-terracotta-deep text-white glow-terracotta",
    sage:    "bg-gradient-to-r from-sage to-sage-deep text-white glow-sage",
    outline: "bg-white/70 border border-hairline text-ink hover:border-terracotta/40 glow-terracotta",
    ghost:   "text-ink-soft hover:text-terracotta",
  };
  return (
    <button className={`${base} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}
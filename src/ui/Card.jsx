export function Card({ children, className = "", padded = true, glow = false, hover = false }) {
  return (
    <div className={`glass rounded-[20px] shadow-[0_6px_28px_-10px_rgba(61,64,91,0.18)]
                     ${glow ? "glow-terracotta" : ""} ${hover ? "card-hover" : ""}
                     ${padded ? "p-6" : ""} ${className}`}>
      {children}
    </div>
  );
}
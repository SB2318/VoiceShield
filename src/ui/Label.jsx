export function Label({ children, className = "" }) {
  return <p className={`label ${className}`}>{children}</p>;
}
export default function StatCard({ value, label, variant }) {
  return (
    <article className={`stat-card stat-card--${variant}`}>
      <strong>{value}</strong>
      <span>{label}</span>
    </article>
  );
}
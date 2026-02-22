export default function DBDAModuleLayout({ title, children }) {
  return (
    <div className="dbda-page">
      <h1 className="dbda-title">📘 {title}</h1>
      {children}
    </div>
  );
}
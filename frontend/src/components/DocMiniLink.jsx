export default function DocMiniLink({ to }) {
  return (
    <a
      href={to}
      style={{
        fontSize: "13px",
        color: "#333",
        borderBottom: "1px dotted #333",
        cursor: "pointer",
        textDecoration: "none",
      }}
    >
      documentation
    </a>
  );
}

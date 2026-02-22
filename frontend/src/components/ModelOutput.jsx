export default function ModelOutput({ title, output }) {
  return (
    <div
      style={{
        border: "1px solid rgba(0,0,0,0.15)",
        borderRadius: "14px",
        padding: "20px",
        background: "#fff",
        marginTop: "30px",
        minHeight: "160px",
      }}
    >
      <h3 style={{ opacity: 0.7, marginBottom: "10px" }}>{title}</h3>

      {!output && (
        <p style={{ opacity: 0.5, marginTop: "20px" }}>
          Model output will appear here...
        </p>
      )}

      {output && (
        <pre
          style={{
            marginTop: "10px",
            fontSize: "16px",
            fontWeight: 500,
            whiteSpace: "pre-wrap",   // ⭐ preserves line-breaks
            lineHeight: "22px",
          }}
        >
          {output}
        </pre>
      )}
    </div>
  );
}

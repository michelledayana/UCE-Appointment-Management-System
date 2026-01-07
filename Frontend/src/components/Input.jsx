export default function Input({ label, ...props }) {
  return (
    <div style={{ marginBottom: "12px" }}>
      <label>{label}</label><br />
      <input
        {...props}
        style={{ padding: "8px", width: "100%" }}
      />
    </div>
  );
}

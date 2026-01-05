import { useState } from "react";
import Input from "../components/Input";
import { registerUser } from "../api/userApi";

export default function Register() {
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: ""
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const res = await registerUser(form);
      setResult(res);
    } catch (err) {
      setError(err.response?.data?.detail || "Error");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto" }}>
      <h2>User Registration</h2>

      <form onSubmit={handleSubmit}>
        <Input
          label="Full Name"
          name="full_name"
          onChange={handleChange}
        />
        <Input
          label="Email"
          name="email"
          type="email"
          onChange={handleChange}
        />
        <Input
          label="Password"
          name="password"
          type="password"
          onChange={handleChange}
        />

        <button type="submit">Register</button>
      </form>

      {result && (
        <p style={{ color: "green" }}>
          ✔ Registered as {result.user_type}
        </p>
      )}

      {error && (
        <p style={{ color: "red" }}>
          ✖ {error}
        </p>
      )}
    </div>
  );
}

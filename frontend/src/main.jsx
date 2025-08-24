// src/main.jsx
import "./index.css";   // ← Tailwind v4 (OBLIGATORIO)
import "./App.css";     // ← tu reset

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App"; // importa App.tsx

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

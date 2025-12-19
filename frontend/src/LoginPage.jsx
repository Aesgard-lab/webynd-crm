// src/LoginPage.jsx
import * as React from "react";
import { useState } from "react";
import {
  Button,
  Card,
  CardContent,
  TextField,
  Typography,
  CircularProgress,
} from "@mui/material";
import LockIcon from "@mui/icons-material/Lock";
import { useLogin, useNotify } from "react-admin";

const LoginPage = () => {
  const login = useLogin();
  const notify = useNotify();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);

    try {
      await login({ email, password });
    } catch (error) {
      console.error(error);
      notify("Email o contraseña incorrectos", { type: "warning" });
      setSubmitting(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background:
          "radial-gradient(circle at center, #202b5c 0, #050827 55%, #03051a 100%)",
      }}
    >
      <Card
        elevation={8}
        sx={{
          width: 380,
          borderRadius: 4,
        }}
      >
        <CardContent
          sx={{
            padding: 4,
            display: "flex",
            flexDirection: "column",
            gap: 2.5,
            alignItems: "stretch",
          }}
        >
          <div
            style={{
              width: 60,
              height: 60,
              borderRadius: "50%",
              margin: "0 auto 8px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              background: "#f5f5f5",
            }}
          >
            <LockIcon fontSize="large" />
          </div>

          <Typography
            variant="h6"
            align="center"
            sx={{ fontWeight: 600, mb: 1 }}
          >
            Inicia sesión en tu gimnasio
          </Typography>

          <form
            onSubmit={handleSubmit}
            style={{ display: "flex", flexDirection: "column", gap: 16 }}
          >
            <TextField
              label="Email"
              type="email"
              name="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              fullWidth
              required
              size="medium"
            />

            <TextField
              label="Password"
              type="password"
              name="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              fullWidth
              required
              size="medium"
            />

            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={submitting}
              sx={{
                mt: 1,
                borderRadius: 999,
                textTransform: "none",
                fontWeight: 600,
                py: 1.2,
              }}
            >
              {submitting ? (
                <CircularProgress size={22} sx={{ color: "white" }} />
              ) : (
                "Sign in"
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default LoginPage;

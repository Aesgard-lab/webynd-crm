import * as React from "react";
import {
  Avatar,
  Divider,
  IconButton,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
  Tooltip,
} from "@mui/material";
import LogoutIcon from "@mui/icons-material/Logout";
import StoreIcon from "@mui/icons-material/Store";
import SwapHorizIcon from "@mui/icons-material/SwapHoriz";
import { useLogout } from "react-admin";

function readMe() {
  try {
    return JSON.parse(localStorage.getItem("me") || "null");
  } catch {
    return null;
  }
}

function writeMe(next: any) {
  try {
    localStorage.setItem("me", JSON.stringify(next));
    localStorage.setItem("currentGymId", next?.currentGym?.id ?? "");
    // notifica a la UI (Menu/Layout) que cambió la sede
    window.dispatchEvent(new Event("gym-changed"));
  } catch {}
}

export default function UserChip() {
  const logout = useLogout();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [me, setMe] = React.useState<any>(() => readMe());

  React.useEffect(() => {
    const onStorage = (e: StorageEvent) => {
      if (e.key === "me") setMe(readMe());
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  const open = Boolean(anchorEl);
  const memberships: Array<any> = me?.memberships ?? [];
  const currentGymId = me?.currentGym?.id ?? null;

  const selectGym = (gym: any) => {
    const next = { ...me, currentGym: gym };
    setMe(next);
    writeMe(next);
    setAnchorEl(null);
  };

  return (
    <>
      <Tooltip title={me?.fullName || me?.email || "Cuenta"}>
        <IconButton size="small" onClick={(e) => setAnchorEl(e.currentTarget)}>
          <Avatar
            src={me?.avatar || undefined}
            alt={me?.fullName || "user"}
            sx={{ width: 32, height: 32 }}
          />
        </IconButton>
      </Tooltip>

      <Menu anchorEl={anchorEl} open={open} onClose={() => setAnchorEl(null)}>
        <div style={{ padding: "8px 16px", maxWidth: 280 }}>
          <div style={{ fontWeight: 600 }}>{me?.fullName || me?.email}</div>
          {me?.role && (
            <div style={{ fontSize: 12, color: "#666" }}>
              {String(me.role).toUpperCase()}
            </div>
          )}
        </div>
        <Divider />
        <MenuItem disabled>
          <ListItemIcon>
            <StoreIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText primary="Cambiar sede" />
        </MenuItem>
        {memberships.map((m: any) => (
          <MenuItem
            key={m?.gym?.id}
            selected={currentGymId === m?.gym?.id}
            onClick={() => selectGym(m?.gym)}
          >
            <ListItemIcon>
              <SwapHorizIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText primary={m?.gym?.name} secondary={m?.role ?? ""} />
          </MenuItem>
        ))}
        <Divider />
        <MenuItem onClick={() => logout()}>
          <ListItemIcon>
            <LogoutIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText primary="Cerrar sesión" />
        </MenuItem>
      </Menu>
    </>
  );
}
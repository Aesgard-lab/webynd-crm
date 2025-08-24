// hooks/useMe.js
import { useEffect, useState } from "react";

export function useMe() {
  const [me, setMe] = useState(null);

  useEffect(() => {
    fetch("/api/auth/me/", {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    })
      .then((res) => res.json())
      .then(setMe)
      .catch(() => setMe(null));
  }, []);

  return me;
}

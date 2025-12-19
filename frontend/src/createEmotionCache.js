// src/createEmotionCache.js
import createCache from "@emotion/cache";

export default function createEmotionCache() {
  // Busca el meta del insertion point (lo añadimos en index.html)
  const insertionPoint =
    typeof document !== "undefined"
      ? document.querySelector('meta[name="emotion-insertion-point"]')
      : null;

  return createCache({
    key: "mui",
    insertionPoint: insertionPoint || undefined,
    prepend: true,
  });
}

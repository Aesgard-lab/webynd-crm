// src/hooks/useGymBrand.ts
import * as React from "react";
import { useDataProvider } from "react-admin";
import { useCurrentGym } from "./useGym";

type Brand = {
  primary_color: string;
  logo: string | null;
  gymName: string;
  loading: boolean;
  error?: any;
};

const DEFAULT_BRAND: Brand = {
  primary_color: "#3d99f5",
  logo: null,
  gymName: "Mi Gimnasio",
  loading: false,
};

export function useGymBrand(): Brand {
  const dp = useDataProvider();
  const { gymId } = useCurrentGym();
  const [brand, setBrand] = React.useState<Brand>(DEFAULT_BRAND);
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    if (!gymId) {
      setBrand(DEFAULT_BRAND);
      return;
    }
    let mounted = true;
    setLoading(true);

    dp.getOne("gyms", { id: gymId })
      .then(({ data }) => {
        if (!mounted) return;
        setBrand({
          primary_color: data?.primary_color || DEFAULT_BRAND.primary_color,
          logo: data?.logo || data?.logo_url || DEFAULT_BRAND.logo,
          gymName: data?.name || DEFAULT_BRAND.gymName,
          loading: false,
        });
      })
      .catch((error) => {
        if (!mounted) return;
        setBrand({ ...DEFAULT_BRAND, loading: false, error });
      })
      .finally(() => mounted && setLoading(false));

    return () => {
      mounted = false;
    };
  }, [dp, gymId]);

  return { ...brand, loading };
}

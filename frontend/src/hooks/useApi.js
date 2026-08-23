import { useState, useCallback } from "react";

/**
 * Generic hook for calling an async API function with consistent
 * loading / error / data state handling.
 */
export function useApi(apiFn) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const run = useCallback(
    async (...args) => {
      setLoading(true);
      setError(null);
      try {
        const result = await apiFn(...args);
        setData(result);
        return result;
      } catch (err) {
        setError(err?.message || "Something went wrong.");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [apiFn]
  );

  return { data, loading, error, run, setData };
}

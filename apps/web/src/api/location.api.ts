import { apiFetch } from "./client";

export function resolveLocation(payload: unknown) {
  return apiFetch("/api/v1/locations/resolve", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}


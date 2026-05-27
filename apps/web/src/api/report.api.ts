import { apiFetch } from "./client";

export function createReport(payload: unknown) {
  return apiFetch("/api/v1/reports", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}


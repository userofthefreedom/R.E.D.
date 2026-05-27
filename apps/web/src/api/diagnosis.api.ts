import { apiFetch } from "./client";

export function createDiagnosisRun(payload: unknown) {
  return apiFetch("/api/v1/diagnosis/runs", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}


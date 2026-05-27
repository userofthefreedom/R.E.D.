import { apiFetch } from "./client";

export function createDiagnosisRun(payload: unknown) {
  return apiFetch("/api/v1/diagnosis/runs", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getDiagnosisResult(runId: string) {
  return apiFetch(`/api/v1/diagnosis/runs/${runId}/result`);
}

export function getDiagnosisEvidence(runId: string) {
  return apiFetch(`/api/v1/diagnosis/runs/${runId}/evidence`);
}

export function getDiagnosisTrace(runId: string) {
  return apiFetch(`/api/v1/diagnosis/runs/${runId}/trace`);
}

export function getAlternativeScenarios(runId: string) {
  return apiFetch(`/api/v1/diagnosis/runs/${runId}/alternatives`);
}


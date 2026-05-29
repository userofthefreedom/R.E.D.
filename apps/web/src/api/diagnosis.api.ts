import { apiFetch } from "./client";

export interface DiagnosisRunCreatePayload {
  project_id: string;
  action_id?: string | null;
  rule_set_version?: string | null;
  rag_index_version?: string | null;
  data_base_date?: string | null;
  law_base_date?: string | null;
}

export interface ApiDiagnosisRun {
  id: string;
  project_id: string;
  action_id?: string | null;
  status: string;
  rule_set_version?: string | null;
  rag_index_version?: string | null;
  data_base_date?: string | null;
  law_base_date?: string | null;
  started_at?: string | null;
  completed_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface DiagnosisProcedureResult {
  name: string;
  target: string;
  reason: string;
  department: string;
  risk: string;
}

export interface DiagnosisRuleTrace {
  rule_id: string;
  rule_name: string;
  input_fields: string[];
  result: string;
  reason: string;
}

export interface DiagnosisResultResponse {
  run_id: string;
  summary: {
    overall: string;
    main_permit_type: string;
    risk_level: string;
    missing_info_count: number;
    required_actions: string[];
  };
  procedures: DiagnosisProcedureResult[];
  rule_traces: DiagnosisRuleTrace[];
  input_snapshot: Record<string, unknown>;
}

export function createDiagnosisRun(payload: DiagnosisRunCreatePayload) {
  return apiFetch<ApiDiagnosisRun>("/api/v1/diagnosis/runs", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getDiagnosisResult(runId: string) {
  return apiFetch<DiagnosisResultResponse>(`/api/v1/diagnosis/runs/${runId}/result`);
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


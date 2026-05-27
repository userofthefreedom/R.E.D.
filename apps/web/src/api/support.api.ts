import { apiFetch } from "./client";

export function listFailureReasons() {
  return apiFetch("/api/v1/support/failure-reasons");
}

export function listPreConsultationGuides() {
  return apiFetch("/api/v1/support/pre-consultation-guides");
}

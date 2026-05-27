import { apiFetch } from "./client";

export function listProjects() {
  return apiFetch("/api/v1/projects");
}

export function getProject(projectId: string) {
  return apiFetch(`/api/v1/projects/${projectId}`);
}

export function listProjectReports(projectId: string) {
  return apiFetch(`/api/v1/projects/${projectId}/reports`);
}

export function listProjectHistory(projectId: string) {
  return apiFetch(`/api/v1/projects/${projectId}/history`);
}

export function compareProjectSnapshots(projectId: string) {
  return apiFetch(`/api/v1/projects/${projectId}/snapshots/compare`);
}


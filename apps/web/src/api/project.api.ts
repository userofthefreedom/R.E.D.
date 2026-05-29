import { apiFetch } from "./client";
import type { ApiProject } from "../types/project";

export interface ProjectCreatePayload {
  name: string;
  address?: string | null;
  pnu?: string | null;
  description?: string | null;
}

export interface ParcelCreatePayload {
  pnu: string;
  standard_address?: string | null;
  jibun_address?: string | null;
  legal_dong_code?: string | null;
  land_category?: string | null;
  site_area?: number | null;
  use_district?: string | null;
  district_unit_plan?: boolean;
  geometry_geojson?: Record<string, unknown> | null;
  data_base_date?: string | null;
}

export interface ActionCreatePayload {
  action_type: string;
  current_use?: string | null;
  desired_use?: string | null;
  site_area?: number | null;
  building_area?: number | null;
  total_floor_area?: number | null;
  floor_count_above?: number | null;
  floor_count_under?: number | null;
  parking_before?: number | null;
  parking_after?: number | null;
  site_conditions?: Record<string, unknown> | null;
  construction_method?: string | null;
  business_purpose?: string | null;
  memo?: string | null;
  normalized_json?: Record<string, unknown>;
}

export interface RegulationOverlayCreatePayload {
  parcel_id?: string | null;
  layer_code?: string | null;
  layer_name: string;
  regulation_type?: string | null;
  jurisdiction?: string | null;
  overlap_area?: number | null;
  overlap_ratio?: number | null;
  source_name?: string | null;
  source_url?: string | null;
  data_base_date?: string | null;
  raw_payload?: Record<string, unknown> | null;
}

export function createProject(payload: ProjectCreatePayload) {
  return apiFetch<ApiProject>("/api/v1/projects", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function listProjects() {
  return apiFetch<ApiProject[]>("/api/v1/projects");
}

export function getProject(projectId: string) {
  return apiFetch<ApiProject>(`/api/v1/projects/${projectId}`);
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

export function createProjectParcel(projectId: string, payload: ParcelCreatePayload) {
  return apiFetch<{ id: string }>(`/api/v1/projects/${projectId}/parcels`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function createProjectAction(projectId: string, payload: ActionCreatePayload) {
  return apiFetch<{ id: string }>(`/api/v1/projects/${projectId}/actions`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function createProjectRegulationOverlay(projectId: string, payload: RegulationOverlayCreatePayload) {
  return apiFetch<{ id: string }>(`/api/v1/projects/${projectId}/regulation-overlays`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}


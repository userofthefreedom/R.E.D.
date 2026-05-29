import { apiFetch } from "./client";

export interface LocationCandidate {
  pnu: string;
  standard_address: string;
  jibun_address: string;
  legal_dong_code: string;
  land_category: string;
  site_area: number;
  use_district: string;
  district_unit_plan: boolean;
  match_score: number;
  data_base_date: string;
  public_data_status: string;
  centroid_lon?: number | null;
  centroid_lat?: number | null;
  geometry_geojson?: Record<string, unknown> | null;
  source_name?: string | null;
}

export interface LocationResolveResponse {
  query: string;
  mode: string;
  status: string;
  provider: string;
  candidates: LocationCandidate[];
}

export function resolveLocation(payload: { query: string; mode?: string; lon?: number; lat?: number }) {
  return apiFetch<LocationResolveResponse>("/api/v1/locations/resolve", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

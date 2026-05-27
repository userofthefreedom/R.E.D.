import { apiFetch } from "./client";

export function listProjects() {
  return apiFetch("/api/v1/projects");
}


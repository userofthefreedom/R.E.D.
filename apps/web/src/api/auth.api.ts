import { apiFetch } from "./client";

export function getCurrentUser() {
  return apiFetch("/api/v1/auth/me");
}

export function listNotifications() {
  return apiFetch("/api/v1/auth/notifications");
}

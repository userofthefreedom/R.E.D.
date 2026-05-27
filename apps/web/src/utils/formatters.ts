export function formatDateTime(value: string | Date): string {
  return new Date(value).toLocaleString("ko-KR");
}


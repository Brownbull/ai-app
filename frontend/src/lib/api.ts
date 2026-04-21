const API_BASE = import.meta.env.VITE_API_URL || "";

export interface Incident {
  id: string;
  title: string;
  description: string;
  reporter_email: string;
  status: string;
  severity: string;
  triage_result: Record<string, unknown> | null;
  confidence: number | null;
  cost_usd: number | null;
  created_at: string;
  updated_at: string;
}

export async function fetchIncidents(): Promise<Incident[]> {
  const res = await fetch(`${API_BASE}/api/incidents`);
  if (!res.ok) throw new Error(`Failed to fetch incidents: ${res.statusText}`);
  return res.json();
}

export async function fetchIncident(id: string): Promise<Incident> {
  const res = await fetch(`${API_BASE}/api/incidents/${id}`);
  if (!res.ok) throw new Error(`Incident not found: ${res.statusText}`);
  return res.json();
}

export async function checkHealth(): Promise<{ status: string }> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error("Backend unreachable");
  return res.json();
}

export interface IncidentSubmitResponse {
  incident_id: string;
  status: string;
}

// FastAPI's HTTPException serializes as { detail: string } (or object).
// Backend `detail` strings prefix the category (e.g. "Input blocked by
// guardrails: ...", "File exceeds 10MB limit", "Invalid reporter_email
// format") so the UI can branch on the string form without needing extra
// structured fields today. When backend adds structured error responses,
// widen this type to a discriminated union.
export interface ApiErrorBody {
  detail: string;
}

export class ApiError extends Error {
  readonly status: number;
  readonly detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

export async function submitIncident(
  data: FormData
): Promise<IncidentSubmitResponse> {
  const res = await fetch(`${API_BASE}/api/incidents`, {
    method: "POST",
    body: data,
    // No Content-Type header — browser sets multipart boundary automatically
  });
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = (await res.json()) as Partial<ApiErrorBody>;
      if (typeof body.detail === "string") detail = body.detail;
    } catch {
      // Body wasn't JSON — keep the fallback message
    }
    throw new ApiError(res.status, detail);
  }
  return res.json();
}

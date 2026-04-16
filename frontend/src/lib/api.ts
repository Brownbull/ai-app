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

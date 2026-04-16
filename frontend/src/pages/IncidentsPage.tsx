import { useEffect, useState } from "react";
import { type Incident, fetchIncidents } from "@/lib/api";

export function IncidentsPage() {
  const [incidents, setIncidents] = useState<Incident[]>([]);

  useEffect(() => {
    fetchIncidents()
      .then(setIncidents)
      .catch(() => setIncidents([]));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold tracking-tight">Incidents</h2>
        <p className="text-muted-foreground text-sm mt-1">
          All submitted incidents
        </p>
      </div>

      <div className="bg-card border border-border rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border text-left text-muted-foreground">
              <th className="px-4 py-3 font-medium">ID</th>
              <th className="px-4 py-3 font-medium">Title</th>
              <th className="px-4 py-3 font-medium">Severity</th>
              <th className="px-4 py-3 font-medium">Status</th>
              <th className="px-4 py-3 font-medium">Created</th>
            </tr>
          </thead>
          <tbody>
            {incidents.map((incident) => (
              <tr
                key={incident.id}
                className="border-b border-border/50 hover:bg-muted/20 transition-colors"
              >
                <td className="px-4 py-3 font-mono text-xs text-muted-foreground">
                  {incident.id}
                </td>
                <td className="px-4 py-3">{incident.title}</td>
                <td className="px-4 py-3">
                  <SeverityBadge severity={incident.severity} />
                </td>
                <td className="px-4 py-3">
                  <StatusBadge status={incident.status} />
                </td>
                <td className="px-4 py-3 text-muted-foreground text-xs">
                  {new Date(incident.created_at).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {incidents.length === 0 && (
          <p className="text-sm text-muted-foreground py-8 text-center">
            No incidents found
          </p>
        )}
      </div>
    </div>
  );
}

function SeverityBadge({ severity }: { severity: string }) {
  const styles: Record<string, string> = {
    P0: "bg-[var(--severity-p0)]/20 text-[var(--severity-p0)]",
    P1: "bg-[var(--severity-p1)]/20 text-[var(--severity-p1)]",
    P2: "bg-[var(--severity-p2)]/20 text-[var(--severity-p2)]",
    P3: "bg-[var(--severity-p3)]/20 text-[var(--severity-p3)]",
    P4: "bg-[var(--severity-p4)]/20 text-[var(--severity-p4)]",
  };
  return (
    <span
      className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${styles[severity] ?? "bg-muted text-muted-foreground"}`}
    >
      {severity}
    </span>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    triaged: "text-[var(--severity-p4)]",
    blocked: "text-destructive",
    submitted: "text-muted-foreground",
    triaging: "text-[var(--severity-p2)]",
  };
  return (
    <span className={`text-xs font-medium ${styles[status] ?? "text-muted-foreground"}`}>
      {status}
    </span>
  );
}

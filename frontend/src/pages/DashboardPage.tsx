import { useEffect, useState } from "react";
import { type Incident, fetchIncidents, checkHealth } from "@/lib/api";

export function DashboardPage() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [healthy, setHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    fetchIncidents()
      .then(setIncidents)
      .catch(() => setIncidents([]));

    checkHealth()
      .then(() => setHealthy(true))
      .catch(() => setHealthy(false));
  }, []);

  const counts = {
    total: incidents.length,
    triaged: incidents.filter((i) => i.status === "triaged").length,
    blocked: incidents.filter((i) => i.status === "blocked").length,
    processing: incidents.filter(
      (i) => i.status === "submitted" || i.status === "triaging"
    ).length,
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground text-sm mt-1">
          SRE triage pipeline overview
        </p>
      </div>

      {/* Status cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          label="Backend"
          value={healthy === null ? "..." : healthy ? "Healthy" : "Down"}
          color={healthy ? "text-[var(--severity-p4)]" : "text-destructive"}
        />
        <StatCard label="Total" value={counts.total} />
        <StatCard
          label="Triaged"
          value={counts.triaged}
          color="text-[var(--severity-p4)]"
        />
        <StatCard
          label="Blocked"
          value={counts.blocked}
          color="text-destructive"
        />
      </div>

      {/* Recent incidents */}
      <div className="bg-card border border-border rounded-lg p-4">
        <h3 className="text-sm font-medium text-muted-foreground mb-3">
          Recent Incidents
        </h3>
        {incidents.length === 0 ? (
          <p className="text-sm text-muted-foreground py-4 text-center">
            No incidents yet. Submit one to get started.
          </p>
        ) : (
          <div className="space-y-2">
            {incidents.slice(0, 10).map((incident) => (
              <div
                key={incident.id}
                className="flex items-center justify-between px-3 py-2 rounded-md bg-muted/30"
              >
                <div className="flex items-center gap-3">
                  <SeverityDot severity={incident.severity} />
                  <span className="text-sm">{incident.title}</span>
                </div>
                <span className="text-xs text-muted-foreground">
                  {incident.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({
  label,
  value,
  color,
}: {
  label: string;
  value: string | number;
  color?: string;
}) {
  return (
    <div className="bg-card border border-border rounded-lg p-4">
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className={`text-2xl font-semibold mt-1 ${color ?? ""}`}>{value}</p>
    </div>
  );
}

function SeverityDot({ severity }: { severity: string }) {
  const colors: Record<string, string> = {
    P0: "bg-[var(--severity-p0)]",
    P1: "bg-[var(--severity-p1)]",
    P2: "bg-[var(--severity-p2)]",
    P3: "bg-[var(--severity-p3)]",
    P4: "bg-[var(--severity-p4)]",
  };
  return (
    <span
      className={`inline-block h-2 w-2 rounded-full ${colors[severity] ?? "bg-muted-foreground"}`}
    />
  );
}

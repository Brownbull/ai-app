import { NavLink } from "react-router-dom";
import { AlertTriangle, LayoutDashboard, Plus } from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { to: "/", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/incidents", icon: AlertTriangle, label: "Incidents" },
  { to: "/submit", icon: Plus, label: "Submit" },
];

export function Sidebar() {
  return (
    <aside className="w-60 border-r border-border bg-card flex flex-col">
      <div className="px-4 py-5 border-b border-border">
        <h1 className="text-lg font-semibold tracking-tight text-primary">
          Triagista
        </h1>
        <p className="text-xs text-muted-foreground mt-0.5">
          SRE Triage Agent
        </p>
      </div>
      <nav className="flex-1 px-2 py-3 space-y-1">
        {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors",
                isActive
                  ? "bg-accent text-accent-foreground"
                  : "text-muted-foreground hover:bg-accent/50 hover:text-foreground"
              )
            }
          >
            <Icon className="h-4 w-4" />
            {label}
          </NavLink>
        ))}
      </nav>
      <div className="px-4 py-3 border-t border-border text-xs text-muted-foreground">
        v0.1.0
      </div>
    </aside>
  );
}

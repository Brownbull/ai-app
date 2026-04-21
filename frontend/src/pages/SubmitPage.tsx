import { type FormEvent, useCallback, useRef, useState } from "react";
import { submitIncident } from "@/lib/api";

const SEVERITY_OPTIONS = ["auto-detect", "P0", "P1", "P2", "P3", "P4"] as const;
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const ALLOWED_TYPES = new Set([
  "image/png",
  "image/jpeg",
  "text/plain",
  "application/json",
  "application/pdf",
]);

type SubmitState =
  | { kind: "idle" }
  | { kind: "submitting" }
  | { kind: "success"; incidentId: string }
  | { kind: "error"; message: string };

export function SubmitPage() {
  const [state, setState] = useState<SubmitState>({ kind: "idle" });
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = useCallback((file: File): string | null => {
    if (!ALLOWED_TYPES.has(file.type)) {
      return `File type "${file.type}" not allowed. Accepted: PNG, JPEG, TXT, JSON, PDF.`;
    }
    if (file.size > MAX_FILE_SIZE) {
      return `File exceeds 10MB limit (${(file.size / 1024 / 1024).toFixed(1)}MB).`;
    }
    return null;
  }, []);

  const handleFile = useCallback(
    (file: File) => {
      const error = validateFile(file);
      if (error) {
        setState({ kind: "error", message: error });
        return;
      }
      setSelectedFile(file);
      setState({ kind: "idle" });
    },
    [validateFile]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    [handleFile]
  );

  const handleSubmit = useCallback(
    async (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      setState({ kind: "submitting" });

      const form = e.currentTarget;
      const formData = new FormData();
      formData.append("title", (form.elements.namedItem("title") as HTMLInputElement).value);
      formData.append(
        "description",
        (form.elements.namedItem("description") as HTMLTextAreaElement).value
      );
      formData.append(
        "reporter_email",
        (form.elements.namedItem("reporter_email") as HTMLInputElement).value
      );
      formData.append(
        "severity_hint",
        (form.elements.namedItem("severity_hint") as HTMLSelectElement).value
      );
      if (selectedFile) {
        formData.append("files", selectedFile);
      }

      try {
        const result = await submitIncident(formData);
        setState({ kind: "success", incidentId: result.incident_id });
        form.reset();
        setSelectedFile(null);
      } catch (err) {
        setState({
          kind: "error",
          message: err instanceof Error ? err.message : "Submission failed",
        });
      }
    },
    [selectedFile]
  );

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold tracking-tight">Submit Incident</h2>
        <p className="text-muted-foreground text-sm mt-1">
          Report a new incident for triage
        </p>
      </div>

      <form onSubmit={handleSubmit} className="bg-card border border-border rounded-lg p-6 max-w-2xl space-y-5">
        {/* Title */}
        <div className="space-y-1.5">
          <label htmlFor="title" className="text-sm font-medium">
            Title <span className="text-destructive">*</span>
          </label>
          <input
            id="title"
            name="title"
            type="text"
            required
            maxLength={500}
            placeholder="Brief description of the incident"
            className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>

        {/* Description */}
        <div className="space-y-1.5">
          <label htmlFor="description" className="text-sm font-medium">
            Description <span className="text-destructive">*</span>
          </label>
          <textarea
            id="description"
            name="description"
            required
            maxLength={8000}
            rows={5}
            placeholder="Detailed description — what happened, what's affected, steps to reproduce..."
            className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring resize-y"
          />
        </div>

        {/* Reporter Email */}
        <div className="space-y-1.5">
          <label htmlFor="reporter_email" className="text-sm font-medium">
            Reporter Email <span className="text-destructive">*</span>
          </label>
          <input
            id="reporter_email"
            name="reporter_email"
            type="email"
            required
            placeholder="you@company.com"
            className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>

        {/* Severity Hint */}
        <div className="space-y-1.5">
          <label htmlFor="severity_hint" className="text-sm font-medium">
            Severity Hint
          </label>
          <select
            id="severity_hint"
            name="severity_hint"
            defaultValue="auto-detect"
            className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            {SEVERITY_OPTIONS.map((opt) => (
              <option key={opt} value={opt}>
                {opt === "auto-detect" ? "Auto-detect" : opt}
              </option>
            ))}
          </select>
        </div>

        {/* File Drop Zone */}
        <div className="space-y-1.5">
          <label className="text-sm font-medium">Attachment</label>
          <div
            onDragOver={(e) => {
              e.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
              dragOver
                ? "border-ring bg-ring/10"
                : "border-border hover:border-muted-foreground"
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".png,.jpg,.jpeg,.txt,.json,.pdf"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleFile(file);
              }}
            />
            {selectedFile ? (
              <div className="flex items-center justify-center gap-2 text-sm">
                <span className="text-primary font-medium">{selectedFile.name}</span>
                <span className="text-muted-foreground">
                  ({(selectedFile.size / 1024).toFixed(1)} KB)
                </span>
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedFile(null);
                  }}
                  className="text-destructive hover:text-destructive/80 text-xs ml-2"
                >
                  Remove
                </button>
              </div>
            ) : (
              <div className="text-sm text-muted-foreground">
                <span className="text-primary font-medium">Click to upload</span> or drag
                and drop
                <br />
                <span className="text-xs">PNG, JPEG, TXT, JSON, PDF — max 10MB</span>
              </div>
            )}
          </div>
        </div>

        {/* Feedback */}
        {state.kind === "error" && (
          <div className="rounded-md border border-destructive/50 bg-destructive/10 px-4 py-3 text-sm text-destructive">
            {state.message}
          </div>
        )}

        {state.kind === "success" && (
          <div className="rounded-md border border-[var(--severity-p4)]/50 bg-[var(--severity-p4)]/10 px-4 py-3 text-sm text-[var(--severity-p4)]">
            Incident <span className="font-mono font-bold">{state.incidentId}</span>{" "}
            submitted.{" "}
            <a
              href={`/incidents`}
              className="underline hover:no-underline"
            >
              View all incidents
            </a>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={state.kind === "submitting"}
          className="inline-flex items-center justify-center rounded-md bg-primary text-primary-foreground px-4 py-2 text-sm font-medium hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {state.kind === "submitting" ? "Submitting..." : "Submit Incident"}
        </button>
      </form>
    </div>
  );
}

"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  api,
  getJSON,
  SEVERITY_ORDER,
  type Finding,
  type RiskCategory,
  type ScanReport,
  type ScanStats,
  type Severity,
} from "@/lib/api";

const RISK: Record<RiskCategory, { label: string; cls: string }> = {
  PROHIBITED: { label: "Prohibited", cls: "border-red-300 bg-red-50 text-red-800" },
  HIGH_RISK: { label: "High risk", cls: "border-orange-300 bg-orange-50 text-orange-800" },
  LIMITED_RISK: { label: "Limited risk", cls: "border-amber-300 bg-amber-50 text-amber-800" },
  MINIMAL_RISK: { label: "Minimal risk", cls: "border-emerald-300 bg-emerald-50 text-emerald-800" },
};

const SEV_CLS: Record<Severity, string> = {
  critical: "text-red-700",
  high: "text-orange-700",
  medium: "text-amber-700",
  low: "text-slate-600",
  info: "text-slate-500",
};

/** Article ids are the product's whole point, so render them readably:
 *  AIACT_ART_5 -> "AI Act Art. 5", GDPR_ART_35 -> "GDPR Art. 35". */
function articleLabel(id: string): string {
  const reg = id.startsWith("AIACT") ? "AI Act" : id.startsWith("GDPR") ? "GDPR" : "";
  const art = id.match(/ART_(\d+[A-Z]?)/)?.[1];
  if (reg && art) return `${reg} Art. ${art}`;
  if (id.includes("ANNEX")) return `${reg} ${id.split("_").slice(1).join(" ")}`.trim();
  return id;
}

export default function ScanPage() {
  const { id } = useParams<{ id: string }>();
  const [report, setReport] = useState<ScanReport | null>(null);
  const [status, setStatus] = useState<string>("loading");
  const [error, setError] = useState<string | null>(null);
  const [severityFilter, setSeverityFilter] = useState<Severity | "all">("all");

  const load = useCallback(async () => {
    try {
      // The list endpoint is the only one carrying status; the detail endpoint
      // has no top-level status field.
      const list = await getJSON<{ scan_id: string; status: string }[]>(api.scans);
      const me = list.find((s) => s.scan_id === id);
      setStatus(me?.status ?? "unknown");
      if (me?.status === "completed" || me?.status === "failed") {
        setReport(await getJSON<ScanReport>(api.scanReport(id)));
      }
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "unreachable");
    }
  }, [id]);

  useEffect(() => {
    load();
    const done = status === "completed" || status === "failed";
    const t = setInterval(load, done ? 30000 : 3000);
    return () => clearInterval(t);
  }, [load, status]);

  const findings = useMemo(() => {
    const all = (report?.profile?.findings ?? []).filter((f) => !f.suppressed);
    const ordered = [...all].sort(
      (a, b) =>
        SEVERITY_ORDER.indexOf(a.severity) - SEVERITY_ORDER.indexOf(b.severity) ||
        b.confidence - a.confidence,
    );
    return severityFilter === "all"
      ? ordered
      : ordered.filter((f) => f.severity === severityFilter);
  }, [report, severityFilter]);

  const counts = useMemo(() => {
    const c: Partial<Record<Severity, number>> = {};
    for (const f of report?.profile?.findings ?? []) {
      if (!f.suppressed) c[f.severity] = (c[f.severity] ?? 0) + 1;
    }
    return c;
  }, [report]);

  const posture = report?.risk_posture;
  const repo = report?.profile?.repo;

  return (
    <div className="space-y-8">
      <div>
        <Link href="/" className="text-[12px] text-slate-500 hover:text-slate-900">
          ← Scans
        </Link>
        <h1 className="mt-2 truncate font-mono text-[16px]">
          {(report?.repo_url ?? "").replace(/^https?:\/\/(www\.)?github\.com\//, "") ||
            id}
        </h1>
      </div>

      {error && (
        <p className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-[12px] text-amber-900">
          Cannot reach the orchestrator — {error}.
        </p>
      )}

      {!report && !error && (
        <p className="text-[13px] text-slate-500">
          {status === "running" || status === "queued"
            ? "Scanning…"
            : "Loading…"}
        </p>
      )}

      {posture && (
        <section className={`rounded-md border px-4 py-3 ${RISK[posture.category].cls}`}>
          <div className="flex items-baseline gap-3">
            <span className="text-[15px] font-semibold">
              {RISK[posture.category].label}
            </span>
            <span className="text-[12px] opacity-80">{posture.reason}</span>
          </div>

          {/* Capability vs deployment: a trigger seen only in test/example code
              does not set the verdict, and saying so is the honest part. */}
          {posture.dampened_triggers && posture.dampened_triggers.length > 0 && (
            <p className="mt-2 border-t border-current/20 pt-2 text-[12px] opacity-90">
              <span className="font-medium">
                {posture.dampened_triggers.join(", ")}
              </span>{" "}
              matched only in test or example code — capability is present, but
              deployment is unverified, so it did not set this verdict.
            </p>
          )}
        </section>
      )}

      {report && (
        <>
          <section>
            <div className="flex items-baseline justify-between">
              <h2 className="text-[13px] font-semibold text-slate-700">
                Findings
              </h2>
              <div className="flex gap-1 text-[11px]">
                <FilterChip
                  active={severityFilter === "all"}
                  onClick={() => setSeverityFilter("all")}
                  label={`all ${report.profile?.findings.filter((f) => !f.suppressed).length ?? 0}`}
                />
                {SEVERITY_ORDER.filter((s) => counts[s]).map((s) => (
                  <FilterChip
                    key={s}
                    active={severityFilter === s}
                    onClick={() => setSeverityFilter(s)}
                    label={`${s} ${counts[s]}`}
                    cls={SEV_CLS[s]}
                  />
                ))}
              </div>
            </div>

            {findings.length === 0 ? (
              <p className="mt-3 text-[13px] text-slate-500">
                No findings at this filter.
              </p>
            ) : (
              <ul className="mt-3 space-y-2">
                {findings.map((f, i) => (
                  <FindingRow key={`${f.rule_id}-${i}`} finding={f} />
                ))}
              </ul>
            )}
          </section>

          <Coverage repo={repo} stats={report.profile?.stats} />
        </>
      )}
    </div>
  );
}

function FilterChip({
  active,
  onClick,
  label,
  cls = "",
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  cls?: string;
}) {
  return (
    <button
      onClick={onClick}
      className={`rounded border px-2 py-0.5 tabular-nums ${
        active ? "border-slate-900 bg-slate-900 text-white" : `border-slate-200 ${cls}`
      }`}
    >
      {label}
    </button>
  );
}

/** One finding, rendered as the trace it is: code → rule → article. */
function FindingRow({ finding: f }: { finding: Finding }) {
  const [open, setOpen] = useState(false);
  const ev = f.evidence[0];
  const demoted = f.triage?.startsWith("llm-demoted");

  return (
    <li className="rounded-md border border-slate-200">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-baseline gap-3 px-3 py-2 text-left hover:bg-slate-50"
      >
        <span className={`shrink-0 font-mono text-[11px] ${SEV_CLS[f.severity]}`}>
          {f.rule_id}
        </span>
        <span className="min-w-0 flex-1 truncate text-[13px]">{f.title}</span>
        <span className="shrink-0 text-[11px] tabular-nums text-slate-500">
          conf {f.confidence.toFixed(2)}
        </span>
        <span className="shrink-0 text-[11px] text-slate-400">
          {open ? "−" : "+"}
        </span>
      </button>

      {/* Collapsed: the single most important line — where in the code. */}
      {!open && ev && (
        <div className="border-t border-slate-100 px-3 py-1.5">
          <span className="font-mono text-[11px] text-slate-600">
            {ev.file}
            {ev.line !== null ? `:${ev.line}` : ""}
          </span>
        </div>
      )}

      {open && (
        <div className="space-y-3 border-t border-slate-100 px-3 py-3">
          {demoted && (
            <p className="rounded border border-slate-200 bg-slate-50 px-2 py-1 text-[11px] text-slate-600">
              {f.triage?.replace("llm-demoted:", "Confidence reduced —")}
            </p>
          )}

          {/* the trace */}
          {f.evidence.map((e, i) => (
            <div key={i} className="space-y-1">
              <div className="font-mono text-[11px] text-slate-600">
                {e.file}
                {e.line !== null ? `:${e.line}` : ""}
              </div>
              {e.excerpt && (
                <pre className="overflow-x-auto rounded bg-slate-50 px-2 py-1.5 font-mono text-[11px] text-slate-800">
                  {e.excerpt}
                </pre>
              )}
            </div>
          ))}

          {f.mapped_articles.length > 0 && (
            <div className="flex flex-wrap items-center gap-1.5">
              <span className="text-[11px] text-slate-400">└─▶</span>
              {f.mapped_articles.map((a) => (
                <span
                  key={a}
                  className="rounded border border-slate-300 px-1.5 py-0.5 font-mono text-[11px]"
                  title={a}
                >
                  {articleLabel(a)}
                </span>
              ))}
            </div>
          )}

          {f.remediation && (
            <p className="text-[12px] leading-relaxed text-slate-700">
              {f.remediation}
            </p>
          )}
        </div>
      )}
    </li>
  );
}

/** What the scanner could and could not read. Without this, "no findings"
 *  and "never looked" render identically — the failure mode this codebase
 *  has hit repeatedly (BUG_LOG DL-019/020/027/028). */
function Coverage({
  repo,
  stats,
}: {
  repo?: ScanReport["profile"] extends infer P
    ? P extends { repo: infer R }
      ? R
      : never
    : never;
  stats?: ScanStats;
}) {
  const manifestErrors = stats?.manifest_scan?.errors ?? [];
  const readErrors = stats?.source_read_errors ?? [];
  const triage = stats?.llm_triage;

  return (
    <section className="rounded-md border border-slate-200 px-4 py-3">
      <h2 className="text-[13px] font-semibold text-slate-700">Coverage</h2>
      <dl className="mt-2 space-y-1 text-[12px] text-slate-600">
        {repo && (
          <Row
            k="Files scanned"
            v={`${repo.scanned_files} of ${repo.total_files}${
              repo.languages?.length ? ` · ${repo.languages.join(", ")}` : ""
            }`}
          />
        )}
        {stats?.manifest_scan && (
          <Row
            k="Manifests read"
            v={
              stats.manifest_scan.files.length
                ? stats.manifest_scan.files.join(", ")
                : "none found"
            }
          />
        )}
        <Row
          k="LLM triage"
          v={
            !triage || triage.status === "skipped"
              ? `not run${triage?.reason ? ` (${triage.reason})` : ""}`
              : triage.status === "failed"
                ? `failed — findings unchanged (${triage.reason ?? ""})`
                : `${triage.reviewed} reviewed, ${triage.demoted} demoted${
                    triage.capped_out ? `, ${triage.capped_out} beyond cap` : ""
                  }`
          }
        />
      </dl>

      {(manifestErrors.length > 0 || readErrors.length > 0) && (
        <div className="mt-3 border-t border-slate-100 pt-2">
          <p className="text-[12px] font-medium text-amber-800">
            Not read — findings here would have been missed
          </p>
          <ul className="mt-1 space-y-0.5 font-mono text-[11px] text-amber-900">
            {[...manifestErrors, ...readErrors].slice(0, 8).map((e, i) => (
              <li key={i}>{e}</li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}

function Row({ k, v }: { k: string; v: string }) {
  return (
    <div className="flex gap-3">
      <dt className="w-32 shrink-0 text-slate-500">{k}</dt>
      <dd className="min-w-0 flex-1 break-words">{v}</dd>
    </div>
  );
}

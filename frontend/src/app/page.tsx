"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api, getJSON, type RiskCategory, type ScanSummary } from "@/lib/api";

const RISK_LABEL: Record<RiskCategory, string> = {
  PROHIBITED: "Prohibited",
  HIGH_RISK: "High risk",
  LIMITED_RISK: "Limited risk",
  MINIMAL_RISK: "Minimal risk",
};

const RISK_CLASS: Record<RiskCategory, string> = {
  PROHIBITED: "text-red-700 bg-red-50 border-red-200",
  HIGH_RISK: "text-orange-700 bg-orange-50 border-orange-200",
  LIMITED_RISK: "text-amber-700 bg-amber-50 border-amber-200",
  MINIMAL_RISK: "text-emerald-700 bg-emerald-50 border-emerald-200",
};

export default function Home() {
  const router = useRouter();
  const [scans, setScans] = useState<ScanSummary[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [repoUrl, setRepoUrl] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const data = await getJSON<ScanSummary[]>(api.scans);
      setScans(Array.isArray(data) ? data : []);
      setLoadError(null);
    } catch (e) {
      // Report an unreachable backend rather than rendering an empty list,
      // which reads identically to "no scans yet".
      setLoadError(e instanceof Error ? e.message : "unreachable");
    } finally {
      setLoaded(true);
    }
  }, []);

  const anyActive = scans.some(
    (s) => s.status === "running" || s.status === "queued",
  );

  useEffect(() => {
    load();
    const id = setInterval(load, anyActive ? 3000 : 15000);
    return () => clearInterval(id);
  }, [load, anyActive]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const url = repoUrl.trim();
    if (!url) return;
    setSubmitting(true);
    setSubmitError(null);
    try {
      const res = await fetch(api.scans, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: url }),
      });
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      const scan = (await res.json()) as ScanSummary;
      router.push(`/scans/${scan.scan_id}`);
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : "failed to start scan");
      setSubmitting(false);
    }
  }

  return (
    <div className="space-y-10">
      <section>
        <h1 className="text-[22px] font-semibold tracking-tight">
          Scan a repository
        </h1>
        <p className="mt-1 max-w-2xl text-[13px] leading-relaxed text-slate-600">
          Deterministic scanners detect AI-system patterns and map them to EU AI
          Act and GDPR articles. Every finding cites the line of code it came
          from and the article it maps to.
        </p>

        <form onSubmit={submit} className="mt-5 flex gap-2">
          <input
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/owner/repo"
            className="flex-1 rounded-md border border-slate-300 px-3 py-2 font-mono text-[13px] outline-none focus:border-slate-500"
            disabled={submitting}
            aria-label="Repository URL"
          />
          <button
            type="submit"
            disabled={submitting || !repoUrl.trim()}
            className="rounded-md bg-slate-900 px-4 py-2 text-[13px] font-medium text-white disabled:opacity-40"
          >
            {submitting ? "Starting…" : "Scan"}
          </button>
        </form>
        {submitError && (
          <p className="mt-2 text-[12px] text-red-700">{submitError}</p>
        )}
      </section>

      <section>
        <h2 className="text-[13px] font-semibold text-slate-700">Scans</h2>

        {loadError && (
          <p className="mt-3 rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-[12px] text-amber-900">
            Cannot reach the orchestrator at{" "}
            <span className="font-mono">{api.base}</span> — {loadError}. This is
            a connection failure, not an empty result.
          </p>
        )}

        {!loadError && loaded && scans.length === 0 && (
          <p className="mt-3 text-[13px] text-slate-500">No scans yet.</p>
        )}

        <ul className="mt-3 divide-y divide-slate-100">
          {scans.map((s) => (
            <li key={s.scan_id}>
              <Link
                href={`/scans/${s.scan_id}`}
                className="flex items-center gap-4 py-3 hover:bg-slate-50"
              >
                <span className="min-w-0 flex-1 truncate font-mono text-[13px]">
                  {s.repo_url.replace(/^https?:\/\/(www\.)?github\.com\//, "")}
                </span>

                {s.status === "completed" && s.risk_category ? (
                  <span
                    className={`shrink-0 rounded border px-2 py-0.5 text-[11px] font-medium ${RISK_CLASS[s.risk_category]}`}
                  >
                    {RISK_LABEL[s.risk_category]}
                  </span>
                ) : (
                  <span className="shrink-0 text-[11px] text-slate-500">
                    {s.status === "failed" ? "failed" : "scanning…"}
                  </span>
                )}

                <span className="w-24 shrink-0 text-right text-[12px] tabular-nums text-slate-500">
                  {s.finding_count ?? 0} finding
                  {s.finding_count === 1 ? "" : "s"}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

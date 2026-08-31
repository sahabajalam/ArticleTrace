"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
    ArrowLeft, ShieldCheck, AlertTriangle, Clock, Loader2, XCircle,
    FileCode, Gauge, BookOpen, ListChecks, Sparkles, ChevronRight, GitBranch,
    Download, Filter,
} from "lucide-react";
import { api, type ScanState, type Severity, type Finding, type RiskPosture } from "@/lib/api";
import { cn } from "@/lib/utils";

const RISK_STYLE: Record<string, { bar: string; bg: string; text: string; border: string; label: string }> = {
    PROHIBITED: { bar: "bg-red-500", bg: "bg-red-50", text: "text-red-700", border: "border-red-200", label: "Prohibited" },
    HIGH_RISK: { bar: "bg-rose-500", bg: "bg-rose-50", text: "text-rose-700", border: "border-rose-200", label: "High Risk" },
    LIMITED_RISK: { bar: "bg-amber-500", bg: "bg-amber-50", text: "text-amber-700", border: "border-amber-200", label: "Limited Risk" },
    MINIMAL_RISK: { bar: "bg-emerald-500", bg: "bg-emerald-50", text: "text-emerald-700", border: "border-emerald-200", label: "Minimal Risk" },
};

const SEVERITY_STYLE: Record<Severity, string> = {
    critical: "bg-red-50 text-red-700 border-red-200",
    high: "bg-rose-50 text-rose-700 border-rose-200",
    medium: "bg-amber-50 text-amber-700 border-amber-200",
    low: "bg-sky-50 text-sky-700 border-sky-200",
    info: "bg-slate-50 text-slate-600 border-slate-200",
};

const PRIORITY_STYLE: Record<string, string> = {
    immediate: "bg-red-50 text-red-700 border-red-200",
    short_term: "bg-amber-50 text-amber-700 border-amber-200",
    long_term: "bg-sky-50 text-sky-700 border-sky-200",
};

export default function ScanDetailPage() {
    const params = useParams<{ id: string }>();
    const scanId = params.id;
    const [scan, setScan] = useState<ScanState | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!scanId) return;
        let cancelled = false;

        async function load() {
            try {
                const res = await fetch(api.scan(scanId));
                if (!res.ok) throw new Error(`Failed to load scan (${res.status})`);
                const data = (await res.json()) as ScanState;
                if (cancelled) return;
                setScan(data);
                if (data.workflow_status === "running" || data.workflow_status === "queued") {
                    setTimeout(load, 2000);
                }
            } catch (err) {
                if (!cancelled) setError(err instanceof Error ? err.message : "Unknown error");
            }
        }
        load();
        return () => {
            cancelled = true;
        };
    }, [scanId]);

    const findings = useMemo(
        () => (scan?.profile?.findings ?? []).filter((f) => !f.suppressed),
        [scan]
    );

    if (error) {
        return (
            <div className="max-w-3xl mx-auto mt-12">
                <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 flex items-start gap-3">
                    <XCircle className="w-5 h-5 text-rose-500 shrink-0" />
                    <div>
                        <p className="text-[14px] font-semibold text-rose-700">Could not load scan</p>
                        <p className="text-[12px] text-rose-600 mt-1">{error}</p>
                    </div>
                </div>
            </div>
        );
    }

    if (!scan) {
        return (
            <div className="flex items-center justify-center py-20 text-slate-400">
                <Loader2 className="w-5 h-5 animate-spin mr-2" />
                <span className="text-[13px]">Loading scan…</span>
            </div>
        );
    }

    const status = scan.workflow_status;
    const running = status === "running" || status === "queued";

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Header */}
            <div className="flex items-start justify-between gap-4">
                <div className="min-w-0">
                    <Link href="/" className="text-[11px] text-slate-400 hover:text-indigo-600 flex items-center gap-1 mb-2">
                        <ArrowLeft className="w-3 h-3" /> Back to dashboard
                    </Link>
                    <h1 className="text-[22px] font-bold text-slate-900 tracking-tight flex items-center gap-2 truncate">
                        <FileCode className="w-5 h-5 text-indigo-600 shrink-0" />
                        <span className="truncate">{scan.repo_url}</span>
                    </h1>
                    <div className="flex items-center gap-3 mt-1 text-[12px] text-slate-500">
                        <span className="inline-flex items-center gap-1">
                            <GitBranch className="w-3 h-3" /> {scan.ref}
                        </span>
                        <span className="font-mono text-[11px]">{scan.scan_id}</span>
                    </div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                    {status === "completed" && (
                        <DownloadReportButton scan={scan} />
                    )}
                    <StatusBadge status={status} currentStep={scan.current_step} />
                </div>
            </div>

            {running && <ProgressCard currentStep={scan.current_step} />}

            {status === "failed" && scan.errors.length > 0 && (
                <div className="bg-rose-50 border border-rose-200 rounded-xl p-5">
                    <p className="text-[13px] font-semibold text-rose-700 flex items-center gap-1.5">
                        <XCircle className="w-4 h-4" /> Scan failed
                    </p>
                    <ul className="mt-2 space-y-1 text-[12px] text-rose-700 list-disc list-inside">
                        {scan.errors.map((e, i) => (
                            <li key={i}>{e}</li>
                        ))}
                    </ul>
                </div>
            )}

            {scan.risk_posture && <RiskPostureCard posture={scan.risk_posture} />}

            {scan.profile && (
                <ProfileCard
                    aiComponents={scan.profile.ai_components}
                    decisionSurfaces={scan.profile.decision_surfaces}
                    dataSignals={scan.profile.data_signals}
                    scannedFiles={scan.profile.repo.scanned_files}
                    totalFiles={scan.profile.repo.total_files}
                    languages={scan.profile.repo.languages}
                />
            )}

            {scan.narrative && <NarrativeCard narrative={scan.narrative} />}

            {findings.length > 0 && (
                <FindingsTable findings={findings} citations={scan.finding_citations} />
            )}

            {scan.narrative?.remediation_plan?.length ? (
                <RemediationCard plan={scan.narrative.remediation_plan} />
            ) : null}
        </div>
    );
}

function StatusBadge({ status, currentStep }: { status: string; currentStep: string }) {
    const map: Record<string, { label: string; classes: string; icon: React.ComponentType<{ className?: string }> }> = {
        queued: { label: "Queued", classes: "bg-slate-50 text-slate-600 border-slate-200", icon: Clock },
        running: { label: currentStep || "Running", classes: "bg-blue-50 text-blue-700 border-blue-200", icon: Loader2 },
        completed: { label: "Completed", classes: "bg-emerald-50 text-emerald-700 border-emerald-200", icon: ShieldCheck },
        failed: { label: "Failed", classes: "bg-rose-50 text-rose-700 border-rose-200", icon: XCircle },
    };
    const cfg = map[status] ?? map.queued;
    const Icon = cfg.icon;
    return (
        <span className={cn("inline-flex items-center gap-1.5 px-2.5 py-1 text-[11px] font-semibold rounded-md border shrink-0", cfg.classes)}>
            <Icon className={cn("w-3 h-3", status === "running" && "animate-spin")} />
            {cfg.label}
        </span>
    );
}

// These IDs must match the `current_step` strings written by the backend
// (see orchestrator/src/api/scans.py and orchestrator/src/agents/*.py).
// If they don't match, idx === -1 and the bar is stuck at 0%.
const WORKFLOW_STEPS: { id: string; label: string }[] = [
    { id: "queued", label: "Queued" },
    { id: "ingesting", label: "Ingest" },
    { id: "scanned", label: "Scan" },
    { id: "legal_researched", label: "Legal" },
    { id: "risk_classified", label: "Risk" },
    { id: "narrative_generated", label: "Narrative" },
    { id: "completed", label: "Done" },
];

function ProgressCard({ currentStep }: { currentStep: string }) {
    const idx = WORKFLOW_STEPS.findIndex((s) => s.id === currentStep);
    // While step is unknown (e.g. transient state), show a minimal 5% so the
    // bar doesn't read as "nothing happening" when work clearly is happening.
    const pct = idx >= 0 ? ((idx + 1) / WORKFLOW_STEPS.length) * 100 : 5;
    return (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5">
            <div className="flex items-center justify-between mb-2">
                <p className="text-[13px] font-semibold text-slate-800">Workflow progress</p>
                <span className="text-[11px] text-slate-400">{Math.round(pct)}%</span>
            </div>
            <div className="h-1.5 rounded-full bg-slate-100 overflow-hidden">
                <div
                    className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 transition-all duration-500"
                    style={{ width: `${pct}%` }}
                />
            </div>
            <div className="flex justify-between mt-3 gap-1">
                {WORKFLOW_STEPS.map((step, i) => (
                    <div key={step.id} className="flex-1 text-center">
                        <div
                            className={cn(
                                "w-2 h-2 rounded-full mx-auto mb-1",
                                i <= idx ? "bg-indigo-500" : "bg-slate-200"
                            )}
                        />
                        <p className={cn("text-[10px] font-medium", i === idx ? "text-indigo-600" : "text-slate-400")}>
                            {step.label}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}

function RiskPostureCard({ posture }: { posture: RiskPosture }) {
    const style = RISK_STYLE[posture.category] ?? RISK_STYLE.MINIMAL_RISK;
    const scorePct = Math.max(0, Math.min(100, posture.compliance_score));
    return (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5">
            <div className="flex items-start justify-between gap-4 mb-4">
                <div>
                    <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Risk posture</p>
                    <div className="flex items-center gap-2 mt-1">
                        <span className={cn("w-2.5 h-2.5 rounded-full", style.bar)} />
                        <h2 className={cn("text-[18px] font-bold", style.text)}>{style.label}</h2>
                    </div>
                    <p className="text-[12px] text-slate-500 mt-1.5 max-w-xl">{posture.reason}</p>
                </div>
                <div className="text-right shrink-0">
                    <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1 justify-end">
                        <Gauge className="w-3 h-3" /> Score
                    </p>
                    <p className="text-3xl font-bold text-slate-900 tracking-tight mt-1">{Math.round(scorePct)}</p>
                    <p className="text-[10px] text-slate-400">/ 100</p>
                </div>
            </div>

            <div className="h-1.5 rounded-full bg-slate-100 overflow-hidden mb-4">
                <div
                    className={cn("h-full transition-all duration-700", style.bar)}
                    style={{ width: `${scorePct}%` }}
                />
            </div>

            <div className="grid grid-cols-4 gap-3">
                {[
                    { label: "Critical", value: posture.critical_count, tone: "text-red-600" },
                    { label: "High", value: posture.high_count, tone: "text-rose-600" },
                    { label: "Medium", value: posture.medium_count, tone: "text-amber-600" },
                    { label: "Low", value: posture.low_count, tone: "text-sky-600" },
                ].map((s) => (
                    <div key={s.label} className="text-center p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                        <p className={cn("text-xl font-bold tracking-tight", s.tone)}>{s.value}</p>
                        <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mt-0.5">{s.label}</p>
                    </div>
                ))}
            </div>

            {posture.prohibited_triggers.length > 0 && (
                <div className="mt-4 p-3 rounded-lg bg-red-50 border border-red-200">
                    <p className="text-[11px] font-semibold uppercase tracking-wider text-red-600 mb-1.5 flex items-center gap-1">
                        <AlertTriangle className="w-3 h-3" /> Prohibited triggers
                    </p>
                    <ul className="space-y-0.5">
                        {posture.prohibited_triggers.map((t, i) => (
                            <li key={i} className="text-[12px] text-red-700 font-mono">{t}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

function ProfileCard({
    aiComponents,
    decisionSurfaces,
    dataSignals,
    scannedFiles,
    totalFiles,
    languages,
}: {
    aiComponents: { kind: string; name: string }[];
    decisionSurfaces: { endpoint: string; file: string; line: number; calls_model: boolean; has_human_review: boolean; has_audit_log: boolean }[];
    dataSignals: { pii_fields: string[]; has_dpia_doc: boolean; has_model_card: boolean; has_data_card: boolean; audit_logging: string };
    scannedFiles: number;
    totalFiles: number;
    languages: string[];
}) {
    return (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5">
            <h2 className="text-[13px] font-semibold text-slate-800 mb-4 flex items-center gap-1.5">
                <FileCode className="w-3.5 h-3.5 text-indigo-600" /> System Profile
            </h2>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-5">
                <Stat label="Files scanned" value={`${scannedFiles}/${totalFiles}`} />
                <Stat label="AI components" value={aiComponents.length} />
                <Stat label="Decision surfaces" value={decisionSurfaces.length} />
                <Stat label="PII fields" value={dataSignals.pii_fields.length} />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2">Languages</p>
                    <div className="flex flex-wrap gap-1.5">
                        {languages.length ? languages.map((l) => (
                            <span key={l} className="text-[11px] font-medium px-2 py-0.5 rounded-md bg-slate-50 border border-slate-200 text-slate-600">{l}</span>
                        )) : <span className="text-[11px] text-slate-400">None detected</span>}
                    </div>
                </div>
                <div>
                    <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2">Documentation</p>
                    <div className="flex flex-wrap gap-1.5">
                        <DocPill label="DPIA" present={dataSignals.has_dpia_doc} />
                        <DocPill label="Model card" present={dataSignals.has_model_card} />
                        <DocPill label="Data card" present={dataSignals.has_data_card} />
                        <span className={cn(
                            "text-[11px] font-medium px-2 py-0.5 rounded-md border",
                            dataSignals.audit_logging === "present" ? "bg-emerald-50 text-emerald-700 border-emerald-200" :
                            dataSignals.audit_logging === "partial" ? "bg-amber-50 text-amber-700 border-amber-200" :
                            "bg-slate-50 text-slate-500 border-slate-200"
                        )}>
                            Audit: {dataSignals.audit_logging}
                        </span>
                    </div>
                </div>
            </div>

            {aiComponents.length > 0 && (
                <div className="mt-5">
                    <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2">AI components detected</p>
                    <div className="flex flex-wrap gap-1.5">
                        {aiComponents.map((c, i) => (
                            <span key={i} className="text-[11px] font-medium px-2 py-0.5 rounded-md bg-violet-50 border border-violet-200 text-violet-700">
                                {c.kind}: <span className="font-mono">{c.name}</span>
                            </span>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

function DocPill({ label, present }: { label: string; present: boolean }) {
    return (
        <span className={cn(
            "text-[11px] font-medium px-2 py-0.5 rounded-md border",
            present ? "bg-emerald-50 text-emerald-700 border-emerald-200" : "bg-slate-50 text-slate-400 border-slate-200"
        )}>
            {present ? "✓" : "—"} {label}
        </span>
    );
}

function Stat({ label, value }: { label: string; value: string | number }) {
    return (
        <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100 text-center">
            <p className="text-xl font-bold text-slate-900 tracking-tight">{value}</p>
            <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mt-0.5">{label}</p>
        </div>
    );
}

function NarrativeCard({ narrative }: { narrative: NonNullable<ScanState["narrative"]> }) {
    return (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
            <h2 className="text-[13px] font-semibold text-slate-800 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-violet-600" /> Executive Narrative
            </h2>
            <NarrativeSection title="Executive Summary" body={narrative.executive_summary} />
            <NarrativeSection title="Risk Narrative" body={narrative.risk_narrative} />
            <NarrativeSection title="Top Findings" body={narrative.top_findings_narrative} />
        </div>
    );
}

function NarrativeSection({ title, body }: { title: string; body: string }) {
    if (!body) return null;
    return (
        <div>
            <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1">{title}</p>
            <p className="text-[13px] text-slate-700 leading-relaxed whitespace-pre-wrap">{body}</p>
        </div>
    );
}

const SEVERITY_ORDER: Severity[] = ["critical", "high", "medium", "low", "info"];

function FindingsTable({ findings, citations }: { findings: Finding[]; citations: ScanState["finding_citations"] }) {
    const [expanded, setExpanded] = useState<string | null>(null);
    const [severityFilter, setSeverityFilter] = useState<Set<Severity>>(new Set());
    const [query, setQuery] = useState("");
    const citationMap = useMemo(() => {
        const m = new Map<string, ScanState["finding_citations"][number]>();
        citations.forEach((c) => m.set(c.rule_id, c));
        return m;
    }, [citations]);

    const severityCounts = useMemo(() => {
        const counts: Record<Severity, number> = { critical: 0, high: 0, medium: 0, low: 0, info: 0 };
        findings.forEach((f) => { counts[f.severity] += 1; });
        return counts;
    }, [findings]);

    const filtered = useMemo(() => {
        const q = query.trim().toLowerCase();
        return findings.filter((f) => {
            if (severityFilter.size > 0 && !severityFilter.has(f.severity)) return false;
            if (!q) return true;
            if (f.rule_id.toLowerCase().includes(q)) return true;
            if (f.title.toLowerCase().includes(q)) return true;
            if (f.evidence.some((e) => e.file.toLowerCase().includes(q))) return true;
            return false;
        });
    }, [findings, severityFilter, query]);

    function toggleSeverity(s: Severity) {
        setSeverityFilter((prev) => {
            const next = new Set(prev);
            if (next.has(s)) next.delete(s); else next.add(s);
            return next;
        });
    }

    return (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between gap-3">
                <h2 className="text-[13px] font-semibold text-slate-800 flex items-center gap-1.5 shrink-0">
                    <BookOpen className="w-3.5 h-3.5 text-indigo-600" /> Findings
                </h2>
                <span className="text-[11px] text-slate-400 shrink-0">
                    {filtered.length === findings.length
                        ? `${findings.length} total`
                        : `${filtered.length} of ${findings.length}`}
                </span>
            </div>
            <div className="px-5 py-3 border-b border-slate-100 flex flex-wrap items-center gap-2 bg-slate-50/40">
                <Filter className="w-3 h-3 text-slate-400 shrink-0" />
                {SEVERITY_ORDER.map((s) => {
                    const count = severityCounts[s];
                    if (count === 0) return null;
                    const active = severityFilter.has(s);
                    return (
                        <button
                            key={s}
                            onClick={() => toggleSeverity(s)}
                            className={cn(
                                "text-[10px] font-bold uppercase px-1.5 py-0.5 rounded border transition-all",
                                active
                                    ? SEVERITY_STYLE[s]
                                    : "bg-white text-slate-500 border-slate-200 hover:border-slate-300"
                            )}
                        >
                            {s} <span className="font-mono opacity-70">{count}</span>
                        </button>
                    );
                })}
                {severityFilter.size > 0 && (
                    <button
                        onClick={() => setSeverityFilter(new Set())}
                        className="text-[10px] font-medium text-slate-500 hover:text-slate-700 underline underline-offset-2"
                    >
                        clear
                    </button>
                )}
                <input
                    type="search"
                    placeholder="Filter by rule, title, or file…"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="ml-auto w-56 max-w-full px-2 py-1 text-[11px] rounded-md border border-slate-200 bg-white text-slate-700 placeholder:text-slate-400 focus:outline-none focus:border-indigo-300 focus:ring-1 focus:ring-indigo-200"
                />
            </div>
            <div className="divide-y divide-slate-50">
                {filtered.length === 0 ? (
                    <div className="px-5 py-8 text-center text-[12px] text-slate-400">
                        No findings match the current filters.
                    </div>
                ) : filtered.map((f, idx) => {
                    const cit = citationMap.get(f.rule_id);
                    // Same rule can fire multiple times (e.g. AI-001 across 4 files);
                    // compose the key + expanded id from rule_id, evidence location,
                    // and index so each row is uniquely keyed and independently expandable.
                    const ev0 = f.evidence[0];
                    const rowId = `${f.rule_id}:${ev0?.file ?? "?"}:${ev0?.line ?? 0}:${idx}`;
                    const isOpen = expanded === rowId;
                    return (
                        <div key={rowId}>
                            <button
                                onClick={() => setExpanded(isOpen ? null : rowId)}
                                className="w-full px-5 py-3.5 flex items-start gap-3 hover:bg-slate-50/50 transition-colors text-left"
                            >
                                <span className={cn("text-[10px] font-bold px-1.5 py-0.5 rounded border uppercase shrink-0 mt-0.5", SEVERITY_STYLE[f.severity])}>
                                    {f.severity}
                                </span>
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-2">
                                        <p className="text-[13px] font-semibold text-slate-800 truncate">{f.title}</p>
                                        <span className="text-[10px] font-mono text-slate-400 shrink-0">{f.rule_id}</span>
                                    </div>
                                    {f.evidence[0] && (
                                        <p className="text-[11px] text-slate-500 font-mono truncate mt-0.5">
                                            {f.evidence[0].file}:{f.evidence[0].line}
                                            {f.evidence[0].excerpt && <span className="text-slate-400"> — {f.evidence[0].excerpt}</span>}
                                        </p>
                                    )}
                                    {f.mapped_articles.length > 0 && (
                                        <div className="flex flex-wrap gap-1 mt-1.5">
                                            {f.mapped_articles.map((a) => (
                                                <span key={a} className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-indigo-50 text-indigo-700 border border-indigo-100">
                                                    {a}
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                </div>
                                <ChevronRight className={cn("w-4 h-4 text-slate-300 shrink-0 mt-1 transition-transform", isOpen && "rotate-90")} />
                            </button>

                            {isOpen && (
                                <div className="px-5 pb-4 pt-1 bg-slate-50/50 space-y-3 animate-in fade-in slide-in-from-top-1 duration-200">
                                    {f.evidence.length > 1 && (
                                        <div>
                                            <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-1">All evidence</p>
                                            <ul className="space-y-1">
                                                {f.evidence.map((e, i) => (
                                                    <li key={i} className="text-[11px] font-mono text-slate-600">
                                                        {e.file}:{e.line}
                                                        {e.excerpt && <span className="text-slate-400"> — {e.excerpt}</span>}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                    {f.remediation && (
                                        <div>
                                            <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-1">Remediation</p>
                                            <p className="text-[12px] text-slate-700 leading-relaxed">{f.remediation}</p>
                                        </div>
                                    )}
                                    {cit && cit.citations.length > 0 && (
                                        <div>
                                            <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-1">Legal citations</p>
                                            <ul className="space-y-1.5">
                                                {cit.citations.map((c, i) => (
                                                    <li key={i} className="text-[12px] text-slate-700 p-2 rounded-md bg-white border border-slate-200">
                                                        <span className="font-semibold text-indigo-700">{c.regulation} Art. {c.article_number}</span>
                                                        {c.title && <span className="text-slate-600"> — {c.title}</span>}
                                                        {c.text_snippet && <p className="text-[11px] text-slate-500 mt-0.5 italic">“{c.text_snippet}”</p>}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                    {cit && cit.reasoning_chain.length > 0 && (
                                        <div>
                                            <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-1">Reasoning chain</p>
                                            <ol className="space-y-0.5 list-decimal list-inside">
                                                {cit.reasoning_chain.map((r, i) => (
                                                    <li key={i} className="text-[11px] text-slate-600">{r}</li>
                                                ))}
                                            </ol>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

function DownloadReportButton({ scan }: { scan: ScanState }) {
    function handleDownload() {
        const md = buildMarkdownReport(scan);
        const blob = new Blob([md], { type: "text/markdown;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = reportFilename(scan);
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    return (
        <button
            onClick={handleDownload}
            className="inline-flex items-center gap-1.5 px-2.5 py-1 text-[11px] font-semibold rounded-md border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 hover:border-slate-300 transition-colors"
            title="Download Markdown report"
        >
            <Download className="w-3 h-3" />
            Report
        </button>
    );
}

function reportFilename(scan: ScanState): string {
    let repoSlug = "scan";
    try {
        const u = new URL(scan.repo_url);
        repoSlug = u.pathname.replace(/^\/+|\.git$/g, "").replace(/\//g, "-") || u.hostname;
    } catch {
        repoSlug = scan.repo_url.replace(/[^a-z0-9]+/gi, "-").slice(0, 40) || "scan";
    }
    return `compliance-${repoSlug}-${scan.scan_id.slice(0, 8)}.md`;
}

function buildMarkdownReport(scan: ScanState): string {
    const lines: string[] = [];
    const posture = scan.risk_posture;
    const profile = scan.profile;
    const narrative = scan.narrative;
    const findings = (profile?.findings ?? []).filter((f) => !f.suppressed);
    const citationMap = new Map<string, ScanState["finding_citations"][number]>();
    scan.finding_citations.forEach((c) => citationMap.set(c.rule_id, c));

    lines.push(`# EU AI Act Compliance Report`);
    lines.push("");
    lines.push(`**Repository:** ${scan.repo_url}`);
    lines.push(`**Ref:** \`${scan.ref}\``);
    lines.push(`**Scan ID:** \`${scan.scan_id}\``);
    if (scan.completed_at) lines.push(`**Completed:** ${scan.completed_at}`);
    lines.push("");

    if (posture) {
        lines.push(`## Risk Posture`);
        lines.push("");
        lines.push(`- **Category:** ${posture.category.replace("_", " ")}`);
        lines.push(`- **Compliance score:** ${Math.round(posture.compliance_score)} / 100`);
        lines.push(`- **Findings by severity:** ${posture.critical_count} critical · ${posture.high_count} high · ${posture.medium_count} medium · ${posture.low_count} low`);
        if (posture.reason) lines.push(`- **Reasoning:** ${posture.reason}`);
        if (posture.prohibited_triggers.length > 0) {
            lines.push(`- **Prohibited triggers:** ${posture.prohibited_triggers.map((t) => `\`${t}\``).join(", ")}`);
        }
        lines.push("");
    }

    if (profile) {
        lines.push(`## System Profile`);
        lines.push("");
        lines.push(`- **Files scanned:** ${profile.repo.scanned_files} / ${profile.repo.total_files}`);
        lines.push(`- **Languages:** ${profile.repo.languages.join(", ") || "—"}`);
        lines.push(`- **AI components detected:** ${profile.ai_components.length}`);
        lines.push(`- **Decision surfaces:** ${profile.decision_surfaces.length}`);
        lines.push(`- **PII fields:** ${profile.data_signals.pii_fields.join(", ") || "—"}`);
        lines.push(`- **Documentation:** DPIA ${tick(profile.data_signals.has_dpia_doc)} · Model card ${tick(profile.data_signals.has_model_card)} · Data card ${tick(profile.data_signals.has_data_card)}`);
        lines.push(`- **Audit logging:** ${profile.data_signals.audit_logging}`);
        lines.push("");
    }

    if (narrative) {
        if (narrative.executive_summary) {
            lines.push(`## Executive Summary`);
            lines.push("");
            lines.push(narrative.executive_summary.trim());
            lines.push("");
        }
        if (narrative.risk_narrative) {
            lines.push(`## Risk Narrative`);
            lines.push("");
            lines.push(narrative.risk_narrative.trim());
            lines.push("");
        }
        if (narrative.top_findings_narrative) {
            lines.push(`## Top Findings`);
            lines.push("");
            lines.push(narrative.top_findings_narrative.trim());
            lines.push("");
        }
    }

    if (findings.length > 0) {
        lines.push(`## Findings (${findings.length})`);
        lines.push("");
        findings.forEach((f) => {
            lines.push(`### \`${f.rule_id}\` — ${f.title}`);
            lines.push("");
            lines.push(`- **Severity:** ${f.severity}`);
            lines.push(`- **Confidence:** ${(f.confidence * 100).toFixed(0)}%`);
            if (f.mapped_articles.length > 0) {
                lines.push(`- **Mapped articles:** ${f.mapped_articles.map((a) => `\`${a}\``).join(", ")}`);
            }
            if (f.evidence.length > 0) {
                lines.push(`- **Evidence:**`);
                f.evidence.slice(0, 10).forEach((e) => {
                    const loc = `\`${e.file}:${e.line}\``;
                    lines.push(`  - ${loc}${e.excerpt ? ` — ${e.excerpt}` : ""}`);
                });
            }
            if (f.remediation) {
                lines.push(`- **Remediation:** ${f.remediation}`);
            }
            const cit = citationMap.get(f.rule_id);
            if (cit && cit.citations.length > 0) {
                lines.push(`- **Legal citations:**`);
                cit.citations.forEach((c) => {
                    const head = `${c.regulation} Art. ${c.article_number}`;
                    const title = c.title ? ` — ${c.title}` : "";
                    lines.push(`  - **${head}**${title}`);
                    if (c.text_snippet) lines.push(`    > ${c.text_snippet.replace(/\n+/g, " ")}`);
                });
            }
            lines.push("");
        });
    }

    if (narrative?.remediation_plan?.length) {
        lines.push(`## Remediation Plan`);
        lines.push("");
        narrative.remediation_plan.forEach((step, i) => {
            lines.push(`### ${i + 1}. [${step.priority.replace("_", " ")}] ${step.title}`);
            lines.push("");
            lines.push(step.description);
            lines.push("");
            lines.push(`*Effort: ${step.effort}*${step.finding_rule_ids.length ? ` · *Addresses:* ${step.finding_rule_ids.map((r) => `\`${r}\``).join(", ")}` : ""}`);
            lines.push("");
        });
    }

    lines.push(`---`);
    lines.push(`*Generated by ArticleTrace Compliance Engine.*`);
    return lines.join("\n");
}

function tick(b: boolean): string {
    return b ? "✓" : "✗";
}

function RemediationCard({ plan }: { plan: NonNullable<ScanState["narrative"]>["remediation_plan"] }) {
    return (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100">
                <h2 className="text-[13px] font-semibold text-slate-800 flex items-center gap-1.5">
                    <ListChecks className="w-3.5 h-3.5 text-indigo-600" /> Remediation Plan
                </h2>
            </div>
            <div className="divide-y divide-slate-50">
                {plan.map((step, i) => (
                    <div key={i} className="px-5 py-3.5 flex items-start gap-3">
                        <span className={cn(
                            "text-[10px] font-bold px-1.5 py-0.5 rounded border uppercase shrink-0 mt-0.5",
                            PRIORITY_STYLE[step.priority] ?? "bg-slate-50 text-slate-600 border-slate-200"
                        )}>
                            {step.priority.replace("_", " ")}
                        </span>
                        <div className="flex-1 min-w-0">
                            <p className="text-[13px] font-semibold text-slate-800">{step.title}</p>
                            <p className="text-[12px] text-slate-600 mt-0.5 leading-relaxed">{step.description}</p>
                            <div className="flex items-center gap-2 mt-1.5">
                                <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                                    Effort: {step.effort}
                                </span>
                                {step.finding_rule_ids.length > 0 && (
                                    <span className="text-[10px] font-mono text-slate-400">
                                        {step.finding_rule_ids.join(", ")}
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
    ShieldCheck, AlertTriangle, CheckCircle, Loader2,
    ArrowUpRight, Database, Zap, ScanSearch,
    TrendingUp, Scale, ChevronRight, XCircle,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { api, type ScanSummary } from "@/lib/api";

function computeStats(scans: ScanSummary[]) {
    const total = scans.length;
    const running = scans.filter((s) => s.status === "running" || s.status === "queued").length;
    const completed = scans.filter((s) => s.status === "completed").length;
    const failed = scans.filter((s) => s.status === "failed").length;
    const highRisk = scans.filter(
        (s) => s.risk_category === "HIGH_RISK" || s.risk_category === "PROHIBITED"
    ).length;
    const compliant = scans.filter(
        (s) => s.status === "completed" &&
            (s.risk_category === "MINIMAL_RISK" || s.risk_category === "LIMITED_RISK") &&
            (s.compliance_score ?? 0) >= 70
    ).length;
    return { total, running, completed, failed, highRisk, compliant };
}

const RISK_COLORS: Record<string, string> = {
    PROHIBITED: "bg-red-500",
    HIGH_RISK: "bg-rose-500",
    LIMITED_RISK: "bg-amber-500",
    MINIMAL_RISK: "bg-emerald-500",
};

const RISK_BADGES: Record<string, string> = {
    PROHIBITED: "bg-red-50 text-red-600 border-red-200",
    HIGH_RISK: "bg-rose-50 text-rose-600 border-rose-200",
    LIMITED_RISK: "bg-amber-50 text-amber-700 border-amber-200",
    MINIMAL_RISK: "bg-emerald-50 text-emerald-700 border-emerald-200",
};

const STATUS_BADGES: Record<string, { label: string; classes: string }> = {
    completed: { label: "Completed", classes: "bg-emerald-50 text-emerald-700 border-emerald-200" },
    running: { label: "Running", classes: "bg-blue-50 text-blue-600 border-blue-200" },
    queued: { label: "Queued", classes: "bg-slate-50 text-slate-500 border-slate-200" },
    failed: { label: "Failed", classes: "bg-rose-50 text-rose-600 border-rose-200" },
};

function Skeleton({ className }: { className?: string }) {
    return <div className={cn("skeleton", className)} />;
}

export default function Dashboard() {
    const [mounted, setMounted] = useState(false);
    const [scans, setScans] = useState<ScanSummary[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setMounted(true);
        let cancelled = false;
        async function load() {
            try {
                const res = await fetch(api.scans);
                if (!res.ok) throw new Error();
                const data = await res.json();
                if (cancelled) return;
                const list: ScanSummary[] = Array.isArray(data) ? data : data.scans ?? [];
                setScans(list);
                if (list.some((s) => s.status === "running" || s.status === "queued")) {
                    setTimeout(load, 3000);
                }
            } catch {
                if (!cancelled) setScans([]);
            } finally {
                if (!cancelled) setLoading(false);
            }
        }
        load();
        return () => {
            cancelled = true;
        };
    }, []);

    if (!mounted) return null;

    const stats = computeStats(scans);
    const recent = scans.slice(0, 6);

    const riskDist = scans.reduce((acc, s) => {
        const cat = s.risk_category ?? "UNKNOWN";
        acc[cat] = (acc[cat] || 0) + 1;
        return acc;
    }, {} as Record<string, number>);
    const riskTotal = Object.values(riskDist).reduce((a, b) => a + b, 0) || 1;

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500 ease-out">
            <div className="flex items-start justify-between">
                <div>
                    <h1 className="text-[22px] font-bold text-slate-900 tracking-tight">Compliance Overview</h1>
                    <p className="text-[13px] text-slate-500 mt-0.5">
                        EU AI Act posture across scanned repositories.
                    </p>
                </div>
                <Link
                    href="/scans/new"
                    className="inline-flex items-center gap-2 px-4 py-2 text-[13px] font-semibold rounded-lg text-white bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-700 hover:to-violet-700 transition-all shadow-sm shadow-indigo-200/50 shrink-0"
                >
                    <ScanSearch className="w-3.5 h-3.5" />
                    New Scan
                </Link>
            </div>

            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                {[
                    {
                        label: "Total Scans",
                        value: stats.total,
                        icon: ShieldCheck,
                        color: "text-indigo-600",
                        bg: "bg-indigo-50",
                        borderColor: "border-indigo-100",
                        trend: stats.completed > 0 ? `${stats.completed} completed` : null,
                    },
                    {
                        label: "In Progress",
                        value: stats.running,
                        icon: Loader2,
                        color: "text-blue-600",
                        bg: "bg-blue-50",
                        borderColor: "border-blue-100",
                        trend: stats.running > 0 ? "Scanning" : "Idle",
                    },
                    {
                        label: "High-Risk Flagged",
                        value: stats.highRisk,
                        icon: AlertTriangle,
                        color: "text-rose-600",
                        bg: "bg-rose-50",
                        borderColor: "border-rose-100",
                        trend: stats.total > 0 ? `${Math.round((stats.highRisk / stats.total) * 100)}% of total` : null,
                    },
                    {
                        label: "Compliant",
                        value: stats.compliant,
                        icon: CheckCircle,
                        color: "text-emerald-600",
                        bg: "bg-emerald-50",
                        borderColor: "border-emerald-100",
                        trend: stats.completed > 0 ? `${Math.round((stats.compliant / Math.max(1, stats.completed)) * 100)}% pass rate` : null,
                    },
                ].map((kpi) => (
                    <div
                        key={kpi.label}
                        className={cn("p-5 bg-white rounded-xl border shadow-sm transition-all hover:shadow-md", kpi.borderColor)}
                    >
                        <div className="flex items-center justify-between mb-3">
                            <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">{kpi.label}</span>
                            <div className={cn("p-1.5 rounded-lg", kpi.bg)}>
                                <kpi.icon className={cn("w-3.5 h-3.5", kpi.color)} />
                            </div>
                        </div>
                        {loading ? (
                            <Skeleton className="h-9 w-16 mb-1" />
                        ) : (
                            <p className={cn("text-3xl font-bold tracking-tight", kpi.color)}>{kpi.value}</p>
                        )}
                        {kpi.trend && !loading && (
                            <p className="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
                                <TrendingUp className="w-3 h-3" />
                                {kpi.trend}
                            </p>
                        )}
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 shadow-sm p-5">
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-[13px] font-semibold text-slate-800">Risk Distribution</h2>
                        <span className="text-[11px] text-slate-400">{scans.length} scans</span>
                    </div>

                    {loading ? (
                        <Skeleton className="h-6 w-full mb-4" />
                    ) : scans.length === 0 ? (
                        <div className="flex items-center justify-center h-16 text-[12px] text-slate-400">
                            No scans to display
                        </div>
                    ) : (
                        <>
                            <div className="flex h-3 rounded-full overflow-hidden bg-slate-100 mb-4">
                                {["MINIMAL_RISK", "LIMITED_RISK", "HIGH_RISK", "PROHIBITED"].map((cat) => {
                                    const count = riskDist[cat] || 0;
                                    if (count === 0) return null;
                                    return (
                                        <div
                                            key={cat}
                                            className={cn("transition-all duration-700", RISK_COLORS[cat])}
                                            style={{ width: `${(count / riskTotal) * 100}%` }}
                                            title={`${cat}: ${count}`}
                                        />
                                    );
                                })}
                            </div>
                            <div className="flex flex-wrap gap-4">
                                {["MINIMAL_RISK", "LIMITED_RISK", "HIGH_RISK", "PROHIBITED"].map((cat) => (
                                    <div key={cat} className="flex items-center gap-1.5">
                                        <span className={cn("w-2.5 h-2.5 rounded-sm", RISK_COLORS[cat])} />
                                        <span className="text-[11px] text-slate-500 font-medium">{cat.replace("_", " ")}</span>
                                        <span className="text-[11px] font-bold text-slate-700">{riskDist[cat] || 0}</span>
                                    </div>
                                ))}
                            </div>
                        </>
                    )}
                </div>

                <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5">
                    <h2 className="text-[13px] font-semibold text-slate-800 mb-3">Platform Modules</h2>
                    <div className="space-y-2.5">
                        {[
                            {
                                name: "Scan Orchestrator",
                                desc: "Static analysis + GraphRAG pipeline",
                                icon: Zap,
                                color: "text-indigo-600",
                                bg: "bg-indigo-50",
                            },
                            {
                                name: "Knowledge Engine",
                                desc: "2,301 nodes / 4,423 relations",
                                icon: Database,
                                color: "text-violet-600",
                                bg: "bg-violet-50",
                            },
                        ].map((mod) => (
                            <div key={mod.name} className="flex items-center gap-3 p-2.5 rounded-lg">
                                <div className={cn("p-2 rounded-lg", mod.bg)}>
                                    <mod.icon className={cn("w-4 h-4", mod.color)} />
                                </div>
                                <div className="flex-1 min-w-0">
                                    <p className="text-[12px] font-semibold text-slate-700">{mod.name}</p>
                                    <p className="text-[11px] text-slate-400">{mod.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                <div className="px-5 py-4 flex justify-between items-center border-b border-slate-100">
                    <h2 className="text-[13px] font-semibold text-slate-800">Recent Scans</h2>
                    <Link
                        href="/scans/new"
                        className="text-[11px] font-semibold text-indigo-600 hover:text-indigo-800 transition-colors flex items-center gap-0.5"
                    >
                        New Scan <ArrowUpRight className="w-3 h-3" />
                    </Link>
                </div>

                {loading ? (
                    <div className="p-5 space-y-3">
                        {[1, 2, 3].map((i) => (
                            <Skeleton key={i} className="h-14 w-full" />
                        ))}
                    </div>
                ) : recent.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-16 text-slate-400">
                        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-50 to-violet-50 border border-indigo-100 flex items-center justify-center mb-4">
                            <ScanSearch className="w-6 h-6 text-indigo-400" />
                        </div>
                        <p className="text-[13px] font-medium text-slate-600 mb-1">No scans yet</p>
                        <p className="text-[12px] text-slate-400 mb-4">Scan a repository for EU AI Act compliance findings</p>
                        <Link
                            href="/scans/new"
                            className="inline-flex items-center gap-1.5 px-4 py-2 text-[12px] font-semibold text-indigo-600 bg-indigo-50 border border-indigo-200 rounded-lg hover:bg-indigo-100 transition-colors"
                        >
                            <ScanSearch className="w-3 h-3" />
                            Run First Scan
                        </Link>
                    </div>
                ) : (
                    <div className="divide-y divide-slate-50">
                        {recent.map((item) => {
                            const statusConfig = STATUS_BADGES[item.status] ?? {
                                label: item.status,
                                classes: "bg-slate-50 text-slate-500 border-slate-200",
                            };
                            const riskCat = item.risk_category;
                            const repoShort = shortenRepo(item.repo_url);
                            return (
                                <Link
                                    key={item.scan_id}
                                    href={`/scans/${item.scan_id}`}
                                    className="px-5 py-3.5 flex items-center gap-4 hover:bg-slate-50/50 transition-colors group"
                                >
                                    <div className="relative shrink-0">
                                        <div className={cn(
                                            "w-9 h-9 rounded-lg flex items-center justify-center",
                                            riskCat === "PROHIBITED" ? "bg-red-50" :
                                            riskCat === "HIGH_RISK" ? "bg-rose-50" :
                                            riskCat === "LIMITED_RISK" ? "bg-amber-50" :
                                            riskCat === "MINIMAL_RISK" ? "bg-emerald-50" :
                                            item.status === "failed" ? "bg-rose-50" :
                                            "bg-slate-50"
                                        )}>
                                            {item.status === "failed" ? <XCircle className="w-4 h-4 text-rose-500" /> :
                                             riskCat === "PROHIBITED" ? <AlertTriangle className="w-4 h-4 text-red-500" /> :
                                             riskCat === "HIGH_RISK" ? <ShieldCheck className="w-4 h-4 text-rose-500" /> :
                                             (item.status === "running" || item.status === "queued") ? <Loader2 className="w-4 h-4 text-blue-500 animate-spin" /> :
                                             <Scale className="w-4 h-4 text-slate-400" />}
                                        </div>
                                    </div>

                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center gap-2">
                                            <p className="text-[13px] font-semibold text-slate-700 group-hover:text-slate-900 transition-colors truncate">
                                                {repoShort}
                                            </p>
                                            {riskCat && (
                                                <span className={cn(
                                                    "text-[9px] font-bold px-1.5 py-0.5 rounded border uppercase",
                                                    RISK_BADGES[riskCat] ?? "bg-slate-50 text-slate-400 border-slate-200"
                                                )}>
                                                    {riskCat.replace("_", " ")}
                                                </span>
                                            )}
                                        </div>
                                        <p className="text-[11px] text-slate-400 mt-0.5 truncate">
                                            <span>{item.ref}</span>
                                            <span> · </span>
                                            <span className="font-mono">{item.scan_id.slice(0, 12)}</span>
                                            {item.finding_count != null && (
                                                <>
                                                    <span> · </span>
                                                    <span>{item.finding_count} findings</span>
                                                </>
                                            )}
                                        </p>
                                    </div>

                                    {item.compliance_score != null && (
                                        <div className="shrink-0 text-right">
                                            <p className="text-[15px] font-bold text-slate-800 tabular-nums">
                                                {Math.round(item.compliance_score)}
                                            </p>
                                            <p className="text-[9px] text-slate-400 uppercase tracking-wider">Score</p>
                                        </div>
                                    )}

                                    <span className={cn(
                                        "text-[10px] font-semibold px-2 py-1 rounded-md border shrink-0",
                                        statusConfig.classes
                                    )}>
                                        {statusConfig.label}
                                    </span>

                                    <ChevronRight className="w-4 h-4 text-slate-300 group-hover:text-slate-500 transition-colors shrink-0" />
                                </Link>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
}

function shortenRepo(url: string): string {
    try {
        const u = new URL(url);
        return `${u.hostname.replace("www.", "")}${u.pathname.replace(/\.git$/, "")}`;
    } catch {
        return url;
    }
}

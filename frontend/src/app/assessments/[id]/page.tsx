"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import {
    ShieldAlert, CheckCircle2, AlertTriangle, XCircle, FileText,
    Loader2, BookOpen, Database, ListChecks, ArrowRight, Scale,
    ChevronDown, ChevronUp, Activity, ClipboardCheck, Building2,
    Server, Copy, Check, Network, DollarSign,
} from "lucide-react";
import { cn } from "@/lib/utils";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

// ── Types ──────────────────────────────────────────────────────────────
type RiskCat = "PROHIBITED" | "HIGH_RISK" | "LIMITED_RISK" | "MINIMAL_RISK";
type Severity = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

interface AssessmentData {
    session_id: string;
    status: string;
    system_description: string | null;
    system_type: string | null;
    company_name: string | null;
    deployment_context: string | null;
    risk_classification: {
        category: RiskCat;
        article: string | null;
        annex: string | null;
        subcategory: string | null;
        reason: string;
        confidence: number;
        requirements: string[];
        action: string | null;
    } | null;
    gdpr_audit: {
        gdpr_compliant: boolean;
        violations: Array<{ article: string; issue: string; severity: Severity; evidence?: string }>;
        warnings: Array<{ article: string; issue: string; severity: Severity }>;
        recommendations: string[];
        lawful_basis: string | null;
        special_category_data: boolean;
        automated_decision_making: boolean;
        dpia_required: boolean;
        data_flows?: {
            data_collected: string[];
            data_sources: string[];
            data_recipients: string[];
            retention_period: string;
            has_special_category_data: boolean;
            special_category_types: string[];
            has_automated_decisions: boolean;
            automated_decision_types: string[];
            data_transfers: string[];
            security_measures_mentioned: string[];
        };
    } | null;
    legal_citations: {
        relevant_articles: Array<{
            regulation: string;
            article_number: string;
            title: string | null;
            text_snippet: string | null;
            relevance_score: number;
            relationship: string | null;
        }>;
        relationship_chains: string[][];
        confidence: number;
        entities_extracted?: any;
    } | null;
    compliance_docs: {
        documents: Array<{
            doc_type: string;
            content: string;
            filename: string;
            format: string;
            generated_at: string;
        }>;
        required_docs: string[];
        generated_count: number;
    } | null;
    final_report: {
        executive_summary: string;
        compliance_score: number;
        gdpr_compliance: {
            compliant: boolean;
            violation_count: number;
            warning_count: number;
            dpia_required: boolean;
        };
        legal_basis: { citations_found: number; confidence: number };
        documents_generated: number;
        recommendations: string[];
        next_steps: string[];
        cost_summary: Record<string, number>;
        assessment_metadata: {
            agents_involved: string[];
            started_at: string;
            completed_at: string;
        };
    } | null;
    errors: string[];
    cost_tracking: Record<string, number>;
    completed_at: string | null;
}

// ── Style maps ─────────────────────────────────────────────────────────
const RISK_BADGE: Record<string, string> = {
    PROHIBITED: "bg-red-50 text-red-600 border-red-200",
    HIGH_RISK: "bg-rose-50 text-rose-600 border-rose-200",
    LIMITED_RISK: "bg-amber-50 text-amber-700 border-amber-200",
    MINIMAL_RISK: "bg-emerald-50 text-emerald-700 border-emerald-200",
};
const SEV_BADGE: Record<string, string> = {
    CRITICAL: "bg-red-50 text-red-600 border-red-200",
    HIGH: "bg-rose-50 text-rose-600 border-rose-200",
    MEDIUM: "bg-amber-50 text-amber-700 border-amber-200",
    LOW: "bg-blue-50 text-blue-600 border-blue-200",
};
const REG_BADGE: Record<string, string> = {
    GDPR: "bg-blue-50 text-blue-700 border-blue-200",
    EU_AI_ACT: "bg-purple-50 text-purple-700 border-purple-200",
};
const DOC_NAMES: Record<string, string> = {
    DPIA: "Data Protection Impact Assessment",
    ROPA: "Record of Processing Activities",
    CONFORMITY_ASSESSMENT: "EU AI Act Conformity Assessment",
    TRANSPARENCY_NOTICE: "AI System Transparency Notice",
};

// ── Pipeline helpers ───────────────────────────────────────────────────
type StepStatus = "done" | "running" | "pending";

const PIPELINE = [
    { label: "Risk Classifier", icon: ShieldAlert },
    { label: "GDPR Auditor", icon: Scale },
    { label: "Legal Research", icon: BookOpen },
    { label: "Doc Generator", icon: FileText },
    { label: "Final Report", icon: ClipboardCheck },
];

function getPipelineStatuses(d: AssessmentData): StepStatus[] {
    const live = d.status === "running";
    const mk = (done: boolean, running: boolean): StepStatus =>
        done ? "done" : running && live ? "running" : "pending";

    const hasRC = !!d.risk_classification;
    const hasGDPR = !!d.gdpr_audit;
    const hasLegal = !!d.legal_citations;
    const hasDocs = !!d.compliance_docs;
    const hasReport = !!d.final_report;

    return [
        mk(hasRC, !hasRC),
        mk(hasGDPR, hasRC && !hasGDPR),
        mk(hasLegal, hasGDPR && !hasLegal),
        mk(hasDocs, hasLegal && !hasDocs),
        mk(hasReport, hasDocs && !hasReport),
    ];
}

// ── Small reusables ────────────────────────────────────────────────────
function Chip({ children, className }: { children: React.ReactNode; className?: string }) {
    return (
        <span className={cn("inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border", className)}>
            {children}
        </span>
    );
}

function SectionHeader({
    icon: Icon,
    title,
    badge,
    iconColor = "text-blue-600",
}: {
    icon: any;
    title: string;
    badge?: React.ReactNode;
    iconColor?: string;
}) {
    return (
        <div className="flex items-center justify-between mb-5">
            <h3 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                <Icon className={cn("w-5 h-5", iconColor)} />
                {title}
            </h3>
            {badge}
        </div>
    );
}

// ── Main Page ──────────────────────────────────────────────────────────
export default function AssessmentResultPage() {
    const { id } = useParams();
    const [data, setData] = useState<AssessmentData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [expandedDocs, setExpandedDocs] = useState<Set<string>>(new Set());
    const [showTech, setShowTech] = useState(false);
    const [copied, setCopied] = useState<string | null>(null);

    useEffect(() => {
        let interval: NodeJS.Timeout;

        const fetch_ = async () => {
            try {
                const res = await fetch(`http://localhost:8000/api/v1/assessments/${id}`);
                if (!res.ok) throw new Error("Assessment not found");
                const json = await res.json();
                setData(json);
                setLoading(false);
                if (["completed", "failed", "awaiting_approval", "rejected"].includes(json.status)) {
                    clearInterval(interval);
                }
            } catch (err: any) {
                setError(err.message);
                setLoading(false);
                clearInterval(interval);
            }
        };

        fetch_();
        interval = setInterval(fetch_, 5000);
        return () => clearInterval(interval);
    }, [id]);

    const handleCopy = (content: string, key: string) => {
        navigator.clipboard.writeText(content);
        setCopied(key);
        setTimeout(() => setCopied(null), 2000);
    };

    const toggleDoc = (key: string) => {
        setExpandedDocs(prev => {
            const next = new Set(prev);
            next.has(key) ? next.delete(key) : next.add(key);
            return next;
        });
    };

    if (loading) return (
        <div className="flex flex-col items-center justify-center h-96 space-y-4">
            <Loader2 className="w-10 h-10 text-indigo-500 animate-spin" />
            <p className="text-slate-400 animate-pulse text-sm">Connecting to compliance pipeline...</p>
        </div>
    );

    if (error) return (
        <div className="p-6 bg-rose-500/10 border border-rose-500/20 rounded-xl">
            <h3 className="text-lg font-medium text-rose-500">Error loading assessment</h3>
            <p className="text-rose-600 mt-1">{error}</p>
        </div>
    );

    if (!data) return null;

    const { status, risk_classification: rc, gdpr_audit: gdpr, legal_citations: legal, compliance_docs: docs, final_report: report, errors, cost_tracking } = data;

    const isCompleted = status === "completed";
    const isRunning = status === "running";
    const needsApproval = status === "awaiting_approval";
    const isFailed = status === "failed";
    const isProhibited = rc?.category === "PROHIBITED";

    const pipelineStatuses = getPipelineStatuses(data);
    const totalCost = Object.values(cost_tracking ?? {}).reduce((a, b) => a + b, 0);

    return (
        <div className="max-w-6xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">

            {/* ── Page Header ── */}
            <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                <div>
                    <div className="flex items-center gap-3 mb-2 flex-wrap">
                        <h1 className="text-3xl font-bold text-slate-900">Assessment Results</h1>
                        <span className={cn(
                            "px-3 py-1 text-xs font-bold rounded-full border uppercase tracking-wide",
                            isRunning ? "bg-blue-50 text-blue-700 border-blue-200 animate-pulse" :
                                isCompleted ? "bg-emerald-50 text-emerald-700 border-emerald-200" :
                                    needsApproval ? "bg-amber-50 text-amber-700 border-amber-200" :
                                        isFailed ? "bg-rose-50 text-rose-600 border-rose-200" :
                                            "bg-slate-100 text-slate-500 border-slate-200"
                        )}>
                            {status.replace(/_/g, " ")}
                        </span>
                    </div>
                    <div className="flex flex-wrap gap-x-4 gap-y-1 text-sm text-slate-400">
                        {data.company_name && (
                            <span className="flex items-center gap-1.5">
                                <Building2 className="w-3.5 h-3.5 text-slate-500" />{data.company_name}
                            </span>
                        )}
                        {data.system_type && (
                            <span className="flex items-center gap-1.5">
                                <Server className="w-3.5 h-3.5 text-slate-500" />{data.system_type}
                            </span>
                        )}
                        {data.deployment_context && (
                            <span className="flex items-center gap-1.5">
                                <ShieldAlert className="w-3.5 h-3.5 text-slate-500" />{data.deployment_context}
                            </span>
                        )}
                        <span className="font-mono text-xs text-slate-600">ID: {String(id).substring(0, 12)}…</span>
                    </div>
                </div>
                {data.completed_at && (
                    <p className="text-xs text-slate-500 shrink-0">
                        Completed {new Date(data.completed_at).toLocaleString()}
                    </p>
                )}
            </div>

            {/* ── Prohibited Alert ── */}
            {isProhibited && (
                <div className="p-5 bg-red-600/10 border border-red-500/40 rounded-xl flex items-start gap-4">
                    <XCircle className="w-6 h-6 text-red-500 shrink-0 mt-0.5" />
                    <div>
                        <p className="text-base font-bold text-red-600">DEPLOYMENT FORBIDDEN — Prohibited AI Practice (Article 5)</p>
                        <p className="text-sm text-red-600/80 mt-1">
                            This system falls under a prohibited category of the EU AI Act. Deployment is legally forbidden in the EU. Immediate redesign and legal consultation are required.
                        </p>
                    </div>
                </div>
            )}

            {/* ── Awaiting Approval Alert ── */}
            {needsApproval && (
                <div className="p-5 bg-amber-500/10 border border-amber-500/30 rounded-xl flex items-start gap-4">
                    <AlertTriangle className="w-6 h-6 text-amber-500 shrink-0 mt-0.5" />
                    <div>
                        <p className="text-base font-bold text-amber-700">Human Review Required</p>
                        <p className="text-sm text-amber-700/80 mt-1">
                            The Supervisor Agent has paused the pipeline and escalated this assessment for mandatory human sign-off. Visit the <strong>Approvals</strong> queue to approve or reject.
                        </p>
                    </div>
                </div>
            )}

            {/* ── Errors / Conflicts ── */}
            {errors?.length > 0 && (
                <div className="p-4 bg-white border border-slate-300 rounded-xl">
                    <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-2">Workflow Notices</p>
                    <ul className="space-y-1">
                        {errors.map((e, i) => (
                            <li key={i} className="text-xs text-slate-400 flex items-start gap-2">
                                <span className="text-amber-700 shrink-0">•</span>{e}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* ── Agent Pipeline Progress ── */}
            <div className="p-5 bg-white border border-slate-200 rounded-xl">
                <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-4">
                    LangGraph Multi-Agent Pipeline
                </p>
                <div className="flex items-center gap-1 flex-wrap">
                    {PIPELINE.map((step, i) => {
                        const s = pipelineStatuses[i];
                        return (
                            <div key={step.label} className="flex items-center gap-1">
                                <div className={cn(
                                    "flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium",
                                    s === "done" ? "bg-emerald-50 text-emerald-700 border-emerald-200" :
                                        s === "running" ? "bg-indigo-50 text-indigo-700 border-indigo-200 animate-pulse" :
                                            "bg-slate-50 text-slate-400 border-slate-200"
                                )}>
                                    {s === "done" ? <CheckCircle2 className="w-3 h-3" /> :
                                        s === "running" ? <Loader2 className="w-3 h-3 animate-spin" /> :
                                            <div className="w-3 h-3 rounded-full border border-slate-200" />}
                                    <step.icon className="w-3 h-3" />
                                    {step.label}
                                </div>
                                {i < PIPELINE.length - 1 && (
                                    <ArrowRight className={cn("w-3 h-3 shrink-0", s === "done" ? "text-emerald-600" : "text-slate-700")} />
                                )}
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* ── 4-Card Stats Row ── */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Compliance Score */}
                <div className="p-5 bg-white border border-slate-200 rounded-xl relative overflow-hidden">
                    <p className="text-xs font-medium text-slate-500 mb-2">Compliance Score</p>
                    {report ? (
                        <>
                            <p className={cn(
                                "text-4xl font-bold tracking-tight",
                                report.compliance_score >= 80 ? "text-emerald-600" :
                                    report.compliance_score >= 50 ? "text-amber-700" : "text-rose-600"
                            )}>
                                {report.compliance_score}
                                <span className="text-lg text-slate-500 font-normal">/100</span>
                            </p>
                            <div
                                className="absolute bottom-0 left-0 h-0.5 transition-all duration-1000"
                                style={{
                                    width: `${report.compliance_score}%`,
                                    background: report.compliance_score >= 80 ? "#10b981" : report.compliance_score >= 50 ? "#f59e0b" : "#f43f5e",
                                }}
                            />
                        </>
                    ) : (
                        <p className="text-slate-600 text-sm mt-2 flex items-center gap-1.5">
                            {isRunning ? <><Loader2 className="w-3 h-3 animate-spin text-slate-500" />Pending</> : "—"}
                        </p>
                    )}
                </div>

                {/* Risk Classification */}
                <div className="p-5 bg-white border border-slate-200 rounded-xl">
                    <p className="text-xs font-medium text-slate-500 mb-2">Risk Classification</p>
                    {rc ? (
                        <div className="space-y-1.5">
                            <Chip className={RISK_BADGE[rc.category] ?? "bg-slate-100 text-slate-500 border-slate-200"}>
                                {rc.category.replace("_", " ")}
                            </Chip>
                            {(rc.annex || rc.article) && (
                                <p className="text-xs text-slate-500">{rc.annex ?? rc.article}</p>
                            )}
                            <p className="text-xs text-slate-600">Confidence {Math.round((rc.confidence ?? 0) * 100)}%</p>
                        </div>
                    ) : (
                        <p className="text-slate-600 text-sm mt-2 flex items-center gap-1.5">
                            {isRunning ? <><Loader2 className="w-3 h-3 animate-spin text-slate-500" />Classifying…</> : "—"}
                        </p>
                    )}
                </div>

                {/* GDPR Status */}
                <div className="p-5 bg-white border border-slate-200 rounded-xl">
                    <p className="text-xs font-medium text-slate-500 mb-2">GDPR Status</p>
                    {gdpr ? (
                        <div className="space-y-1.5">
                            <Chip className={gdpr.gdpr_compliant ? "bg-emerald-500/10 text-emerald-600 border-emerald-500/20" : "bg-amber-500/10 text-amber-700 border-amber-500/20"}>
                                {gdpr.gdpr_compliant ? "Compliant" : "Issues Found"}
                            </Chip>
                            <p className="text-xs text-slate-500">
                                {gdpr.violations.length} violation{gdpr.violations.length !== 1 ? "s" : ""} · {gdpr.warnings?.length ?? 0} warning{(gdpr.warnings?.length ?? 0) !== 1 ? "s" : ""}
                            </p>
                            {gdpr.dpia_required && (
                                <p className="text-xs text-amber-700">⚠ DPIA Required</p>
                            )}
                        </div>
                    ) : (
                        <p className="text-slate-600 text-sm mt-2 flex items-center gap-1.5">
                            {isRunning ? <><Loader2 className="w-3 h-3 animate-spin text-slate-500" />Auditing…</> : "—"}
                        </p>
                    )}
                </div>

                {/* Documents */}
                <div className="p-5 bg-white border border-slate-200 rounded-xl">
                    <p className="text-xs font-medium text-slate-500 mb-2">Documents Generated</p>
                    {docs ? (
                        <div className="space-y-1.5">
                            <p className="text-3xl font-bold text-slate-900">{docs.generated_count}</p>
                            <div className="flex flex-wrap gap-1">
                                {docs.required_docs.map(d => (
                                    <span key={d} className="text-[10px] font-medium px-1.5 py-0.5 bg-indigo-500/10 text-indigo-600 border border-indigo-500/20 rounded">
                                        {d}
                                    </span>
                                ))}
                            </div>
                        </div>
                    ) : (
                        <p className="text-slate-600 text-sm mt-2 flex items-center gap-1.5">
                            {isRunning ? <><Loader2 className="w-3 h-3 animate-spin text-slate-500" />Generating…</> : "—"}
                        </p>
                    )}
                </div>
            </div>

            {/* ── Executive Summary ── */}
            {report?.executive_summary && (
                <div className="p-5 bg-white border border-slate-200 rounded-xl">
                    <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                        <ClipboardCheck className="w-4 h-4 text-blue-600" />
                        Executive Summary
                    </p>
                    <p className="text-sm text-slate-600 leading-relaxed">{report.executive_summary}</p>
                </div>
            )}

            {/* ── System Description ── */}
            {data.system_description && (
                <div className="p-5 bg-white border border-slate-200 rounded-xl">
                    <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                        <FileText className="w-4 h-4 text-slate-400" />
                        System Description
                    </p>
                    <p className="text-sm text-slate-600 leading-relaxed">{data.system_description}</p>
                </div>
            )}

            {/* ── EU AI Act + GDPR Audit (side-by-side) ── */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

                {/* EU AI Act Classification */}
                <div className={cn("p-6 border rounded-xl", rc ? "bg-white border-slate-200" : "bg-white/40 border-slate-200/40 opacity-50")}>
                    <SectionHeader
                        icon={ShieldAlert}
                        title="EU AI Act Classification"
                        badge={rc && (
                            <Chip className={RISK_BADGE[rc.category] ?? "bg-slate-100 text-slate-500 border-slate-200"}>
                                {rc.category.replace("_", " ")}
                            </Chip>
                        )}
                    />
                    {rc ? (
                        <div className="space-y-4">
                            {/* Article / Annex / Action chips */}
                            <div className="flex flex-wrap gap-2">
                                {rc.article && <Chip className="bg-blue-500/10 text-blue-600 border-blue-500/20">{rc.article}</Chip>}
                                {rc.annex && <Chip className="bg-purple-500/10 text-purple-600 border-purple-500/20">{rc.annex}</Chip>}
                                {rc.subcategory && (
                                    <Chip className="bg-slate-100 text-slate-600 border-slate-200">
                                        {rc.subcategory.replace(/_/g, " ")}
                                    </Chip>
                                )}
                                {rc.action && (
                                    <Chip className="bg-indigo-500/10 text-indigo-600 border-indigo-500/20 text-[10px]">
                                        {rc.action.replace(/_/g, " ")}
                                    </Chip>
                                )}
                            </div>

                            {/* Rationale */}
                            <div>
                                <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Classification Rationale</p>
                                <p className="text-sm text-slate-600 leading-relaxed">{rc.reason}</p>
                            </div>

                            {/* Confidence bar */}
                            <div className="flex items-center gap-3">
                                <p className="text-xs text-slate-500 shrink-0">Agent Confidence</p>
                                <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-blue-500 rounded-full transition-all duration-700"
                                        style={{ width: `${(rc.confidence ?? 0) * 100}%` }}
                                    />
                                </div>
                                <p className="text-xs font-medium text-slate-600 shrink-0">{Math.round((rc.confidence ?? 0) * 100)}%</p>
                            </div>

                            {/* Requirements */}
                            {rc.requirements?.length > 0 && (
                                <div className="pt-3 border-t border-slate-200">
                                    <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-1">
                                        <AlertTriangle className="w-3 h-3 text-amber-700" />Legal Requirements
                                    </p>
                                    <ul className="space-y-1.5">
                                        {rc.requirements.map((req, i) => (
                                            <li key={i} className="text-sm text-slate-600 flex items-start gap-2">
                                                <span className="text-rose-600 mt-0.5 shrink-0">•</span>{req}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="flex items-center justify-center h-32 text-slate-500 gap-2 text-sm">
                            {isRunning ? <><Loader2 className="w-4 h-4 animate-spin" />Classifying risk…</> : "Awaiting risk classification…"}
                        </div>
                    )}
                </div>

                {/* GDPR Compliance Audit */}
                <div className={cn("p-6 border rounded-xl", gdpr ? "bg-white border-slate-200" : "bg-white/40 border-slate-200/40 opacity-50")}>
                    <SectionHeader
                        icon={Scale}
                        title="GDPR Compliance Audit"
                        iconColor="text-emerald-600"
                        badge={gdpr && (
                            <Chip className={gdpr.gdpr_compliant ? "bg-emerald-500/10 text-emerald-600 border-emerald-500/20" : "bg-amber-500/10 text-amber-700 border-amber-500/20"}>
                                {gdpr.gdpr_compliant ? "Compliant" : "Issues Found"}
                            </Chip>
                        )}
                    />
                    {gdpr ? (
                        <div className="space-y-4">
                            {/* Flags row */}
                            <div className="flex flex-wrap gap-2">
                                <Chip className={gdpr.dpia_required ? "bg-rose-500/10 text-rose-600 border-rose-500/20" : "bg-slate-100 text-slate-500 border-slate-200"}>
                                    {gdpr.dpia_required ? "⚠ DPIA Required" : "No DPIA Required"}
                                </Chip>
                                <Chip className={gdpr.special_category_data ? "bg-rose-500/10 text-rose-600 border-rose-500/20" : "bg-slate-100 text-slate-500 border-slate-200"}>
                                    {gdpr.special_category_data ? "Special Category Data" : "No Special Category"}
                                </Chip>
                                <Chip className={gdpr.automated_decision_making ? "bg-amber-500/10 text-amber-700 border-amber-500/20" : "bg-slate-100 text-slate-500 border-slate-200"}>
                                    {gdpr.automated_decision_making ? "Art. 22 Applies" : "No Automated Decisions"}
                                </Chip>
                            </div>

                            {/* Lawful basis */}
                            {gdpr.lawful_basis && (
                                <div>
                                    <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Lawful Basis (Art. 6)</p>
                                    <p className="text-sm text-slate-600 capitalize">{gdpr.lawful_basis.replace(/_/g, " ")}</p>
                                </div>
                            )}

                            {/* Violations */}
                            {gdpr.violations.length > 0 ? (
                                <div>
                                    <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-1">
                                        <XCircle className="w-3 h-3 text-rose-600" />Violations ({gdpr.violations.length})
                                    </p>
                                    <div className="space-y-2">
                                        {gdpr.violations.map((v, i) => (
                                            <div key={i} className="p-3 bg-rose-500/5 border border-rose-500/15 rounded-lg">
                                                <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                                                    <span className="text-xs font-bold text-rose-300">{v.article}</span>
                                                    <Chip className={SEV_BADGE[v.severity] ?? "bg-slate-100 text-slate-500 border-slate-200"}>{v.severity}</Chip>
                                                </div>
                                                <p className="text-sm text-slate-600">{v.issue}</p>
                                                {v.evidence && (
                                                    <p className="text-xs text-slate-500 mt-1.5 italic border-t border-slate-200/50 pt-1.5">
                                                        Evidence: "{v.evidence}"
                                                    </p>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ) : (
                                <div className="p-3 bg-emerald-500/5 border border-emerald-500/15 rounded-lg">
                                    <p className="text-sm text-emerald-600 flex items-center gap-2">
                                        <CheckCircle2 className="w-4 h-4" />No GDPR violations detected.
                                    </p>
                                </div>
                            )}

                            {/* Warnings */}
                            {gdpr.warnings?.length > 0 && (
                                <div>
                                    <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-1">
                                        <AlertTriangle className="w-3 h-3 text-amber-700" />Warnings ({gdpr.warnings.length})
                                    </p>
                                    <div className="space-y-2">
                                        {gdpr.warnings.map((w, i) => (
                                            <div key={i} className="p-3 bg-amber-500/5 border border-amber-500/15 rounded-lg">
                                                <div className="flex items-center gap-2 mb-1 flex-wrap">
                                                    <span className="text-xs font-bold text-amber-300">{w.article}</span>
                                                    <Chip className={SEV_BADGE[w.severity] ?? ""}>{w.severity}</Chip>
                                                </div>
                                                <p className="text-sm text-slate-600">{w.issue}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="flex items-center justify-center h-32 text-slate-500 gap-2 text-sm">
                            {isRunning ? <><Loader2 className="w-4 h-4 animate-spin" />Auditing GDPR compliance…</> : "Awaiting GDPR audit…"}
                        </div>
                    )}
                </div>
            </div>

            {/* ── Data Flow Analysis ── */}
            {gdpr?.data_flows && (
                <div className="p-6 bg-white border border-slate-200 rounded-xl">
                    <SectionHeader icon={Database} title="Data Flow Analysis" iconColor="text-purple-600" />
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                        {([
                            { label: "Data Collected", items: gdpr.data_flows.data_collected, color: "text-blue-600 bg-blue-500/5 border-blue-500/15" },
                            { label: "Data Sources", items: gdpr.data_flows.data_sources, color: "text-purple-600 bg-purple-500/5 border-purple-500/15" },
                            { label: "Data Recipients", items: gdpr.data_flows.data_recipients, color: "text-indigo-600 bg-indigo-500/5 border-indigo-500/15" },
                            { label: "Cross-Border Transfers", items: gdpr.data_flows.data_transfers, color: "text-rose-600 bg-rose-500/5 border-rose-500/15" },
                            { label: "Security Measures", items: gdpr.data_flows.security_measures_mentioned, color: "text-emerald-600 bg-emerald-500/5 border-emerald-500/15" },
                            { label: "Special Category Types", items: gdpr.data_flows.special_category_types, color: "text-amber-700 bg-amber-500/5 border-amber-500/15" },
                        ] as const).map(({ label, items, color }) =>
                            (items as string[])?.length > 0 && (
                                <div key={label}>
                                    <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-2">{label}</p>
                                    <div className="flex flex-wrap gap-1.5">
                                        {(items as string[]).map((item, i) => (
                                            <span key={i} className={cn("text-xs px-2 py-0.5 rounded-md border", color)}>{item}</span>
                                        ))}
                                    </div>
                                </div>
                            )
                        )}
                        <div>
                            <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-2">Retention Period</p>
                            <p className="text-sm text-slate-600">{gdpr.data_flows.retention_period || "Not specified"}</p>
                        </div>
                    </div>
                    {gdpr.data_flows.automated_decision_types?.length > 0 && (
                        <div className="mt-5 pt-4 border-t border-slate-200">
                            <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-2">Automated Decision Types (Art. 22)</p>
                            <div className="flex flex-wrap gap-1.5">
                                {gdpr.data_flows.automated_decision_types.map((dt, i) => (
                                    <span key={i} className="text-xs px-2 py-0.5 bg-amber-500/5 border border-amber-500/20 text-amber-700 rounded-md">{dt}</span>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* ── GDPR Recommendations ── */}
            {gdpr?.recommendations && gdpr.recommendations.length > 0 && (
                <div className="p-6 bg-white border border-slate-200 rounded-xl">
                    <SectionHeader icon={ListChecks} title="GDPR Remediation Recommendations" iconColor="text-emerald-600" />
                    <ul className="space-y-2">
                        {gdpr.recommendations.map((rec, i) => (
                            <li key={i} className="flex items-start gap-2 text-sm text-slate-600">
                                <span className="text-blue-600 mt-0.5 shrink-0">→</span>{rec}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* ── Legal Citations & Knowledge Graph ── */}
            {legal && (legal.relevant_articles?.length > 0 || legal.relationship_chains?.length > 0) && (
                <div className="p-6 bg-white border border-slate-200 rounded-xl">
                    <SectionHeader
                        icon={BookOpen}
                        title="Legal Citations & Knowledge Graph"
                        iconColor="text-indigo-600"
                        badge={
                            <div className="flex items-center gap-2">
                                <Chip className="bg-slate-100 text-slate-500 border-slate-200">
                                    {legal.relevant_articles?.length ?? 0} articles
                                </Chip>
                                <Chip className="bg-slate-100 text-slate-500 border-slate-200">
                                    {Math.round(legal.confidence * 100)}% confidence
                                </Chip>
                            </div>
                        }
                    />

                    {/* Article list */}
                    {legal.relevant_articles?.length > 0 && (
                        <div className="space-y-2 mb-6">
                            {legal.relevant_articles.map((art, i) => (
                                <div key={i} className="flex items-start gap-3 p-3 bg-slate-50/50 border border-slate-200 rounded-lg hover:border-slate-300 transition-colors">
                                    <div className="shrink-0 pt-0.5">
                                        <Chip className={REG_BADGE[art.regulation] ?? "bg-slate-100 text-slate-500 border-slate-200"}>
                                            {art.regulation === "EU_AI_ACT" ? "EU AI Act" : art.regulation}
                                        </Chip>
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center gap-2 flex-wrap">
                                            <span className="text-sm font-medium text-slate-900">{art.article_number}</span>
                                            {art.title && <span className="text-sm text-slate-400">— {art.title}</span>}
                                            {art.relationship && (
                                                <Chip className="bg-slate-100 text-slate-500 border-slate-200 text-[10px]">{art.relationship}</Chip>
                                            )}
                                        </div>
                                        {art.text_snippet && (
                                            <p className="text-xs text-slate-500 mt-1 italic line-clamp-2">"{art.text_snippet}"</p>
                                        )}
                                    </div>
                                    <div className="shrink-0 flex items-center gap-1.5 pt-0.5">
                                        <div className="h-1.5 w-16 bg-slate-100 rounded-full overflow-hidden">
                                            <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${art.relevance_score * 100}%` }} />
                                        </div>
                                        <span className="text-[10px] text-slate-500 w-6">{Math.round(art.relevance_score * 100)}%</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Reasoning chains */}
                    {legal.relationship_chains?.length > 0 && (
                        <div className="pt-4 border-t border-slate-200">
                            <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                                <Network className="w-3.5 h-3.5" />Multi-hop Reasoning Chains
                            </p>
                            <div className="space-y-2">
                                {legal.relationship_chains.map((chain, i) => (
                                    <div key={i} className="flex items-center gap-1 flex-wrap p-2.5 bg-slate-50/50 rounded-lg border border-slate-200">
                                        {chain.map((node, j) => (
                                            <span key={j} className={cn(
                                                "text-xs px-1.5 py-0.5 rounded",
                                                node.startsWith("→") ? "text-slate-500" : "font-medium text-slate-200 bg-slate-100"
                                            )}>
                                                {node}
                                            </span>
                                        ))}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* ── Generated Compliance Documents ── */}
            {docs?.documents && docs.documents.length > 0 && (
                <div className="p-6 bg-white border border-slate-200 rounded-xl">
                    <SectionHeader icon={FileText} title="Generated Compliance Documents" iconColor="text-amber-700" />
                    <div className="space-y-3">
                        {docs.documents.map((doc, i) => (
                            <div key={i} className="border border-slate-200 rounded-lg overflow-hidden">
                                <div className="flex items-center justify-between px-4 py-3 bg-slate-50/40">
                                    <div className="flex items-center gap-3 min-w-0">
                                        <Chip className="bg-indigo-500/10 text-indigo-600 border-indigo-500/20 shrink-0">
                                            {doc.doc_type}
                                        </Chip>
                                        <span className="text-sm text-slate-600 truncate">
                                            {DOC_NAMES[doc.doc_type] ?? doc.doc_type}
                                        </span>
                                        <span className="text-xs text-slate-600 font-mono hidden lg:block shrink-0">{doc.filename}</span>
                                    </div>
                                    <div className="flex items-center gap-2 shrink-0 ml-3">
                                        <button
                                            onClick={() => handleCopy(doc.content, doc.doc_type)}
                                            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-400 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-lg border border-slate-200 transition-colors"
                                        >
                                            {copied === doc.doc_type
                                                ? <><Check className="w-3 h-3 text-emerald-600" />Copied</>
                                                : <><Copy className="w-3 h-3" />Copy</>}
                                        </button>
                                        <button
                                            onClick={() => toggleDoc(doc.doc_type)}
                                            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-400 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-lg border border-slate-200 transition-colors"
                                        >
                                            {expandedDocs.has(doc.doc_type)
                                                ? <><ChevronUp className="w-3 h-3" />Hide</>
                                                : <><ChevronDown className="w-3 h-3" />View</>}
                                        </button>
                                    </div>
                                </div>
                                {expandedDocs.has(doc.doc_type) && (
                                    <div className="border-t border-slate-200 p-5 max-h-[560px] overflow-y-auto bg-slate-50">
                                        <ReactMarkdown
                                            remarkPlugins={[remarkGfm]}
                                            components={{
                                                h1: ({ node, className, children, ...props }) => <h1 className={cn("text-base font-bold text-slate-900 mt-5 mb-2 pb-2 border-b border-slate-200", className)} {...props}>{children}</h1>,
                                                h2: ({ node, className, children, ...props }) => <h2 className={cn("text-sm font-semibold text-indigo-700 mt-4 mb-1.5 pb-1 border-b border-indigo-100", className)} {...props}>{children}</h2>,
                                                h3: ({ node, className, children, ...props }) => <h3 className={cn("text-sm font-semibold text-slate-700 mt-3 mb-1", className)} {...props}>{children}</h3>,
                                                h4: ({ node, className, children, ...props }) => <h4 className={cn("text-xs font-semibold text-slate-600 mt-2 mb-1 uppercase tracking-wide", className)} {...props}>{children}</h4>,
                                                p: ({ node, className, children, ...props }) => <p className={cn("text-sm text-slate-600 mb-2.5 leading-relaxed", className)} {...props}>{children}</p>,
                                                ul: ({ node, className, children, ...props }) => <ul className={cn("list-disc list-inside mb-2.5 space-y-1", className)} {...props}>{children}</ul>,
                                                ol: ({ node, className, children, ...props }) => <ol className={cn("list-decimal list-inside mb-2.5 space-y-1", className)} {...props}>{children}</ol>,
                                                li: ({ node, className, children, ...props }) => <li className={cn("text-sm text-slate-600 leading-relaxed pl-1", className)} {...props}>{children}</li>,
                                                strong: ({ node, className, children, ...props }) => <strong className={cn("font-semibold text-slate-800", className)} {...props}>{children}</strong>,
                                                em: ({ node, className, children, ...props }) => <em className={cn("italic text-slate-500", className)} {...props}>{children}</em>,
                                                code: ({ node, className, children, ...props }) => {
                                                    const isBlock = node?.position?.start?.column === 1 || className?.includes('language');
                                                    return <code className={cn(
                                                        "font-mono rounded",
                                                        isBlock ? "text-slate-700 text-xs" : "text-[11px] bg-indigo-50 text-indigo-700 border border-indigo-100 px-1 py-0.5",
                                                        className
                                                    )} {...props}>{children}</code>;
                                                },
                                                pre: ({ node, className, children, ...props }) => <pre className={cn("bg-white border border-slate-200 rounded-lg p-4 overflow-x-auto mb-3 text-xs font-mono text-slate-700", className)} {...props}>{children}</pre>,
                                                blockquote: ({ node, className, children, ...props }) => <blockquote className={cn("border-l-4 border-indigo-400 pl-4 py-1 my-2 bg-indigo-50 rounded-r text-sm text-slate-600 italic", className)} {...props}>{children}</blockquote>,
                                                hr: ({ node, className, ...props }) => <hr className={cn("border-slate-200 my-3", className)} {...props} />,
                                                table: ({ node, className, children, ...props }) => <div className="overflow-x-auto mb-3"><table className={cn("w-full text-sm border-collapse", className)} {...props}>{children}</table></div>,
                                                thead: ({ node, className, children, ...props }) => <thead className={cn("bg-indigo-50", className)} {...props}>{children}</thead>,
                                                th: ({ node, className, children, ...props }) => <th className={cn("text-left text-xs font-semibold text-indigo-700 uppercase tracking-wide px-3 py-2 border border-indigo-100", className)} {...props}>{children}</th>,
                                                td: ({ node, className, children, ...props }) => <td className={cn("text-sm text-slate-600 px-3 py-2 border border-slate-200 align-top", className)} {...props}>{children}</td>,
                                                tr: ({ node, className, children, ...props }) => <tr className={cn("even:bg-slate-50", className)} {...props}>{children}</tr>,
                                                a: ({ node, className, children, ...props }) => <a className={cn("text-indigo-600 hover:text-indigo-800 underline underline-offset-2", className)} {...props}>{children}</a>,
                                            }}
                                        >
                                            {doc.content}
                                        </ReactMarkdown>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* ── Action Plan: Recommendations + Next Steps ── */}
            {(report?.recommendations?.length || report?.next_steps?.length) && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {report?.recommendations && report.recommendations.length > 0 && (
                        <div className="p-6 bg-white border border-slate-200 rounded-xl">
                            <SectionHeader icon={ListChecks} title="Recommendations" iconColor="text-blue-600" />
                            <ul className="space-y-2.5">
                                {report.recommendations.map((rec, i) => (
                                    <li key={i} className="flex items-start gap-2.5 text-sm text-slate-600">
                                        <CheckCircle2 className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
                                        {rec}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                    {report?.next_steps && report.next_steps.length > 0 && (
                        <div className="p-6 bg-white border border-slate-200 rounded-xl">
                            <SectionHeader icon={ArrowRight} title="Next Steps" iconColor="text-emerald-600" />
                            <ol className="space-y-2.5">
                                {report.next_steps.map((step, i) => (
                                    <li key={i} className="flex items-start gap-3 text-sm text-slate-600">
                                        <span className="shrink-0 w-5 h-5 rounded-full bg-blue-500/20 text-blue-600 text-xs font-bold flex items-center justify-center mt-0.5">
                                            {i + 1}
                                        </span>
                                        {step}
                                    </li>
                                ))}
                            </ol>
                        </div>
                    )}
                </div>
            )}

            {/* ── Technical Details (collapsible) ── */}
            <div className="border border-slate-200 rounded-xl overflow-hidden">
                <button
                    onClick={() => setShowTech(v => !v)}
                    className="w-full flex items-center justify-between px-6 py-4 bg-white hover:bg-slate-100/50 transition-colors"
                >
                    <span className="flex items-center gap-2 text-sm font-medium text-slate-400">
                        <Activity className="w-4 h-4 text-slate-500" />
                        Technical Details — Agent Costs, Confidence Scores & Metadata
                    </span>
                    {showTech ? <ChevronUp className="w-4 h-4 text-slate-500" /> : <ChevronDown className="w-4 h-4 text-slate-500" />}
                </button>

                {showTech && (
                    <div className="px-6 pb-6 pt-4 bg-white border-t border-slate-200 space-y-6">

                        {/* Agent Costs */}
                        {cost_tracking && Object.keys(cost_tracking).length > 0 && (
                            <div>
                                <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                                    <DollarSign className="w-3.5 h-3.5" />Agent API Costs (USD)
                                </p>
                                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
                                    {Object.entries(cost_tracking).map(([agent, cost]) => (
                                        <div key={agent} className="p-3 bg-slate-50/50 border border-slate-200 rounded-lg">
                                            <p className="text-xs text-slate-500 capitalize mb-1">{agent.replace(/_/g, " ")}</p>
                                            <p className="text-sm font-mono font-medium text-slate-200">${(cost as number).toFixed(4)}</p>
                                        </div>
                                    ))}
                                    <div className="p-3 bg-slate-50/50 border border-blue-500/20 rounded-lg">
                                        <p className="text-xs text-slate-500 mb-1">Total</p>
                                        <p className="text-sm font-mono font-bold text-blue-600">${totalCost.toFixed(4)}</p>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Assessment Metadata */}
                        {report?.assessment_metadata && (
                            <div>
                                <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-3">Assessment Metadata</p>
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
                                    <div>
                                        <p className="text-xs text-slate-500 mb-1">Session ID</p>
                                        <p className="font-mono text-slate-600 text-xs">{data.session_id}</p>
                                    </div>
                                    <div>
                                        <p className="text-xs text-slate-500 mb-1">Agents Involved</p>
                                        <div className="flex flex-wrap gap-1">
                                            {report.assessment_metadata.agents_involved.map(a => (
                                                <span key={a} className="text-[10px] px-1.5 py-0.5 bg-slate-100 text-slate-400 border border-slate-300 rounded">
                                                    {a.replace(/_/g, " ")}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                    {report.assessment_metadata.started_at && (
                                        <div>
                                            <p className="text-xs text-slate-500 mb-1">Started At</p>
                                            <p className="text-slate-600 text-xs">{new Date(report.assessment_metadata.started_at).toLocaleString()}</p>
                                        </div>
                                    )}
                                    {data.completed_at && (
                                        <div>
                                            <p className="text-xs text-slate-500 mb-1">Completed At</p>
                                            <p className="text-slate-600 text-xs">{new Date(data.completed_at).toLocaleString()}</p>
                                        </div>
                                    )}
                                    {report.legal_basis && (
                                        <div>
                                            <p className="text-xs text-slate-500 mb-1">Legal Citations Found</p>
                                            <p className="text-slate-600 text-xs">
                                                {report.legal_basis.citations_found} articles · {Math.round(report.legal_basis.confidence * 100)}% confidence
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ShieldAlert, AlertTriangle, CheckCircle, Clock, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

type Assessment = {
  session_id: string;
  system_type?: string;
  status: string;
  risk_classification?: { category: string };
  gdpr_audit?: { gdpr_compliant: boolean; violations?: any[] };
};

function computeStats(assessments: Assessment[]) {
  const total = assessments.length;
  const pending = assessments.filter((a) => a.status === "awaiting_approval").length;
  const highRisk = assessments.filter(
    (a) => a.risk_classification?.category === "HIGH_RISK" || a.risk_classification?.category === "PROHIBITED"
  ).length;
  const compliant = assessments.filter(
    (a) =>
      a.status === "completed" &&
      a.gdpr_audit?.gdpr_compliant === true &&
      a.risk_classification?.category !== "HIGH_RISK" &&
      a.risk_classification?.category !== "PROHIBITED"
  ).length;
  return { total, pending, highRisk, compliant };
}

function statusLabel(status: string) {
  if (status === "completed") return "Compliant";
  if (status === "awaiting_approval") return "Pending Review";
  if (status === "running") return "Running";
  if (status === "failed") return "Failed";
  return status;
}

const STAT_CONFIG = [
  { name: "Total Assessments", key: "total" as const, icon: ShieldAlert, color: "text-indigo-600", bg: "bg-indigo-50", border: "border-indigo-200", iconBg: "bg-indigo-600" },
  { name: "Pending Human Review", key: "pending" as const, icon: Clock, color: "text-amber-700", bg: "bg-amber-50", border: "border-amber-200", iconBg: "bg-amber-500" },
  { name: "High-Risk Systems", key: "highRisk" as const, icon: AlertTriangle, color: "text-rose-600", bg: "bg-rose-50", border: "border-rose-200", iconBg: "bg-rose-500" },
  { name: "Fully Compliant", key: "compliant" as const, icon: CheckCircle, color: "text-emerald-700", bg: "bg-emerald-50", border: "border-emerald-200", iconBg: "bg-emerald-500" },
];

export default function Dashboard() {
  const [mounted, setMounted] = useState(false);
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setMounted(true);
    fetch("http://localhost:8000/api/v1/assessments")
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then((data) => setAssessments(Array.isArray(data) ? data : data.assessments ?? []))
      .catch(() => setAssessments([]))
      .finally(() => setLoading(false));
  }, []);

  if (!mounted) return null;

  const stats = computeStats(assessments);
  const recent = assessments.slice(0, 5);

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500 ease-out">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 mb-1">Compliance Overview</h1>
          <p className="text-sm text-slate-500">Monitor EU AI Act & GDPR compliance across your AI systems.</p>
        </div>
        <Link
          href="/assessments/new"
          className="inline-flex items-center justify-center px-4 py-2.5 text-sm font-semibold rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 transition-colors shadow-sm shrink-0"
        >
          <ShieldAlert className="w-4 h-4 mr-2" />
          Run New Assessment
        </Link>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {STAT_CONFIG.map((s) => {
          const value = loading ? "—" : String(stats[s.key]);
          return (
            <div key={s.name} className={cn("p-5 bg-white rounded-xl border shadow-sm", s.border)}>
              <div className="flex items-center justify-between mb-3">
                <p className="text-xs font-medium text-slate-500">{s.name}</p>
                <div className={cn("p-2 rounded-lg", s.bg)}>
                  <s.icon className={cn("w-4 h-4", s.color)} />
                </div>
              </div>
              <p className={cn("text-3xl font-bold tracking-tight", s.color)}>{value}</p>
            </div>
          );
        })}
      </div>

      {/* Recent Assessments */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="px-6 py-4 flex justify-between items-center border-b border-slate-100">
          <h2 className="text-sm font-semibold text-slate-900">Recent Assessments</h2>
          <Link href="/assessments/new" className="text-xs font-medium text-indigo-600 hover:text-indigo-800 transition-colors">
            + New Assessment →
          </Link>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-48">
            <Loader2 className="w-7 h-7 text-indigo-500 animate-spin" />
          </div>
        ) : recent.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-48 text-slate-400">
            <div className="w-12 h-12 rounded-full bg-indigo-50 border border-indigo-100 flex items-center justify-center mb-3">
              <ShieldAlert className="w-5 h-5 text-indigo-400" />
            </div>
            <p className="text-sm text-slate-500">No assessments yet.</p>
            <Link href="/assessments/new" className="mt-2 text-sm text-indigo-600 hover:text-indigo-800 transition-colors">
              Run your first assessment →
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {recent.map((item) => {
              const label = statusLabel(item.status);
              const badge =
                label === "Compliant" ? "bg-emerald-50 text-emerald-700 border-emerald-200" :
                label === "Running" ? "bg-blue-50 text-blue-700 border-blue-200" :
                label === "Failed" ? "bg-rose-50 text-rose-700 border-rose-200" :
                "bg-amber-50 text-amber-700 border-amber-200";
              return (
                <Link
                  key={item.session_id}
                  href={`/assessments/${item.session_id}`}
                  className="px-6 py-4 flex items-center justify-between hover:bg-slate-50 transition-colors group"
                >
                  <div className="flex items-center space-x-4">
                    <div className="w-9 h-9 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center shrink-0">
                      <span className="text-xs font-bold text-indigo-600">
                        {item.session_id.substring(0, 2).toUpperCase()}
                      </span>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">
                        {item.system_type || "Unknown System"}
                      </p>
                      <p className="text-xs text-slate-400 mt-0.5 font-mono">{item.session_id.substring(0, 8)}…</p>
                    </div>
                  </div>
                  <span className={cn("text-xs font-semibold px-2.5 py-1 rounded-full border", badge)}>
                    {label}
                  </span>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

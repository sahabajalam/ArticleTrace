"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { UserCheck, ShieldAlert, CheckCircle2, XCircle, Clock } from "lucide-react";

export default function ApprovalsPage() {
    const [approvals, setApprovals] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchApprovals = async () => {
        try {
            const res = await fetch("http://localhost:8000/api/v1/approvals");
            if (res.ok) {
                const data = await res.json();
                setApprovals(data.pending_approvals || []);
            }
        } catch (e) {
            console.error("Failed to fetch approvals", e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchApprovals(); }, []);

    const handleDecision = async (id: string, decision: "approved" | "rejected") => {
        try {
            await fetch(`http://localhost:8000/api/v1/approvals/${id}/decide`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ decision, reviewer_id: "admin_user", notes: `Manually ${decision} via dashboard.` }),
            });
            fetchApprovals();
        } catch (e) {
            alert("Failed to submit decision");
        }
    };

    return (
        <div className="max-w-5xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div>
                <h1 className="text-2xl font-bold text-slate-900 mb-1">Human Review Queue</h1>
                <p className="text-sm text-slate-500">Assessments paused by the Supervisor Agent requiring manual sign-off.</p>
            </div>

            <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden min-h-[420px]">
                <div className="px-6 py-4 flex items-center border-b border-slate-100">
                    <h2 className="text-sm font-semibold text-slate-900 flex items-center gap-2">
                        <Clock className="w-4 h-4 text-amber-500" />
                        Pending Approvals
                    </h2>
                    <span className="ml-2 px-2 py-0.5 text-xs font-semibold rounded-full bg-amber-50 text-amber-700 border border-amber-200">
                        {approvals.length}
                    </span>
                </div>

                {loading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="w-7 h-7 rounded-full border-2 border-slate-200 border-t-indigo-600 animate-spin" />
                    </div>
                ) : approvals.length === 0 ? (
                    <div className="flex flex-col justify-center items-center h-64 text-slate-400">
                        <div className="w-14 h-14 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center mb-3">
                            <UserCheck className="w-6 h-6 text-emerald-500" />
                        </div>
                        <p className="text-sm font-medium text-slate-600">All clear!</p>
                        <p className="text-xs text-slate-400 mt-1">No assessments currently require human review.</p>
                    </div>
                ) : (
                    <div className="divide-y divide-slate-100">
                        {approvals.map((req) => (
                            <div key={req.id} className="p-6 flex flex-col md:flex-row md:items-center justify-between gap-6 hover:bg-slate-50 transition-colors">
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center flex-wrap gap-2 mb-2">
                                        <span className="font-mono text-xs px-2 py-1 rounded bg-slate-100 text-slate-500 border border-slate-200">
                                            ID: {req.id?.substring(0, 8) ?? "—"}…
                                        </span>
                                        <span className="text-xs font-semibold px-2 py-0.5 rounded bg-rose-50 text-rose-600 border border-rose-200 flex items-center gap-1">
                                            <ShieldAlert className="w-3 h-3" /> High-Risk Flag
                                        </span>
                                    </div>
                                    <h3 className="text-sm font-semibold text-slate-800 mb-1">
                                        System requires conformity assessment approval
                                    </h3>
                                    <p className="text-xs text-slate-400">
                                        Created: {new Date(req.created_at).toLocaleString()}
                                    </p>
                                </div>
                                <div className="flex items-center gap-2 shrink-0">
                                    <Link href={`/assessments/${req.assessment_id}`} className="px-3 py-2 text-xs font-medium text-slate-500 hover:text-slate-800 transition-colors">
                                        View Details
                                    </Link>
                                    <button
                                        onClick={() => handleDecision(req.id, "rejected")}
                                        className="flex items-center px-4 py-2 text-xs font-semibold rounded-lg bg-white text-rose-600 border border-rose-200 hover:bg-rose-50 transition-colors"
                                    >
                                        <XCircle className="w-3.5 h-3.5 mr-1.5" /> Reject
                                    </button>
                                    <button
                                        onClick={() => handleDecision(req.id, "approved")}
                                        className="flex items-center px-4 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 transition-colors shadow-sm"
                                    >
                                        <CheckCircle2 className="w-3.5 h-3.5 mr-1.5" /> Approve
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

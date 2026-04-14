"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ScanSearch, GitBranch, Sparkles, AlertCircle, Loader2 } from "lucide-react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

const SAMPLE_REPOS = [
    { label: "FastAPI demo", url: "https://github.com/tiangolo/full-stack-fastapi-template", ref: "master" },
    { label: "LangChain examples", url: "https://github.com/langchain-ai/langchain", ref: "master" },
    { label: "HuggingFace transformers", url: "https://github.com/huggingface/transformers", ref: "main" },
];

export default function NewScanPage() {
    const router = useRouter();
    const [repoUrl, setRepoUrl] = useState("");
    const [ref, setRef] = useState("main");
    const [enrichWithKg, setEnrichWithKg] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        setError(null);
        setSubmitting(true);
        try {
            const res = await fetch(api.scans, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    repo_url: repoUrl.trim(),
                    ref: ref.trim() || "main",
                    enrich_with_kg: enrichWithKg,
                }),
            });
            if (!res.ok) {
                const body = await res.json().catch(() => ({}));
                throw new Error(body.detail ?? `Scan creation failed (${res.status})`);
            }
            const data = await res.json();
            router.push(`/scans/${data.scan_id}`);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Unknown error");
            setSubmitting(false);
        }
    }

    return (
        <div className="max-w-3xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div>
                <h1 className="text-[22px] font-bold text-slate-900 tracking-tight">New Compliance Scan</h1>
                <p className="text-[13px] text-slate-500 mt-0.5">
                    Static analysis of a Git repository against the EU AI Act. Findings are anchored to file:line evidence and mapped to articles.
                </p>
            </div>

            <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-5">
                <div className="space-y-1.5">
                    <label className="text-[12px] font-semibold text-slate-700 flex items-center gap-1.5">
                        <ScanSearch className="w-3.5 h-3.5 text-indigo-600" /> Repository URL
                    </label>
                    <input
                        type="url"
                        required
                        placeholder="https://github.com/org/repo"
                        value={repoUrl}
                        onChange={(e) => setRepoUrl(e.target.value)}
                        className="w-full px-3.5 py-2.5 text-[13px] rounded-lg border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
                    />
                    <p className="text-[11px] text-slate-400">Public HTTPS Git URL. Private repos need backend credentials.</p>
                </div>

                <div className="space-y-1.5">
                    <label className="text-[12px] font-semibold text-slate-700 flex items-center gap-1.5">
                        <GitBranch className="w-3.5 h-3.5 text-indigo-600" /> Ref
                    </label>
                    <input
                        type="text"
                        value={ref}
                        onChange={(e) => setRef(e.target.value)}
                        placeholder="main"
                        className="w-full px-3.5 py-2.5 text-[13px] rounded-lg border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
                    />
                    <p className="text-[11px] text-slate-400">Branch, tag, or commit SHA.</p>
                </div>

                <label className="flex items-start gap-3 p-3 rounded-lg border border-slate-200 cursor-pointer hover:bg-slate-50 transition-colors">
                    <input
                        type="checkbox"
                        checked={enrichWithKg}
                        onChange={(e) => setEnrichWithKg(e.target.checked)}
                        className="mt-0.5 accent-indigo-600"
                    />
                    <div>
                        <p className="text-[12px] font-semibold text-slate-700 flex items-center gap-1.5">
                            <Sparkles className="w-3.5 h-3.5 text-violet-500" /> Enrich with Knowledge Graph
                        </p>
                        <p className="text-[11px] text-slate-400 mt-0.5">
                            Cross-reference findings against 2,301 legal nodes and attach article citations + reasoning chains.
                        </p>
                    </div>
                </label>

                <div className="space-y-2">
                    <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Sample repositories</p>
                    <div className="flex flex-wrap gap-2">
                        {SAMPLE_REPOS.map((r) => (
                            <button
                                key={r.url}
                                type="button"
                                onClick={() => {
                                    setRepoUrl(r.url);
                                    setRef(r.ref);
                                }}
                                className="text-[11px] font-medium px-2.5 py-1 rounded-md border border-slate-200 text-slate-600 hover:border-indigo-300 hover:text-indigo-600 hover:bg-indigo-50 transition-all"
                            >
                                {r.label}
                            </button>
                        ))}
                    </div>
                </div>

                {error && (
                    <div className="flex items-start gap-2 p-3 rounded-lg bg-rose-50 border border-rose-200">
                        <AlertCircle className="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />
                        <p className="text-[12px] text-rose-700">{error}</p>
                    </div>
                )}

                <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                    <button
                        type="button"
                        onClick={() => router.push("/")}
                        className="px-4 py-2 text-[13px] font-semibold rounded-lg text-slate-600 hover:bg-slate-100 transition-colors"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        disabled={submitting || !repoUrl.trim()}
                        className={cn(
                            "inline-flex items-center gap-2 px-4 py-2 text-[13px] font-semibold rounded-lg text-white transition-all shadow-sm shadow-indigo-200/50",
                            submitting || !repoUrl.trim()
                                ? "bg-slate-300 cursor-not-allowed"
                                : "bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-700 hover:to-violet-700"
                        )}
                    >
                        {submitting ? (
                            <>
                                <Loader2 className="w-3.5 h-3.5 animate-spin" /> Queuing scan…
                            </>
                        ) : (
                            <>
                                <ScanSearch className="w-3.5 h-3.5" /> Start Scan
                            </>
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
}

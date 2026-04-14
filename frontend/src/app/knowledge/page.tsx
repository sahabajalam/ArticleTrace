"use client";

import {
    Database, FileText, Scale, BookOpen, Gavel, Shield,
    Users, AlertTriangle, Network, Layers, ChevronRight,
    Search, ExternalLink,
} from "lucide-react";
import { cn } from "@/lib/utils";

// Static data reflecting actual Neo4j content
const ENTITY_TYPES = [
    { type: "Obligation", count: 1325, icon: Gavel, color: "text-red-600", bg: "bg-red-50", border: "border-red-100", desc: "Legal requirements extracted from articles" },
    { type: "Recital", count: 353, icon: BookOpen, color: "text-blue-600", bg: "bg-blue-50", border: "border-blue-100", desc: "Interpretive context for articles" },
    { type: "Article", count: 212, icon: FileText, color: "text-indigo-600", bg: "bg-indigo-50", border: "border-indigo-100", desc: "GDPR + EU AI Act provisions" },
    { type: "Exemption", count: 96, icon: Shield, color: "text-emerald-600", bg: "bg-emerald-50", border: "border-emerald-100", desc: "Exception pathways with conditions" },
    { type: "Definition", count: 90, icon: Scale, color: "text-violet-600", bg: "bg-violet-50", border: "border-violet-100", desc: "Legal term definitions" },
    { type: "Concept", count: 47, icon: Layers, color: "text-amber-600", bg: "bg-amber-50", border: "border-amber-100", desc: "Abstract regulatory concepts" },
    { type: "Chapter", count: 24, icon: Layers, color: "text-slate-600", bg: "bg-slate-50", border: "border-slate-100", desc: "Structural groupings" },
    { type: "Guideline", count: 21, icon: BookOpen, color: "text-teal-600", bg: "bg-teal-50", border: "border-teal-100", desc: "EDPB/WP29 guidance" },
    { type: "CaseLaw", count: 20, icon: Gavel, color: "text-orange-600", bg: "bg-orange-50", border: "border-orange-100", desc: "CJEU landmark decisions" },
    { type: "AISystemType", count: 19, icon: Network, color: "text-cyan-600", bg: "bg-cyan-50", border: "border-cyan-100", desc: "AI system classifications" },
    { type: "Right", count: 19, icon: Users, color: "text-pink-600", bg: "bg-pink-50", border: "border-pink-100", desc: "Data subject rights" },
    { type: "Actor", count: 18, icon: Users, color: "text-slate-600", bg: "bg-slate-50", border: "border-slate-100", desc: "Legal roles & actors" },
    { type: "DataType", count: 17, icon: Database, color: "text-purple-600", bg: "bg-purple-50", border: "border-purple-100", desc: "Data classifications" },
    { type: "EnforcementAction", count: 15, icon: AlertTriangle, color: "text-rose-600", bg: "bg-rose-50", border: "border-rose-100", desc: "Major DPA enforcement cases" },
    { type: "Annex", count: 13, icon: FileText, color: "text-blue-600", bg: "bg-blue-50", border: "border-blue-100", desc: "Technical annexes" },
    { type: "Penalty", count: 6, icon: AlertTriangle, color: "text-red-600", bg: "bg-red-50", border: "border-red-100", desc: "Fine tiers & sanctions" },
    { type: "RiskCategory", count: 4, icon: Shield, color: "text-amber-600", bg: "bg-amber-50", border: "border-amber-100", desc: "Prohibited / High / Limited / Minimal" },
    { type: "Regulation", count: 2, icon: Scale, color: "text-indigo-600", bg: "bg-indigo-50", border: "border-indigo-100", desc: "GDPR & EU AI Act" },
];

const RELATIONSHIPS = [
    { type: "REQUIRES", count: 1008, desc: "Creates obligation" },
    { type: "APPLIES_TO", count: 939, desc: "Affects which actors" },
    { type: "CONTAINS", count: 602, desc: "Parent-child structure" },
    { type: "REFERENCES", count: 587, desc: "Cross-references" },
    { type: "INTERPRETS", count: 303, desc: "Recital/guideline interprets" },
    { type: "PART_OF", count: 270, desc: "Child belongs to parent" },
    { type: "PERMITS", count: 232, desc: "Allows activity" },
    { type: "EXEMPTS", count: 96, desc: "Provides exception" },
    { type: "DEFINES", count: 90, desc: "Definition provision" },
    { type: "CITES", count: 85, desc: "Case/enforcement cites" },
    { type: "PROHIBITS", count: 85, desc: "Forbids activity" },
    { type: "COMPLEMENTS", count: 76, desc: "Cross-regulation link" },
    { type: "ENFORCES", count: 50, desc: "Authority enforces" },
];

const VECTOR_COLLECTIONS = [
    { name: "obligations", count: 1421, desc: "Obligations + exemptions" },
    { name: "recitals", count: 353, desc: "GDPR + AI Act recitals" },
    { name: "articles", count: 212, desc: "Full article text" },
    { name: "definitions", count: 90, desc: "Legal definitions" },
    { name: "interpretive", count: 56, desc: "Guidelines, case law, enforcement" },
    { name: "concepts", count: 47, desc: "Regulatory concepts" },
    { name: "rights", count: 19, desc: "Data subject rights" },
];

const TOTAL_NODES = 2301;
const TOTAL_RELS = 4423;
const TOTAL_VECTORS = 2198;

export default function KnowledgePage() {
    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500 ease-out">
            {/* Header */}
            <div>
                <h1 className="text-[22px] font-bold text-slate-900 tracking-tight">Knowledge Graph</h1>
                <p className="text-[13px] text-slate-500 mt-0.5">
                    Legal knowledge infrastructure powering multi-hop compliance reasoning.
                </p>
            </div>

            {/* Summary Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {[
                    {
                        label: "Neo4j Graph Nodes",
                        value: TOTAL_NODES.toLocaleString(),
                        sub: "18 entity types",
                        icon: Database,
                        gradient: "from-violet-500 to-purple-600",
                    },
                    {
                        label: "Graph Relationships",
                        value: TOTAL_RELS.toLocaleString(),
                        sub: "13 relationship types",
                        icon: Network,
                        gradient: "from-indigo-500 to-blue-600",
                    },
                    {
                        label: "Vector Embeddings",
                        value: TOTAL_VECTORS.toLocaleString(),
                        sub: "7 collections with Gemini embeddings",
                        icon: Search,
                        gradient: "from-emerald-500 to-teal-600",
                    },
                ].map((stat) => (
                    <div key={stat.label} className="relative p-5 bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                        <div className={cn("absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r", stat.gradient)} />
                        <div className="flex items-start justify-between">
                            <div>
                                <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-1">{stat.label}</p>
                                <p className="text-3xl font-bold text-slate-900 tracking-tight">{stat.value}</p>
                                <p className="text-[11px] text-slate-400 mt-1">{stat.sub}</p>
                            </div>
                            <div className={cn("p-2 rounded-lg bg-gradient-to-br", stat.gradient)}>
                                <stat.icon className="w-4 h-4 text-white" />
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Entity Types Grid */}
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
                <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
                    <h2 className="text-[13px] font-semibold text-slate-800">Entity Types ({ENTITY_TYPES.length})</h2>
                    <span className="text-[11px] text-slate-400">Sorted by count</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-px bg-slate-100">
                    {ENTITY_TYPES.map((entity) => (
                        <div key={entity.type} className="bg-white p-4 flex items-center gap-3 hover:bg-slate-50/50 transition-colors">
                            <div className={cn("p-2 rounded-lg shrink-0", entity.bg)}>
                                <entity.icon className={cn("w-4 h-4", entity.color)} />
                            </div>
                            <div className="flex-1 min-w-0">
                                <div className="flex items-center justify-between">
                                    <p className="text-[12px] font-semibold text-slate-700">{entity.type}</p>
                                    <span className="text-[12px] font-bold text-slate-900 font-mono">{entity.count.toLocaleString()}</span>
                                </div>
                                <p className="text-[10px] text-slate-400 truncate">{entity.desc}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Relationships + Vector Store side-by-side */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {/* Relationships */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
                    <div className="px-5 py-4 border-b border-slate-100">
                        <h2 className="text-[13px] font-semibold text-slate-800">Relationship Types</h2>
                    </div>
                    <div className="divide-y divide-slate-50">
                        {RELATIONSHIPS.map((rel) => (
                            <div key={rel.type} className="px-5 py-2.5 flex items-center justify-between hover:bg-slate-50/50 transition-colors">
                                <div className="flex items-center gap-2">
                                    <code className="text-[11px] font-mono font-semibold text-indigo-600 bg-indigo-50 px-1.5 py-0.5 rounded border border-indigo-100">
                                        {rel.type}
                                    </code>
                                    <span className="text-[10px] text-slate-400">{rel.desc}</span>
                                </div>
                                <span className="text-[12px] font-bold text-slate-700 font-mono">{rel.count.toLocaleString()}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Vector Collections */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
                    <div className="px-5 py-4 border-b border-slate-100">
                        <h2 className="text-[13px] font-semibold text-slate-800">Vector Store Collections</h2>
                        <p className="text-[10px] text-slate-400 mt-0.5">Gemini text-embedding-004 (768 dims)</p>
                    </div>
                    <div className="p-5 space-y-3">
                        {VECTOR_COLLECTIONS.map((coll) => {
                            const pct = (coll.count / TOTAL_VECTORS) * 100;
                            return (
                                <div key={coll.name}>
                                    <div className="flex items-center justify-between mb-1">
                                        <span className="text-[12px] font-semibold text-slate-700">{coll.name}</span>
                                        <span className="text-[11px] font-mono font-bold text-slate-600">{coll.count.toLocaleString()}</span>
                                    </div>
                                    <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full transition-all duration-700"
                                            style={{ width: `${Math.max(pct, 2)}%` }}
                                        />
                                    </div>
                                    <p className="text-[10px] text-slate-400 mt-0.5">{coll.desc}</p>
                                </div>
                            );
                        })}
                    </div>
                    <div className="px-5 py-3 bg-slate-50/50 border-t border-slate-100 flex items-center justify-between">
                        <span className="text-[11px] font-semibold text-slate-500">Total Documents</span>
                        <span className="text-[13px] font-bold text-slate-800 font-mono">{TOTAL_VECTORS.toLocaleString()}</span>
                    </div>
                </div>
            </div>

            {/* Architecture Info */}
            <div className="p-5 bg-gradient-to-r from-slate-50 to-indigo-50/30 rounded-xl border border-slate-200">
                <div className="flex items-start gap-4">
                    <div className="p-2.5 rounded-lg bg-white border border-slate-200 shadow-sm shrink-0">
                        <Network className="w-5 h-5 text-indigo-600" />
                    </div>
                    <div>
                        <h3 className="text-[13px] font-semibold text-slate-800 mb-1">Hybrid Retrieval Architecture</h3>
                        <p className="text-[12px] text-slate-500 leading-relaxed">
                            <strong className="text-slate-700">Graph + Vector fusion</strong> via Reciprocal Rank Fusion (RRF).
                            Neo4j handles structural traversal (multi-hop reasoning across articles, obligations, cross-regulation links).
                            Vector store handles semantic discovery (cosine similarity over Gemini embeddings).
                            Combined results are synthesized by Gemini 1.5 Pro for grounded legal analysis with citations.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

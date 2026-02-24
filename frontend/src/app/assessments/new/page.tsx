"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ShieldAlert, ArrowRight, CheckCircle2, Loader2, Building2, Server, FileText, FlaskConical, ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "@/lib/utils";

type FormData = {
    system_description: string;
    system_type: string;
    deployment_context: string;
    company_name: string;
};

const PREDEFINED_TEST_CASES: {
    id: string;
    label: string;
    description: string;
    tag: string;
    data: FormData;
}[] = [
    {
        id: "GT_01",
        label: "Prohibited AI Practice",
        description: "Tests detection of prohibited AI practices and associated penalties (AIACT Art. 5).",
        tag: "PROHIBITED",
        data: {
            company_name: "Demo: Government Agency",
            system_type: "Social Scoring System",
            deployment_context: "Public Authority Citizen Assessment",
            system_description: "Is social scoring by public authorities allowed under the EU AI Act?",
        },
    },
    {
        id: "GT_02",
        label: "Cross-Regulation Obligations",
        description: "Tests cross-regulation retrieval for automated decision-making under GDPR Art. 22 & AI Act Art. 14.",
        tag: "GDPR + AI Act",
        data: {
            company_name: "Demo: FinTech Corporation",
            system_type: "Automated Decision-Making System",
            deployment_context: "Financial Services — GDPR & AI Act",
            system_description: "What obligations apply when using automated decision-making that processes personal data under both GDPR and AI Act?",
        },
    },
    {
        id: "GT_03",
        label: "Data Subject Rights",
        description: "Tests data subject rights retrieval under GDPR Art. 15 (right of access).",
        tag: "GDPR",
        data: {
            company_name: "Demo: Data Controller Ltd.",
            system_type: "Personal Data Processing System",
            deployment_context: "GDPR Data Access Rights",
            system_description: "What rights does a data subject have regarding access to their personal data?",
        },
    },
    {
        id: "GT_04",
        label: "DPIA & FRIA Requirements",
        description: "Tests co-triggering of Data Protection and Fundamental Rights Impact Assessments (GDPR Art. 35 & AI Act Art. 27).",
        tag: "DPIA / FRIA",
        data: {
            company_name: "Demo: High-Risk AI Deployer",
            system_type: "High-Risk AI System",
            deployment_context: "Critical Infrastructure Deployment",
            system_description: "When must a Data Protection Impact Assessment and a Fundamental Rights Impact Assessment both be conducted?",
        },
    },
    {
        id: "GT_05",
        label: "Chatbot Transparency",
        description: "Tests AI Act transparency obligations for limited-risk systems (AI Act Art. 50).",
        tag: "LIMITED RISK",
        data: {
            company_name: "Demo: Tech Company",
            system_type: "LLM Chatbot",
            deployment_context: "Customer Service Deployment",
            system_description: "What are the transparency requirements for deploying a chatbot under the AI Act?",
        },
    },
    {
        id: "GT_06",
        label: "Household Exemption",
        description: "Tests household exemption / scope exclusion under GDPR Art. 2.",
        tag: "OUT OF SCOPE",
        data: {
            company_name: "Demo: Private Individual",
            system_type: "Personal Use Application",
            deployment_context: "Household / Personal Activity",
            system_description: "Does the GDPR apply to personal use of data for household activities?",
        },
    },
];

const TAG_STYLES: Record<string, string> = {
    "PROHIBITED": "bg-red-50 text-red-600 border-red-200",
    "GDPR + AI Act": "bg-purple-50 text-purple-600 border-purple-200",
    "GDPR": "bg-blue-50 text-blue-600 border-blue-200",
    "DPIA / FRIA": "bg-indigo-50 text-indigo-600 border-indigo-200",
    "LIMITED RISK": "bg-amber-50 text-amber-700 border-amber-200",
    "OUT OF SCOPE": "bg-slate-100 text-slate-500 border-slate-200",
};

export default function NewAssessmentPage() {
    const router = useRouter();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [showTestCases, setShowTestCases] = useState(true);
    const [selectedTestCase, setSelectedTestCase] = useState<string | null>(null);
    const [formData, setFormData] = useState<FormData>({
        system_description: "",
        system_type: "",
        deployment_context: "",
        company_name: "",
    });

    const loadTestCase = (tc: (typeof PREDEFINED_TEST_CASES)[0]) => {
        setFormData(tc.data);
        setSelectedTestCase(tc.id);
        // Scroll to form
        document.getElementById("assessment-form")?.scrollIntoView({ behavior: "smooth", block: "start" });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            const res = await fetch("http://localhost:8000/api/v1/assessments", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            if (!res.ok) throw new Error("Failed to start assessment");

            const data = await res.json();
            router.push(`/assessments/${data.session_id}`);
        } catch (error) {
            console.error(error);
            setIsSubmitting(false);
            alert("Failed to connect to orchestrator API (make sure it's running on port 8000)");
        }
    };

    return (
        <div className="max-w-3xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500 ease-out">
            <div>
                <h1 className="text-2xl font-bold text-slate-900 mb-1">Initiate Compliance Review</h1>
                <p className="text-sm text-slate-500">Submit a new AI system for automated EU AI Act classification and GDPR audit.</p>
            </div>

            {/* Predefined Test Cases */}
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                <button
                    type="button"
                    onClick={() => setShowTestCases((v) => !v)}
                    className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-50 transition-colors"
                >
                    <span className="flex items-center text-sm font-medium text-slate-700">
                        <FlaskConical className="w-4 h-4 mr-2 text-indigo-500" />
                        Predefined Test Cases
                        <span className="ml-2 px-1.5 py-0.5 text-[10px] font-bold bg-indigo-100 text-indigo-600 border border-indigo-200 rounded">
                            {PREDEFINED_TEST_CASES.length}
                        </span>
                    </span>
                    {showTestCases ? (
                        <ChevronUp className="w-4 h-4 text-slate-400" />
                    ) : (
                        <ChevronDown className="w-4 h-4 text-slate-400" />
                    )}
                </button>

                {showTestCases && (
                    <div className="px-6 pb-6 pt-2 grid grid-cols-1 sm:grid-cols-2 gap-3 border-t border-slate-100">
                        {PREDEFINED_TEST_CASES.map((tc) => (
                            <button
                                key={tc.id}
                                type="button"
                                onClick={() => loadTestCase(tc)}
                                className={cn(
                                    "text-left p-4 rounded-lg border transition-all hover:border-indigo-300 hover:bg-indigo-50/50",
                                    selectedTestCase === tc.id
                                        ? "border-indigo-400 bg-indigo-50 shadow-sm"
                                        : "border-slate-200 bg-white"
                                )}
                            >
                                <div className="flex items-center justify-between mb-2">
                                    <span className="font-mono text-[10px] font-bold text-slate-400">{tc.id}</span>
                                    <span className={cn(
                                        "text-[10px] font-bold px-1.5 py-0.5 rounded border",
                                        TAG_STYLES[tc.tag] ?? "bg-slate-100 text-slate-500 border-slate-200"
                                    )}>
                                        {tc.tag}
                                    </span>
                                </div>
                                <p className="text-sm font-semibold text-slate-700 mb-1">{tc.label}</p>
                                <p className="text-xs text-slate-500 leading-relaxed">{tc.description}</p>
                            </button>
                        ))}
                    </div>
                )}
            </div>

            {/* Assessment Form */}
            <div id="assessment-form" className="bg-white rounded-xl border border-slate-200 shadow-sm relative overflow-hidden">
                {/* Indigo top accent */}
                <div className="absolute top-0 inset-x-0 h-0.5 bg-indigo-600" />

                <form onSubmit={handleSubmit} className="p-8 space-y-6">
                    <div className="space-y-5">
                        <div className="space-y-1.5">
                            <label htmlFor="company_name" className="text-xs font-semibold uppercase tracking-wider text-slate-500 flex items-center gap-2">
                                <Building2 className="w-3.5 h-3.5 text-slate-400" />
                                Company / Organization
                            </label>
                            <input
                                id="company_name"
                                required
                                value={formData.company_name}
                                onChange={e => setFormData({ ...formData, company_name: e.target.value })}
                                placeholder="e.g. Acme Corporation"
                                className="w-full px-4 py-2.5 text-slate-800 bg-white border border-slate-200 rounded-lg text-sm transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 placeholder:text-slate-400"
                            />
                        </div>

                        <div className="space-y-1.5">
                            <label htmlFor="system_type" className="text-xs font-semibold uppercase tracking-wider text-slate-500 flex items-center gap-2">
                                <Server className="w-3.5 h-3.5 text-slate-400" />
                                AI System Type
                            </label>
                            <input
                                id="system_type"
                                required
                                value={formData.system_type}
                                onChange={e => setFormData({ ...formData, system_type: e.target.value })}
                                placeholder="e.g. Facial Recognition, Large Language Model, Predictive Analytics"
                                className="w-full px-4 py-2.5 text-slate-800 bg-white border border-slate-200 rounded-lg text-sm transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 placeholder:text-slate-400"
                            />
                        </div>

                        <div className="space-y-1.5">
                            <label htmlFor="deployment_context" className="text-xs font-semibold uppercase tracking-wider text-slate-500 flex items-center gap-2">
                                <ShieldAlert className="w-3.5 h-3.5 text-slate-400" />
                                Intended Deployment Context
                            </label>
                            <input
                                id="deployment_context"
                                required
                                value={formData.deployment_context}
                                onChange={e => setFormData({ ...formData, deployment_context: e.target.value })}
                                placeholder="e.g. Employee Monitoring, Healthcare Diagnostics, Recruitment"
                                className="w-full px-4 py-2.5 text-slate-800 bg-white border border-slate-200 rounded-lg text-sm transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 placeholder:text-slate-400"
                            />
                        </div>

                        <div className="space-y-1.5">
                            <label htmlFor="system_description" className="text-xs font-semibold uppercase tracking-wider text-slate-500 flex items-center gap-2">
                                <FileText className="w-3.5 h-3.5 text-slate-400" />
                                System Description & Capabilities
                            </label>
                            <textarea
                                id="system_description"
                                required
                                rows={5}
                                value={formData.system_description}
                                onChange={e => setFormData({ ...formData, system_description: e.target.value })}
                                placeholder="Describe exactly what the system does, the data it consumes, and how it interacts with humans..."
                                className="w-full px-4 py-2.5 text-slate-800 bg-white border border-slate-200 rounded-lg text-sm transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 placeholder:text-slate-400 resize-none"
                            />
                        </div>
                    </div>

                    <div className="pt-4 flex items-center justify-between border-t border-slate-100">
                        <p className="text-xs text-slate-400 flex items-center gap-1.5">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                            Automated multi-agent analysis takes ~2 minutes.
                        </p>
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className="inline-flex items-center justify-center px-6 py-2.5 text-sm font-semibold rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isSubmitting ? (
                                <>
                                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                    Initializing Agents...
                                </>
                            ) : (
                                <>
                                    Start Assessment
                                    <ArrowRight className="w-4 h-4 ml-2" />
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8004";

export const api = {
  base: API_BASE,
  scans: `${API_BASE}/api/v1/scans`,
  scan: (id: string) => `${API_BASE}/api/v1/scans/${id}`,
  scanFindings: (id: string) => `${API_BASE}/api/v1/scans/${id}/findings`,
  scanReport: (id: string) => `${API_BASE}/api/v1/scans/${id}/report`,
  statistics: `${API_BASE}/api/v1/statistics`,
  auditLog: `${API_BASE}/api/v1/audit-log`,
  health: `${API_BASE}/health`,
};

export type ScanStatus = "queued" | "running" | "completed" | "failed";

export type ScanSummary = {
  scan_id: string;
  status: ScanStatus;
  repo_url: string;
  ref: string;
  created_at: string;
  completed_at: string | null;
  risk_category: string | null;
  compliance_score: number | null;
  finding_count: number | null;
  error?: string | null;
};

export type Severity = "critical" | "high" | "medium" | "low" | "info";

export type Evidence = {
  file: string;
  line: number;
  column?: number | null;
  excerpt?: string | null;
  symbol?: string | null;
};

export type Finding = {
  rule_id: string;
  title: string;
  severity: Severity;
  confidence: number;
  evidence: Evidence[];
  mapped_articles: string[];
  obligation_anchors: string[];
  remediation?: string | null;
  suppressed: boolean;
  suppress_reason?: string | null;
};

export type RiskPosture = {
  category: "PROHIBITED" | "HIGH_RISK" | "LIMITED_RISK" | "MINIMAL_RISK";
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  prohibited_triggers: string[];
  reason: string;
  compliance_score: number;
};

export type LegalCitation = {
  regulation: string;
  article_number: string;
  title?: string | null;
  text_snippet?: string | null;
  relevance_score: number;
  obligation_anchor?: string | null;
};

export type FindingCitations = {
  rule_id: string;
  citations: LegalCitation[];
  reasoning_chain: string[];
};

export type RemediationStep = {
  priority: "immediate" | "short_term" | "long_term";
  finding_rule_ids: string[];
  title: string;
  description: string;
  effort: "low" | "medium" | "high";
};

export type NarrativeReport = {
  executive_summary: string;
  risk_narrative: string;
  top_findings_narrative: string;
  remediation_plan: RemediationStep[];
};

export type ScanState = {
  scan_id: string;
  repo_url: string;
  ref: string;
  profile: {
    scan_id: string;
    repo: {
      url: string;
      ref: string;
      commit?: string | null;
      languages: string[];
      total_files: number;
      scanned_files: number;
    };
    ai_components: { kind: string; name: string; evidence: Evidence[] }[];
    decision_surfaces: {
      endpoint: string;
      file: string;
      line: number;
      calls_model: boolean;
      has_human_review: boolean;
      has_audit_log: boolean;
    }[];
    data_signals: {
      pii_fields: string[];
      has_dpia_doc: boolean;
      has_model_card: boolean;
      has_data_card: boolean;
      audit_logging: "none" | "partial" | "present";
    };
    findings: Finding[];
    stats: Record<string, unknown>;
  } | null;
  risk_posture: RiskPosture | null;
  finding_citations: FindingCitations[];
  narrative: NarrativeReport | null;
  final_report: Record<string, unknown> | null;
  current_step: string;
  workflow_status: ScanStatus;
  errors: string[];
  started_at: string;
  completed_at: string | null;
};

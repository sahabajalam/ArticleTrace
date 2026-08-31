const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8004";

export const api = {
  base: API_BASE,
  scans: `${API_BASE}/api/v1/scans`,
  scan: (id: string) => `${API_BASE}/api/v1/scans/${id}`,
  scanReport: (id: string) => `${API_BASE}/api/v1/scans/${id}/report`,
  health: `${API_BASE}/health`,
};

export type ScanStatus = "queued" | "running" | "completed" | "failed";
export type Severity = "critical" | "high" | "medium" | "low" | "info";
export type RiskCategory =
  | "PROHIBITED"
  | "HIGH_RISK"
  | "LIMITED_RISK"
  | "MINIMAL_RISK";

export type ScanSummary = {
  scan_id: string;
  status: ScanStatus;
  repo_url: string;
  ref: string;
  created_at: string;
  completed_at: string | null;
  risk_category: RiskCategory | null;
  finding_count: number | null;
  error?: string | null;
};

export type Evidence = {
  file: string;
  /** null for repo-level facts, e.g. "no model card anywhere" (see BUG_LOG DL-029). */
  line: number | null;
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
  /** "llm-confirmed" | "llm-demoted: <reason>" | null when triage did not run. */
  triage?: string | null;
};

export type RiskPosture = {
  category: RiskCategory;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  prohibited_triggers: string[];
  /** Prohibited patterns seen only in test/example context — capability, not deployment. */
  dampened_triggers?: string[];
  reason: string;
  compliance_score: number;
};

/** Coverage receipts: what the scanner could not read, so "no findings" is
 *  distinguishable from "never looked". */
export type ScanStats = {
  /** Size of the rule corpus this scan actually ran against. 0 or missing
   *  means the findings are meaningless, however clean they look. */
  rules_loaded?: number;
  total_findings?: number;
  by_severity?: Record<string, number>;
  by_rule?: Record<string, number>;
  suppressed?: number;
  manifest_scan?: { files: string[]; errors: string[] };
  source_read_errors?: string[];
  llm_triage?: {
    status: "ok" | "skipped" | "failed";
    reason?: string;
    reviewed?: number;
    demoted?: number;
    confirmed?: number;
    capped_out?: number;
  };
};

export type RepoInfo = {
  url: string;
  ref: string;
  commit?: string | null;
  languages: string[];
  total_files: number;
  scanned_files: number;
};

export type ScanReport = {
  scan_id: string;
  repo_url: string;
  ref: string;
  risk_posture: RiskPosture | null;
  profile: {
    repo: RepoInfo;
    ai_components: { kind: string; name: string; evidence: Evidence[] }[];
    findings: Finding[];
    stats: ScanStats;
  } | null;
  completed_at: string | null;
};

export const SEVERITY_ORDER: Severity[] = [
  "critical",
  "high",
  "medium",
  "low",
  "info",
];

export async function getJSON<T>(url: string): Promise<T> {
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json() as Promise<T>;
}

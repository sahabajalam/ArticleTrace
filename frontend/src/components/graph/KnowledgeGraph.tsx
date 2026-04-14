"use client";

import { useRef, useEffect, useMemo, useCallback, useState } from "react";
import dynamic from "next/dynamic";
import { cn } from "@/lib/utils";

// Lazy-load the force graph (it uses canvas/window APIs)
const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), { ssr: false });

// ── Types ──────────────────────────────────────────────────────────────

interface GraphNode {
    id: string;
    label: string;
    type: "entity" | "article" | "relationship" | "query" | "regulation";
    group?: string;          // regulation or category
    confidence?: number;
    val?: number;            // node size weight
    // Force-graph internals
    x?: number;
    y?: number;
    fx?: number;
    fy?: number;
}

interface GraphLink {
    source: string;
    target: string;
    label?: string;
    type: "resolves_to" | "reasoning_hop" | "chain_link";
}

interface KnowledgeGraphProps {
    resolved_entities?: Record<string, string[]>;
    kg_connections?: Array<{
        chain: string[];
        source_regulation: string;
    }>;
    relationship_chains?: string[][];
    className?: string;
}

// ── Color palette (Neo4j-inspired) ─────────────────────────────────────

const NODE_COLORS: Record<string, string> = {
    entity: "#6366f1",       // indigo
    article: "#8b5cf6",      // violet
    relationship: "#64748b",  // slate
    query: "#0ea5e9",        // sky
    regulation: "#f59e0b",   // amber
};

const REGULATION_COLORS: Record<string, string> = {
    GDPR: "#3b82f6",        // blue
    EU_AI_ACT: "#a855f7",   // purple
    mixed: "#6b7280",       // gray
};

const LINK_COLORS: Record<string, string> = {
    resolves_to: "#818cf8",  // indigo-400
    reasoning_hop: "#c084fc", // purple-400
    chain_link: "#94a3b8",   // slate-400
};

// ── Helpers ────────────────────────────────────────────────────────────

function isRelArrow(s: string) {
    return s.startsWith("→") || s.includes("→");
}

function extractRelName(s: string) {
    return s.replace(/→/g, "").trim();
}

function buildGraphData(
    resolved_entities: Record<string, string[]>,
    kg_connections: Array<{ chain: string[]; source_regulation: string }>,
    relationship_chains: string[][],
) {
    const nodesMap = new Map<string, GraphNode>();
    const links: GraphLink[] = [];

    const ensureNode = (id: string, label: string, type: GraphNode["type"], group?: string) => {
        if (!nodesMap.has(id)) {
            nodesMap.set(id, {
                id,
                label,
                type,
                group,
                val: type === "regulation" ? 6 : type === "article" ? 4 : type === "query" ? 3 : 2,
            });
        }
    };

    // 1. Entity Resolution: query terms → resolved graph node IDs
    for (const [term, ids] of Object.entries(resolved_entities)) {
        const queryId = `q:${term}`;
        ensureNode(queryId, term, "query");

        for (const nodeId of ids) {
            const entityId = `e:${nodeId}`;
            ensureNode(entityId, nodeId, "article", nodeId.startsWith("GDPR") ? "GDPR" : "EU_AI_ACT");
            links.push({ source: queryId, target: entityId, label: "resolves to", type: "resolves_to" });
        }
    }

    // 2. KG Reasoning Chains (from decision_graph.kg_connections)
    for (const conn of kg_connections) {
        const regId = `reg:${conn.source_regulation}`;
        ensureNode(regId, conn.source_regulation === "EU_AI_ACT" ? "AI Act" : conn.source_regulation, "regulation", conn.source_regulation);

        let prevId = regId;
        for (const segment of conn.chain) {
            if (isRelArrow(segment)) continue;

            const nodeId = `kg:${segment}`;
            ensureNode(nodeId, segment, "entity", conn.source_regulation);

            // Find the relationship label between prev and this
            const idx = conn.chain.indexOf(segment);
            let relLabel = "";
            if (idx > 0 && isRelArrow(conn.chain[idx - 1])) {
                relLabel = extractRelName(conn.chain[idx - 1]);
            }

            links.push({ source: prevId, target: nodeId, label: relLabel, type: "chain_link" });
            prevId = nodeId;
        }
    }

    // 3. Multi-hop Reasoning Chains (from legal_citations.relationship_chains)
    for (const chain of relationship_chains) {
        let prevId: string | null = null;
        for (const segment of chain) {
            if (isRelArrow(segment)) continue;

            const nodeId = `hop:${segment}`;
            ensureNode(nodeId, segment, "article");

            if (prevId) {
                const idx = chain.indexOf(segment);
                let relLabel = "";
                if (idx > 0 && isRelArrow(chain[idx - 1])) {
                    relLabel = extractRelName(chain[idx - 1]);
                }
                links.push({ source: prevId, target: nodeId, label: relLabel, type: "reasoning_hop" });
            }
            prevId = nodeId;
        }
    }

    // Deduplicate links
    const linkSet = new Set<string>();
    const uniqueLinks = links.filter(l => {
        const key = `${typeof l.source === "string" ? l.source : (l.source as any).id}-${typeof l.target === "string" ? l.target : (l.target as any).id}`;
        if (linkSet.has(key)) return false;
        linkSet.add(key);
        return true;
    });

    // Remove orphan nodes (nodes with no connections)
    const connectedIds = new Set<string>();
    for (const l of uniqueLinks) {
        connectedIds.add(typeof l.source === "string" ? l.source : (l.source as any).id);
        connectedIds.add(typeof l.target === "string" ? l.target : (l.target as any).id);
    }

    const nodes = Array.from(nodesMap.values()).filter(n => connectedIds.has(n.id));

    return { nodes, links: uniqueLinks };
}

// ── Component ──────────────────────────────────────────────────────────

export default function KnowledgeGraph({
    resolved_entities = {},
    kg_connections = [],
    relationship_chains = [],
    className,
}: KnowledgeGraphProps) {
    const containerRef = useRef<HTMLDivElement>(null);
    const fgRef = useRef<any>(null);
    const [dimensions, setDimensions] = useState({ width: 800, height: 500 });
    const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null);

    // Measure container
    useEffect(() => {
        const el = containerRef.current;
        if (!el) return;
        const ro = new ResizeObserver((entries) => {
            const { width } = entries[0].contentRect;
            setDimensions({ width, height: Math.max(420, Math.min(600, width * 0.55)) });
        });
        ro.observe(el);
        return () => ro.disconnect();
    }, []);

    const graphData = useMemo(
        () => buildGraphData(resolved_entities, kg_connections, relationship_chains),
        [resolved_entities, kg_connections, relationship_chains],
    );

    // Zoom to fit on mount
    useEffect(() => {
        const t = setTimeout(() => fgRef.current?.zoomToFit(400, 40), 500);
        return () => clearTimeout(t);
    }, [graphData]);

    const nodeColor = useCallback((node: any) => {
        const n = node as GraphNode;
        if (n.group && REGULATION_COLORS[n.group]) return REGULATION_COLORS[n.group];
        return NODE_COLORS[n.type] || "#94a3b8";
    }, []);

    const paintNode = useCallback((node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
        const n = node as GraphNode;
        const x = n.x ?? 0;
        const y = n.y ?? 0;
        const r = Math.sqrt(n.val ?? 2) * 4;
        const isHovered = hoveredNode?.id === n.id;
        const fontSize = Math.max(10 / globalScale, 2);

        // Glow on hover
        if (isHovered) {
            ctx.shadowColor = nodeColor(n);
            ctx.shadowBlur = 15;
        }

        // Node circle
        ctx.beginPath();
        ctx.arc(x, y, r, 0, 2 * Math.PI);
        ctx.fillStyle = nodeColor(n);
        ctx.fill();

        // Border
        ctx.strokeStyle = isHovered ? "#fff" : "rgba(255,255,255,0.3)";
        ctx.lineWidth = isHovered ? 2 / globalScale : 0.5 / globalScale;
        ctx.stroke();

        ctx.shadowColor = "transparent";
        ctx.shadowBlur = 0;

        // Label
        if (globalScale > 0.6 || isHovered) {
            const label = n.label.length > 24 ? n.label.slice(0, 22) + "..." : n.label;
            ctx.font = `${isHovered ? "bold " : ""}${fontSize}px Inter, system-ui, sans-serif`;
            ctx.textAlign = "center";
            ctx.textBaseline = "top";

            // Background for readability
            const textWidth = ctx.measureText(label).width;
            const padding = 2 / globalScale;
            ctx.fillStyle = "rgba(15, 23, 42, 0.75)";
            ctx.beginPath();
            ctx.roundRect(
                x - textWidth / 2 - padding,
                y + r + 2 / globalScale,
                textWidth + padding * 2,
                fontSize + padding * 2,
                2 / globalScale,
            );
            ctx.fill();

            ctx.fillStyle = "#f8fafc";
            ctx.fillText(label, x, y + r + 2 / globalScale + padding);
        }
    }, [hoveredNode, nodeColor]);

    const paintLink = useCallback((link: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
        const l = link as GraphLink & { source: any; target: any };
        const sx = l.source.x ?? 0;
        const sy = l.source.y ?? 0;
        const tx = l.target.x ?? 0;
        const ty = l.target.y ?? 0;

        // Line
        ctx.beginPath();
        ctx.moveTo(sx, sy);
        ctx.lineTo(tx, ty);
        ctx.strokeStyle = LINK_COLORS[l.type] || "#94a3b8";
        ctx.lineWidth = l.type === "resolves_to" ? 1.5 / globalScale : 1 / globalScale;
        if (l.type === "chain_link") {
            ctx.setLineDash([4 / globalScale, 2 / globalScale]);
        }
        ctx.stroke();
        ctx.setLineDash([]);

        // Arrow head
        const angle = Math.atan2(ty - sy, tx - sx);
        const targetR = Math.sqrt((l.target as any).val ?? 2) * 4;
        const ax = tx - Math.cos(angle) * (targetR + 2);
        const ay = ty - Math.sin(angle) * (targetR + 2);
        const arrowLen = 6 / globalScale;

        ctx.beginPath();
        ctx.moveTo(ax, ay);
        ctx.lineTo(
            ax - arrowLen * Math.cos(angle - Math.PI / 7),
            ay - arrowLen * Math.sin(angle - Math.PI / 7),
        );
        ctx.lineTo(
            ax - arrowLen * Math.cos(angle + Math.PI / 7),
            ay - arrowLen * Math.sin(angle + Math.PI / 7),
        );
        ctx.closePath();
        ctx.fillStyle = LINK_COLORS[l.type] || "#94a3b8";
        ctx.fill();

        // Edge label
        if (l.label && globalScale > 1.2) {
            const mx = (sx + tx) / 2;
            const my = (sy + ty) / 2;
            const fontSize = Math.max(8 / globalScale, 1.5);
            ctx.font = `${fontSize}px Inter, system-ui, sans-serif`;
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";

            const tw = ctx.measureText(l.label).width;
            const pad = 1.5 / globalScale;
            ctx.fillStyle = "rgba(15, 23, 42, 0.65)";
            ctx.beginPath();
            ctx.roundRect(mx - tw / 2 - pad, my - fontSize / 2 - pad, tw + pad * 2, fontSize + pad * 2, 1.5 / globalScale);
            ctx.fill();

            ctx.fillStyle = "#e2e8f0";
            ctx.fillText(l.label, mx, my);
        }
    }, []);

    if (graphData.nodes.length === 0) {
        return (
            <div className={cn("flex items-center justify-center h-40 text-sm text-slate-400 bg-slate-50 rounded-xl border border-slate-200", className)}>
                No graph data available
            </div>
        );
    }

    // Legend entries
    const legendItems = [
        { color: NODE_COLORS.query, label: "Query Term" },
        { color: NODE_COLORS.article, label: "Legal Article" },
        { color: NODE_COLORS.entity, label: "Entity / Concept" },
        { color: NODE_COLORS.regulation, label: "Regulation" },
        { color: LINK_COLORS.resolves_to, label: "Entity Resolution", dash: false },
        { color: LINK_COLORS.reasoning_hop, label: "Reasoning Hop", dash: false },
        { color: LINK_COLORS.chain_link, label: "KG Chain", dash: true },
    ];

    return (
        <div ref={containerRef} className={cn("relative", className)}>
            {/* Graph Canvas */}
            <div className="rounded-xl overflow-hidden border border-slate-200 bg-slate-950">
                <ForceGraph2D
                    ref={fgRef}
                    width={dimensions.width}
                    height={dimensions.height}
                    graphData={graphData}
                    nodeCanvasObject={paintNode}
                    linkCanvasObject={paintLink}
                    nodeRelSize={4}
                    linkDirectionalArrowLength={0}
                    onNodeHover={(node: any) => setHoveredNode(node as GraphNode | null)}
                    cooldownTicks={80}
                    d3AlphaDecay={0.04}
                    d3VelocityDecay={0.3}
                    backgroundColor="#0f172a"
                    enableZoomInteraction={true}
                    enablePanInteraction={true}
                />
            </div>

            {/* Legend */}
            <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1.5 px-1">
                {legendItems.map((item) => (
                    <div key={item.label} className="flex items-center gap-1.5 text-[10px] text-slate-500">
                        {item.dash !== undefined ? (
                            <svg width="16" height="6" className="shrink-0">
                                <line
                                    x1="0" y1="3" x2="16" y2="3"
                                    stroke={item.color}
                                    strokeWidth="2"
                                    strokeDasharray={item.dash ? "3,2" : undefined}
                                />
                            </svg>
                        ) : (
                            <span
                                className="w-2.5 h-2.5 rounded-full shrink-0"
                                style={{ backgroundColor: item.color }}
                            />
                        )}
                        {item.label}
                    </div>
                ))}
            </div>

            {/* Hover tooltip */}
            {hoveredNode && (
                <div className="absolute top-3 right-3 bg-slate-900/90 backdrop-blur-sm border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 max-w-[200px] pointer-events-none z-10">
                    <p className="font-semibold text-white">{hoveredNode.label}</p>
                    <p className="text-slate-400 mt-0.5 capitalize">{hoveredNode.type}{hoveredNode.group ? ` · ${hoveredNode.group}` : ""}</p>
                </div>
            )}
        </div>
    );
}

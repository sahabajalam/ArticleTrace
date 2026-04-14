"use client";

import { usePathname } from "next/navigation";
import { ChevronRight } from "lucide-react";

const BREADCRUMB_MAP: Record<string, string> = {
    "": "Dashboard",
    scans: "Scans",
    new: "New Scan",
    knowledge: "Knowledge Graph",
};

export default function Topbar() {
    const pathname = usePathname();
    const segments = pathname?.split("/").filter(Boolean) ?? [];

    const crumbs = [
        { label: "AlloyCode", href: "/" },
        ...segments.map((seg, i) => ({
            label: BREADCRUMB_MAP[seg] ?? (seg.length > 12 ? `${seg.slice(0, 8)}...` : seg),
            href: "/" + segments.slice(0, i + 1).join("/"),
        })),
    ];

    return (
        <header className="h-14 flex items-center px-6 bg-white/80 backdrop-blur-md border-b border-slate-200/60 sticky top-0 z-30">
            <nav className="flex items-center gap-1 text-[13px]">
                {crumbs.map((crumb, i) => (
                    <span key={crumb.href} className="flex items-center gap-1">
                        {i > 0 && <ChevronRight className="w-3 h-3 text-slate-300" />}
                        <span
                            className={
                                i === crumbs.length - 1
                                    ? "font-semibold text-slate-800"
                                    : "text-slate-400 font-medium"
                            }
                        >
                            {crumb.label}
                        </span>
                    </span>
                ))}
            </nav>
        </header>
    );
}

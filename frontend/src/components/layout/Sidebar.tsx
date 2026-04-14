"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
    LayoutDashboard, ScanSearch, Database,
    ChevronRight, Zap,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_SECTIONS = [
    {
        label: "Platform",
        items: [
            { name: "Dashboard", href: "/", icon: LayoutDashboard },
            { name: "New Scan", href: "/scans/new", icon: ScanSearch },
        ],
    },
    {
        label: "Intelligence",
        items: [
            { name: "Knowledge Graph", href: "/knowledge", icon: Database },
        ],
    },
];

export default function Sidebar() {
    const pathname = usePathname();

    return (
        <div className="flex flex-col w-[260px] h-full bg-white border-r border-slate-200/80">
            {/* Brand */}
            <div className="flex items-center h-16 px-5 border-b border-slate-100">
                <div className="relative flex items-center justify-center w-8 h-8 rounded-lg mr-3 bg-gradient-to-br from-indigo-600 to-violet-600 shrink-0 shadow-sm">
                    <Zap className="w-4 h-4 text-white" />
                    <div className="absolute inset-0 rounded-lg bg-white/10" />
                </div>
                <div className="min-w-0">
                    <span className="font-bold text-[15px] text-slate-900 tracking-tight block leading-tight">AlloyCode</span>
                    <span className="text-[10px] font-medium text-slate-400 tracking-wide uppercase">Compliance Engine</span>
                </div>
            </div>

            {/* Navigation */}
            <div className="flex-1 overflow-y-auto py-4 px-3 space-y-6">
                {NAV_SECTIONS.map((section) => (
                    <div key={section.label}>
                        <p className="px-3 mb-1.5 text-[10px] font-semibold uppercase tracking-[0.1em] text-slate-400">
                            {section.label}
                        </p>
                        <nav className="space-y-0.5">
                            {section.items.map((item) => {
                                const isActive =
                                    pathname === item.href ||
                                    (item.href !== "/" && pathname?.startsWith(`${item.href}/`));
                                return (
                                    <Link
                                        key={item.href}
                                        href={item.href}
                                        className={cn(
                                            "flex items-center px-3 py-2 text-[13px] font-medium rounded-lg transition-all duration-150 group",
                                            isActive
                                                ? "bg-indigo-50 text-indigo-700 shadow-sm shadow-indigo-100/50"
                                                : "text-slate-500 hover:bg-slate-50 hover:text-slate-800"
                                        )}
                                    >
                                        <item.icon
                                            className={cn(
                                                "mr-2.5 flex-shrink-0 w-[15px] h-[15px] transition-colors",
                                                isActive ? "text-indigo-600" : "text-slate-400 group-hover:text-slate-500"
                                            )}
                                        />
                                        {item.name}
                                        {isActive && (
                                            <ChevronRight className="ml-auto w-3.5 h-3.5 text-indigo-400" />
                                        )}
                                    </Link>
                                );
                            })}
                        </nav>
                    </div>
                ))}
            </div>

        </div>
    );
}

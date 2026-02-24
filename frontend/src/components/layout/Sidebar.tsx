"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ShieldAlert, LayoutDashboard, FileText, Settings, UserCheck } from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
    { name: "Dashboard", href: "/", icon: LayoutDashboard },
    { name: "New Assessment", href: "/assessments/new", icon: ShieldAlert },
    { name: "Approvals", href: "/approvals", icon: UserCheck },
    { name: "Reports", href: "/reports", icon: FileText },
    { name: "Settings", href: "/settings", icon: Settings },
];

export default function Sidebar() {
    const pathname = usePathname();

    return (
        <div className="flex flex-col w-64 h-full bg-white border-r border-slate-200 text-slate-700">
            {/* Logo */}
            <div className="flex items-center h-16 px-5 border-b border-slate-200">
                <div className="flex items-center justify-center w-8 h-8 rounded-lg mr-3 bg-indigo-600 shrink-0">
                    <ShieldAlert className="w-4 h-4 text-white" />
                </div>
                <div>
                    <span className="font-bold text-sm text-slate-900 tracking-tight">AI Compliance</span>
                    <p className="text-[10px] text-slate-400 -mt-0.5">EU AI Act · GDPR</p>
                </div>
            </div>

            {/* Nav */}
            <div className="flex-1 overflow-y-auto py-5 px-3">
                <p className="px-3 mb-2 text-[10px] font-semibold uppercase tracking-widest text-slate-400">Navigation</p>
                <nav className="space-y-0.5">
                    {navigation.map((item) => {
                        const isActive = pathname === item.href || (item.href !== "/" && pathname?.startsWith(`${item.href}/`));
                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={cn(
                                    "flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-all group",
                                    isActive
                                        ? "bg-indigo-50 text-indigo-700"
                                        : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                                )}
                            >
                                <item.icon
                                    className={cn(
                                        "mr-3 flex-shrink-0 w-4 h-4 transition-colors",
                                        isActive ? "text-indigo-600" : "text-slate-400 group-hover:text-slate-600"
                                    )}
                                    aria-hidden="true"
                                />
                                {item.name}
                            </Link>
                        );
                    })}
                </nav>
            </div>

            {/* User */}
            <div className="p-4 border-t border-slate-200">
                <div className="flex items-center">
                    <div className="w-8 h-8 rounded-full flex items-center justify-center bg-indigo-600 shrink-0">
                        <span className="text-xs font-bold text-white">AD</span>
                    </div>
                    <div className="ml-3 min-w-0">
                        <p className="text-sm font-semibold text-slate-900 truncate">Admin User</p>
                        <p className="text-xs text-slate-400 truncate">Compliance Officer</p>
                    </div>
                    <div className="ml-auto w-2 h-2 rounded-full bg-emerald-500 shrink-0" title="Online" />
                </div>
            </div>
        </div>
    );
}

"use client";

import { Bell, Search } from "lucide-react";

export default function Topbar() {
    return (
        <header className="h-16 flex items-center justify-between px-6 bg-white border-b border-slate-200">
            <div className="flex items-center flex-1">
                <div className="relative w-full max-w-md">
                    <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                        <Search className="w-4 h-4 text-slate-400" />
                    </div>
                    <input
                        type="text"
                        className="block w-full pl-10 pr-3 py-2 border border-slate-200 rounded-lg bg-slate-50 text-slate-700 placeholder-slate-400 text-sm transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                        placeholder="Search assessments, systems, or policies..."
                    />
                </div>
            </div>

            <div className="flex items-center space-x-3 ml-4">
                <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                    API Online
                </div>
                <button className="relative p-2 rounded-lg text-slate-500 hover:text-slate-700 hover:bg-slate-100 transition-colors">
                    <span className="sr-only">View notifications</span>
                    <Bell className="w-5 h-5" />
                    <span className="absolute top-1.5 right-1.5 block w-2 h-2 rounded-full bg-rose-500 ring-2 ring-white" />
                </button>
            </div>
        </header>
    );
}

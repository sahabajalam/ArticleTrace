import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

interface MainLayoutProps {
    children: React.ReactNode;
}

export default function MainLayout({ children }: MainLayoutProps) {
    return (
        <div className="flex h-screen overflow-hidden font-[family-name:var(--font-inter)] bg-slate-50">
            <Sidebar />
            <div className="flex flex-col flex-1 overflow-hidden">
                <Topbar />
                <main className="flex-1 overflow-y-auto">
                    <div className="px-6 py-6 md:px-8 max-w-[1400px] mx-auto w-full">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
}

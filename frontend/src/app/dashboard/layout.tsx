"use client"; 

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/lib/stores/auth-store";
import { Sidebar } from "@/components/layout/sidebar";
import { Navbar } from "@/components/layout/navbar";
import { CommandPalette } from "@/components/layout/command-palette";
import { useAppStore } from "@/lib/stores/app-store";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const [hasHydrated, setHasHydrated] = useState(false);

  useEffect(() => {
    useAuthStore.persist.onFinishHydration(() => setHasHydrated(true));
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setHasHydrated(useAuthStore.persist.hasHydrated());
  }, []);

  useEffect(() => {
    if (hasHydrated && !isAuthenticated) {
      router.replace("/login");
    }
  }, [isAuthenticated, hasHydrated, router]);

  if (!hasHydrated || !isAuthenticated) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-bg-primary">
        <div className="w-12 h-12 rounded-xl gradient-accent flex items-center justify-center animate-pulse shadow-lg shadow-accent-primary/30">
          <span className="text-white font-bold text-xl">D</span>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen w-full bg-bg-primary overflow-hidden">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
      <CommandPalette />
    </div>
  );
}

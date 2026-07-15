"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/lib/stores/auth-store";
import { motion } from "framer-motion";

export default function RootPage() {
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const [hasHydrated, setHasHydrated] = useState(false);

  useEffect(() => {
    useAuthStore.persist.onFinishHydration(() => setHasHydrated(true));
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setHasHydrated(useAuthStore.persist.hasHydrated());
  }, []);

  useEffect(() => {
    if (hasHydrated) {
      if (isAuthenticated) {
        router.replace("/dashboard");
      } else {
        router.replace("/login");
      }
    }
  }, [isAuthenticated, hasHydrated, router]);
  return (
    <div className="min-h-screen bg-bg-primary flex flex-col items-center justify-center p-4">
      <motion.div
        animate={{ 
          scale: [1, 1.05, 1],
          opacity: [0.5, 1, 0.5] 
        }}
        transition={{ 
          duration: 2, 
          repeat: Infinity,
          ease: "easeInOut" 
        }}
        className="w-16 h-16 rounded-2xl gradient-accent flex items-center justify-center mb-6 shadow-2xl shadow-accent-primary/50"
      >
        <span className="text-white font-bold text-3xl">D</span>
      </motion.div>
      <h1 className="text-2xl font-bold text-gradient mb-2 tracking-tight">Dronzer AI Gateway</h1>
      <p className="text-text-tertiary text-sm animate-pulse">Initializing workspace...</p>
    </div>
  );
}

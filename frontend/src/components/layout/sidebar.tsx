"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAppStore } from "@/lib/stores/app-store";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Building2,
  FolderKanban,
  Key,
  Cloud,
  Brain,
  Puzzle,
  MessageSquare,
  PanelLeftClose,
  PanelLeftOpen,
  ShieldCheck,
  BookOpen,
} from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";

const navItems = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Organizations", href: "/dashboard/organizations", icon: Building2 },
  { name: "Projects", href: "/dashboard/projects", icon: FolderKanban },
  { name: "Gateway Keys", href: "/dashboard/gateway-keys", icon: ShieldCheck },
  { name: "Provider Credentials", href: "/dashboard/api-keys", icon: Key },
  { name: "AI Providers", href: "/dashboard/providers", icon: Cloud },
  { name: "Models", href: "/dashboard/models", icon: Brain },
  { name: "Plugins", href: "/dashboard/plugins", icon: Puzzle },
  { name: "Docs", href: "/dashboard/docs", icon: BookOpen },
  { name: "Playground", href: "/dashboard/playground", icon: MessageSquare },
];

export function Sidebar() {
  const pathname = usePathname();
  const { sidebarCollapsed, toggleSidebar } = useAppStore();

  return (
    <motion.aside
      initial={false}
      animate={{ width: sidebarCollapsed ? 72 : 260 }}
      className="h-full glass-card border-y-0 border-l-0 rounded-none border-r border-border-primary flex flex-col z-20 shrink-0 overflow-hidden"
    >
      {/* Logo Area */}
      <div className="h-16 flex items-center px-4 border-b border-border-primary shrink-0">
        <div className="w-8 h-8 rounded-lg gradient-accent flex items-center justify-center shrink-0">
          <span className="text-white font-bold text-sm">D</span>
        </div>
        <AnimatePresence>
          {!sidebarCollapsed && (
            <motion.span
              initial={{ opacity: 0, width: 0 }}
              animate={{ opacity: 1, width: "auto" }}
              exit={{ opacity: 0, width: 0 }}
              className="ml-3 font-semibold text-text-primary whitespace-nowrap overflow-hidden"
            >
              Dronzer Gateway
            </motion.span>
          )}
        </AnimatePresence>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center px-3 py-2.5 rounded-lg transition-all group relative overflow-hidden",
                isActive
                  ? "bg-accent-muted text-accent-primary"
                  : "text-text-secondary hover:bg-bg-elevated hover:text-text-primary"
              )}
              title={sidebarCollapsed ? item.name : undefined}
            >
              {isActive && (
                <motion.div
                  layoutId="sidebar-active-indicator"
                  className="absolute left-0 top-0 bottom-0 w-1 bg-accent-primary rounded-r-full"
                />
              )}
              <item.icon className={cn("w-5 h-5 shrink-0", isActive ? "text-accent-primary" : "text-text-secondary group-hover:text-text-primary")} />
              
              <AnimatePresence>
                {!sidebarCollapsed && (
                  <motion.span
                    initial={{ opacity: 0, width: 0 }}
                    animate={{ opacity: 1, width: "auto" }}
                    exit={{ opacity: 0, width: 0 }}
                    className="ml-3 whitespace-nowrap text-sm font-medium"
                  >
                    {item.name}
                  </motion.span>
                )}
              </AnimatePresence>
            </Link>
          );
        })}
      </div>

      {/* Bottom Section */}
      <div className="p-4 border-t border-border-primary flex flex-col gap-4">
        {/* System Health */}
        <div className={cn("flex items-center", sidebarCollapsed ? "justify-center" : "px-2")}>
          <div className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-success opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-success"></span>
          </div>
          <AnimatePresence>
            {!sidebarCollapsed && (
              <motion.span
                initial={{ opacity: 0, width: 0 }}
                animate={{ opacity: 1, width: "auto" }}
                exit={{ opacity: 0, width: 0 }}
                className="ml-3 text-xs font-medium text-text-secondary whitespace-nowrap"
              >
                System Healthy
              </motion.span>
            )}
          </AnimatePresence>
        </div>

        {/* Collapse Toggle */}
        <button
          onClick={toggleSidebar}
          className={cn(
            "flex items-center justify-center p-2 rounded-lg text-text-tertiary hover:bg-bg-elevated hover:text-text-primary transition-colors",
            !sidebarCollapsed && "self-end"
          )}
          title={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {sidebarCollapsed ? <PanelLeftOpen className="w-5 h-5" /> : <PanelLeftClose className="w-5 h-5" />}
        </button>
      </div>
    </motion.aside>
  );
}

"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import * as Dialog from "@radix-ui/react-dialog";
import { Search, LayoutDashboard, Building2, FolderKanban, Key, Cloud, Brain, Puzzle, MessageSquare, ShieldCheck } from "lucide-react";
import { cn } from "@/lib/utils";

const items = [
  { name: "Dashboard Overview", href: "/dashboard", icon: LayoutDashboard },
  { name: "Manage Organizations", href: "/dashboard/organizations", icon: Building2 },
  { name: "Manage Projects", href: "/dashboard/projects", icon: FolderKanban },
  { name: "Gateway Keys", href: "/dashboard/gateway-keys", icon: ShieldCheck },
  { name: "Provider Credentials", href: "/dashboard/api-keys", icon: Key },
  { name: "AI Providers", href: "/dashboard/providers", icon: Cloud },
  { name: "Models & Routing", href: "/dashboard/models", icon: Brain },
  { name: "Plugins", href: "/dashboard/plugins", icon: Puzzle },
  { name: "Playground", href: "/dashboard/playground", icon: MessageSquare },
];

export function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [activeIndex, setActiveIndex] = useState(0);
  const router = useRouter();
  const listRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener("keydown", down);
    
    const handleCustomEvent = () => setOpen(true);
    window.addEventListener("open-command-palette", handleCustomEvent);
    
    return () => {
      document.removeEventListener("keydown", down);
      window.removeEventListener("open-command-palette", handleCustomEvent);
    };
  }, []);

  const filteredItems = items.filter((item) =>
    item.name.toLowerCase().includes(query.toLowerCase())
  );

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActiveIndex((i) => (i + 1) % filteredItems.length);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActiveIndex((i) => (i - 1 + filteredItems.length) % filteredItems.length);
    } else if (e.key === "Enter" && filteredItems[activeIndex]) {
      e.preventDefault();
      router.push(filteredItems[activeIndex].href);
      setOpen(false);
    }
  };

  return (
    <Dialog.Root open={open} onOpenChange={(val) => {
      setOpen(val);
      if (!val) setQuery("");
    }}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-bg-overlay backdrop-blur-sm z-50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
        <Dialog.Content 
          className="fixed left-1/2 top-[15%] -translate-x-1/2 z-50 w-full max-w-xl glass-card-hover p-0 overflow-hidden shadow-2xl data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95"
        >
          <div className="flex items-center px-4 py-3 border-b border-border-primary">
            <Search className="w-5 h-5 text-text-tertiary mr-3 shrink-0" />
            <input
              autoFocus
              className="flex-1 bg-transparent border-none outline-none text-text-primary placeholder:text-text-muted text-base"
              placeholder="Search pages and settings..."
              value={query}
              onChange={(e) => {
                setQuery(e.target.value);
                setActiveIndex(0);
              }}
              onKeyDown={handleKeyDown}
            />
            <kbd className="hidden sm:inline-flex items-center gap-1 px-1.5 rounded bg-bg-elevated font-mono text-[10px] font-medium text-text-muted ml-2">
              ESC
            </kbd>
          </div>
          
          <div className="max-h-[300px] overflow-y-auto p-2" ref={listRef}>
            {filteredItems.length === 0 ? (
              <div className="py-14 text-center text-sm text-text-muted">
                No results found for &quot;{query}&quot;
              </div>
            ) : (
              <div className="flex flex-col gap-1">
                {filteredItems.map((item, i) => (
                  <button
                    key={item.href}
                    onClick={() => {
                      router.push(item.href);
                      setOpen(false);
                    }}
                    onMouseEnter={() => setActiveIndex(i)}
                    className={cn(
                      "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors w-full text-left",
                      i === activeIndex ? "bg-accent-muted text-accent-primary" : "text-text-secondary hover:bg-bg-elevated hover:text-text-primary"
                    )}
                  >
                    <item.icon className={cn("w-5 h-5", i === activeIndex ? "text-accent-primary" : "text-text-tertiary")} />
                    <div className="flex flex-col flex-1">
                      <span className="text-sm font-medium">{item.name}</span>
                      <span className="text-xs text-text-muted font-mono">{item.href}</span>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

"use client";

import { motion } from "framer-motion";
import { Puzzle, RefreshCw, Gauge, Filter, BarChart3, Database, User } from "lucide-react";
import { usePlugins, useReloadPlugins } from "@/lib/hooks/use-plugins";
import { EmptyState } from "@/components/ui/empty-state";
import { SkeletonCard } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

const getPluginIcon = (name: string) => {
  const lower = name.toLowerCase();
  if (lower.includes('rate')) return Gauge;
  if (lower.includes('filter')) return Filter;
  if (lower.includes('analytic')) return BarChart3;
  if (lower.includes('cache')) return Database;
  return Puzzle;
};

export default function PluginsPage() {
  const { data: plugins, isLoading } = usePlugins();
  const reloadPlugins = useReloadPlugins();

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row gap-4 sm:items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-text-primary tracking-tight">Plugins</h2>
          <p className="text-sm text-text-secondary mt-1">Manage system plugins for middleware and routing.</p>
        </div>
        <button 
          onClick={() => reloadPlugins.mutate()}
          disabled={reloadPlugins.isPending}
          className="h-10 px-4 rounded-lg bg-bg-elevated border border-border-primary text-text-primary text-sm font-medium flex items-center gap-2 hover:bg-bg-card-hover hover:border-border-secondary transition-all disabled:opacity-50"
        >
          <RefreshCw className={cn("w-4 h-4 text-text-secondary", reloadPlugins.isPending && "animate-spin text-accent-primary")} />
          Reload Plugins
        </button>
      </div>

      {/* Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      ) : !plugins || plugins.length === 0 ? (
        <EmptyState 
          icon={Puzzle}
          title="No plugins found"
          description="Your gateway has no plugins active. Check the backend plugin directory."
        />
      ) : (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {plugins.map((plugin, i) => {
            const Icon = getPluginIcon(plugin.name);
            
            return (
              <motion.div 
                key={plugin.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="glass-card hover:glass-card-hover p-6 flex flex-col transition-all group"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-accent-muted flex items-center justify-center border border-accent-primary/20 text-accent-primary">
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-text-primary text-base truncate max-w-[200px]">{plugin.name}</h3>
                      <div className="mt-1">
                        <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] uppercase font-bold bg-accent-muted text-accent-primary tracking-wider">
                          v{plugin.version}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="space-y-3 flex-1">
                  <p className="text-sm text-text-tertiary line-clamp-2 leading-relaxed">
                    {plugin.description || "No description provided."}
                  </p>
                  
                  <div className="pt-4 mt-4 border-t border-border-primary flex items-center gap-2 text-xs text-text-secondary">
                    <User className="w-3.5 h-3.5 text-text-tertiary" />
                    <span className="truncate">{plugin.author || "Unknown"}</span>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </motion.div>
      )}
    </div>
  );
}

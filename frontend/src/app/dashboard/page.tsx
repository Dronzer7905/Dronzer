"use client";

import Link from "next/link";
import { motion, type Variants } from "framer-motion";
import { 
  Activity, Coins, Zap, ShieldAlert, 
  Cloud, Puzzle, Clock, Database, 
  Server, ArrowRight, Building2, Brain, MessageSquare
} from "lucide-react";
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, 
  Tooltip as RechartsTooltip, ResponsiveContainer 
} from "recharts";
import { useHealthMetrics, useHealthDiagnostics, useLiveness } from "@/lib/hooks/use-health";
import { SkeletonStatCard, SkeletonCard, SkeletonLine } from "@/components/ui/skeleton";
import { StatusPill } from "@/components/ui/status-pill";



const containerVariants: Variants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } }
};

export default function DashboardOverviewPage() {
  const { data: metrics, isLoading: loadingMetrics } = useHealthMetrics();
  const { data: diagnostics, isLoading: loadingDiagnostics } = useHealthDiagnostics();
  const { data: liveness, isLoading: loadingLiveness } = useLiveness();

  const formatUptime = (seconds: number) => {
    const d = Math.floor(seconds / (3600 * 24));
    const h = Math.floor((seconds % (3600 * 24)) / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    return `${d}d ${h}h ${m}m`;
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
    if (num >= 1000) return (num / 1000).toFixed(1) + "K";
    return num.toString();
  };

  const isHealthy = liveness?.status === "alive";

  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="show"
      className="max-w-7xl mx-auto space-y-6 pb-12"
    >
      {/* Header */}
      <motion.div variants={itemVariants} className="flex flex-col gap-1 md:flex-row md:items-end justify-between">
        <div>
          <h2 className="text-2xl font-bold text-text-primary tracking-tight">Dashboard</h2>
          <p className="text-text-secondary mt-1">Welcome back. Here&apos;s your system overview.</p>
        </div>
        <div className="text-sm font-medium text-text-tertiary bg-bg-elevated px-3 py-1.5 rounded-lg border border-border-primary inline-flex w-fit mt-4 md:mt-0">
          {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
        {loadingMetrics ? (
          Array.from({ length: 4 }).map((_, i) => <SkeletonStatCard key={i} />)
        ) : (
          <>
            <motion.div variants={itemVariants} whileHover={{ y: -4 }} className="glass-card p-6">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm font-medium text-text-secondary">Active Requests</span>
                <div className="w-10 h-10 rounded-xl bg-info-muted flex items-center justify-center text-info">
                  <Activity className="w-5 h-5" />
                </div>
              </div>
              <div className="text-3xl font-bold text-text-primary mb-1">
                {formatNumber(metrics?.active_requests ?? 0)}
              </div>
              <div className="text-xs text-text-tertiary">Current live connections</div>
            </motion.div>

            <motion.div variants={itemVariants} whileHover={{ y: -4 }} className="glass-card p-6">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm font-medium text-text-secondary">Total Token Usage</span>
                <div className="w-10 h-10 rounded-xl bg-accent-muted flex items-center justify-center text-accent-primary">
                  <Coins className="w-5 h-5" />
                </div>
              </div>
              <div className="text-3xl font-bold text-text-primary mb-1">
                {formatNumber(metrics?.token_usage_total ?? 0)}
              </div>
              <div className="text-xs text-text-tertiary">Across all active models</div>
            </motion.div>

            <motion.div variants={itemVariants} whileHover={{ y: -4 }} className="glass-card p-6">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm font-medium text-text-secondary">Cache Hit Rate</span>
                <div className="w-10 h-10 rounded-xl bg-success-muted flex items-center justify-center text-success">
                  <Zap className="w-5 h-5" />
                </div>
              </div>
              <div className="text-3xl font-bold text-text-primary mb-1">
                {((metrics?.cache_hit_rate ?? 0) * 100).toFixed(1)}%
              </div>
              <div className="w-full bg-bg-elevated h-1.5 rounded-full mt-3 overflow-hidden">
                <div 
                  className="bg-success h-full rounded-full" 
                  style={{ width: `${(metrics?.cache_hit_rate ?? 0) * 100}%` }} 
                />
              </div>
            </motion.div>

            <motion.div variants={itemVariants} whileHover={{ y: -4 }} className="glass-card p-6">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm font-medium text-text-secondary">Circuit Breakers</span>
                <div className="w-10 h-10 rounded-xl bg-warning-muted flex items-center justify-center text-warning">
                  <ShieldAlert className="w-5 h-5" />
                </div>
              </div>
              <div className="text-3xl font-bold text-text-primary mb-1 flex items-baseline gap-2">
                {metrics?.circuit_breakers_open ?? 0}
                <span className="text-sm font-medium text-text-tertiary">/ {metrics?.circuit_breakers_half_open ?? 0}</span>
              </div>
              <div className="text-xs text-text-tertiary">Open / Half-open</div>
            </motion.div>
          </>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Activity Chart */}
        <motion.div variants={itemVariants} className="lg:col-span-2 glass-card p-6">
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-text-primary">System Activity</h3>
            <p className="text-sm text-text-tertiary">Request volume over the last 24 hours</p>
          </div>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={metrics?.timeseries || []} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorRequests" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--color-accent-primary)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--color-accent-primary)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-primary)" vertical={false} />
                <XAxis 
                  dataKey="time" 
                  stroke="var(--color-text-tertiary)" 
                  fontSize={12} 
                  tickLine={false} 
                  axisLine={false}
                  dy={10}
                />
                <YAxis 
                  stroke="var(--color-text-tertiary)" 
                  fontSize={12} 
                  tickLine={false} 
                  axisLine={false}
                  tickFormatter={(value) => `${value}`}
                  dx={-10}
                />
                <RechartsTooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(20, 24, 34, 0.9)', 
                    borderColor: 'var(--color-border-primary)',
                    borderRadius: '8px',
                    boxShadow: '0 4px 20px rgba(0,0,0,0.4)'
                  }}
                  itemStyle={{ color: 'var(--color-text-primary)' }}
                />
                <Area 
                  type="monotone" 
                  dataKey="requests" 
                  stroke="var(--color-accent-primary)" 
                  strokeWidth={2}
                  fillOpacity={1} 
                  fill="url(#colorRequests)" 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* System Health */}
        <motion.div variants={itemVariants} className="glass-card p-6 flex flex-col">
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-text-primary">System Health</h3>
            <p className="text-sm text-text-tertiary">Diagnostic overview</p>
          </div>
          
          {loadingDiagnostics || loadingLiveness ? (
            <div className="space-y-4">
              <SkeletonLine />
              <SkeletonLine />
              <SkeletonLine />
              <SkeletonLine />
            </div>
          ) : (
            <div className="flex flex-col gap-6 flex-1">
              {/* Infrastructure */}
              <div className="space-y-4">
                <h4 className="text-xs font-semibold uppercase tracking-wider text-text-tertiary mb-2">Infrastructure</h4>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-bg-elevated"><Server className="w-4 h-4 text-text-secondary" /></div>
                    <span className="text-sm font-medium text-text-secondary">Gateway Core</span>
                  </div>
                  <StatusPill status={isHealthy ? "healthy" : "error"} />
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-bg-elevated"><Database className="w-4 h-4 text-text-secondary" /></div>
                    <span className="text-sm font-medium text-text-secondary">PostgreSQL</span>
                  </div>
                  <StatusPill status={diagnostics?.database === "healthy" ? "healthy" : "error"} />
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-bg-elevated"><Database className="w-4 h-4 text-text-secondary" /></div>
                    <span className="text-sm font-medium text-text-secondary">Redis Cache</span>
                  </div>
                  <StatusPill status={diagnostics?.redis === "healthy" ? "healthy" : "error"} />
                </div>
              </div>
              
              <div className="h-px w-full bg-border-primary" />
              
              {/* Platform */}
              <div className="space-y-4">
                <h4 className="text-xs font-semibold uppercase tracking-wider text-text-tertiary mb-2">Platform</h4>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-bg-elevated"><Cloud className="w-4 h-4 text-text-secondary" /></div>
                    <span className="text-sm font-medium text-text-secondary">Providers Loaded</span>
                  </div>
                  <span className="text-sm font-bold text-text-primary">{diagnostics?.providers_loaded ?? 0}</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-bg-elevated"><Puzzle className="w-4 h-4 text-text-secondary" /></div>
                    <span className="text-sm font-medium text-text-secondary">Plugins Active</span>
                  </div>
                  <span className="text-sm font-bold text-text-primary">{diagnostics?.plugins_loaded ?? 0}</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-bg-elevated"><Clock className="w-4 h-4 text-text-secondary" /></div>
                    <span className="text-sm font-medium text-text-secondary">Uptime</span>
                  </div>
                  <span className="text-sm font-mono text-text-primary">{formatUptime(diagnostics?.uptime_seconds ?? 0)}</span>
                </div>
              </div>
            </div>
          )}
        </motion.div>
      </div>

      {/* Quick Actions */}
      <motion.div variants={itemVariants}>
        <h3 className="text-lg font-semibold text-text-primary mb-4 mt-2">Quick Actions</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link href="/dashboard/organizations" className="glass-card hover:glass-card-hover p-5 flex items-center justify-between group transition-all">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-xl bg-bg-elevated flex items-center justify-center text-text-secondary group-hover:text-accent-primary group-hover:bg-accent-muted transition-colors">
                <Building2 className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-semibold text-text-primary">Organizations</h4>
                <p className="text-xs text-text-tertiary">Manage tenants</p>
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-text-tertiary opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all text-accent-primary" />
          </Link>

          <Link href="/dashboard/providers" className="glass-card hover:glass-card-hover p-5 flex items-center justify-between group transition-all">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-xl bg-bg-elevated flex items-center justify-center text-text-secondary group-hover:text-accent-primary group-hover:bg-accent-muted transition-colors">
                <Cloud className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-semibold text-text-primary">AI Providers</h4>
                <p className="text-xs text-text-tertiary">Configure endpoints</p>
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-text-tertiary opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all text-accent-primary" />
          </Link>

          <Link href="/dashboard/models" className="glass-card hover:glass-card-hover p-5 flex items-center justify-between group transition-all">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-xl bg-bg-elevated flex items-center justify-center text-text-secondary group-hover:text-accent-primary group-hover:bg-accent-muted transition-colors">
                <Brain className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-semibold text-text-primary">Models</h4>
                <p className="text-xs text-text-tertiary">Routing & limits</p>
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-text-tertiary opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all text-accent-primary" />
          </Link>

          <Link href="/dashboard/playground" className="glass-card hover:glass-card-hover p-5 flex items-center justify-between group transition-all">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-xl bg-bg-elevated flex items-center justify-center text-text-secondary group-hover:text-accent-primary group-hover:bg-accent-muted transition-colors">
                <MessageSquare className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-semibold text-text-primary">Playground</h4>
                <p className="text-xs text-text-tertiary">Test completions</p>
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-text-tertiary opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all text-accent-primary" />
          </Link>
        </div>
      </motion.div>
    </motion.div>
  );
}

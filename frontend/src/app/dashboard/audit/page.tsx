"use client"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Search, Filter, Download, ShieldAlert } from "lucide-react"

const logs = [
  { id: "evt-001", user: "admin@dronzer.ai", action: "API Key Revoked", target: "key-9012", time: "2026-07-08 19:22:00", status: "success" },
  { id: "evt-002", user: "system", action: "Provider Disabled", target: "Google Gemini", time: "2026-07-08 18:45:12", status: "success" },
  { id: "evt-003", user: "bob@acme.com", action: "Failed Login", target: "Dashboard", time: "2026-07-08 14:20:00", status: "failure" },
]

export default function AuditPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Audit Logs</h2>
          <p className="text-muted-foreground">
            Immutable record of all configuration changes and security events.
          </p>
        </div>
        <Button variant="outline" className="gap-2">
          <Download className="h-4 w-4" /> Export CSV
        </Button>
      </div>

      <div className="flex items-center gap-4 bg-card p-2 rounded-lg border">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input placeholder="Search actions, users, or targets..." className="pl-9 border-0 bg-transparent focus-visible:ring-0" />
        </div>
        <div className="h-6 w-px bg-border"></div>
        <Button variant="ghost" size="sm" className="gap-2">
          <Filter className="h-4 w-4" /> Filter
        </Button>
      </div>

      <Card>
        <CardContent className="p-0">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-muted-foreground bg-muted/50 border-b">
              <tr>
                <th className="px-6 py-3 font-medium">Timestamp</th>
                <th className="px-6 py-3 font-medium">User</th>
                <th className="px-6 py-3 font-medium">Action</th>
                <th className="px-6 py-3 font-medium">Target</th>
                <th className="px-6 py-3 font-medium text-right">Status</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id} className="border-b last:border-0 hover:bg-muted/30 transition-colors">
                  <td className="px-6 py-4 font-mono text-xs">{log.time}</td>
                  <td className="px-6 py-4">{log.user}</td>
                  <td className="px-6 py-4 font-medium flex items-center gap-2">
                    {log.status === "failure" && <ShieldAlert className="h-4 w-4 text-red-500" />}
                    {log.action}
                  </td>
                  <td className="px-6 py-4">{log.target}</td>
                  <td className="px-6 py-4 text-right">
                    {log.status === "success" ? (
                      <span className="text-green-500 font-medium">Success</span>
                    ) : (
                      <span className="text-red-500 font-medium">Failed</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  )
}

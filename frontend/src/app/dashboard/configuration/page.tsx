"use client"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Settings, Save } from "lucide-react"

export default function ConfigurationPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Configuration Management</h2>
          <p className="text-muted-foreground">
            Manage global runtime settings, feature flags, and environment variables.
          </p>
        </div>
        <Button className="gap-2">
          <Save className="h-4 w-4" /> Save Config
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Settings className="h-5 w-5" />
              Global Settings
            </CardTitle>
            <CardDescription>Gateway-wide timeouts and retries.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <label className="text-sm font-medium">Default Request Timeout (ms)</label>
              <Input type="number" defaultValue={30000} />
            </div>
            <div className="grid gap-2">
              <label className="text-sm font-medium">Max Retries</label>
              <Input type="number" defaultValue={3} />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Settings className="h-5 w-5" />
              Feature Flags
            </CardTitle>
            <CardDescription>Toggle experimental features.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="font-medium text-sm">Semantic Caching</span>
              <span className="px-2 py-1 bg-green-500/10 text-green-500 rounded text-xs font-medium cursor-pointer">Enabled</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="font-medium text-sm">Vision Model Routing</span>
              <span className="px-2 py-1 bg-green-500/10 text-green-500 rounded text-xs font-medium cursor-pointer">Enabled</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="font-medium text-sm">Beta Tracing Analytics</span>
              <span className="px-2 py-1 bg-muted text-muted-foreground rounded text-xs font-medium cursor-pointer">Disabled</span>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

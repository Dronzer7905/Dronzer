"use client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Activity, BarChart2 } from "lucide-react"

export default function MetricsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Metrics & Observability</h2>
          <p className="text-muted-foreground">
            Deep dive into token usage, latency distribution, and cost analysis.
          </p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5" />
              Latency Percentiles
            </CardTitle>
          </CardHeader>
          <CardContent className="h-[300px] flex items-center justify-center border-t bg-muted/10">
            <p className="text-muted-foreground">Latency distribution charts will render here.</p>
          </CardContent>
        </Card>
        
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart2 className="h-5 w-5" />
              Token Usage by Model
            </CardTitle>
          </CardHeader>
          <CardContent className="h-[300px] flex items-center justify-center border-t bg-muted/10">
            <p className="text-muted-foreground">Token usage bar charts will render here.</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

"use client"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Route, Plus, ArrowRight, Play } from "lucide-react"

const policies = [
  { 
    id: "pol-1", 
    name: "Cost Optimization Route", 
    priority: 100,
    conditions: "Prompt length < 1000", 
    strategy: "Route to Groq Llama3" 
  },
  { 
    id: "pol-2", 
    name: "High Intelligence Route", 
    priority: 50,
    conditions: "Model == gpt-4o OR Requires Vision", 
    strategy: "Route to OpenAI" 
  },
  { 
    id: "pol-3", 
    name: "Default Fallback", 
    priority: 0,
    conditions: "Catch-all", 
    strategy: "Load Balance (Anthropic, Gemini)" 
  }
]

export default function RoutingPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Routing Policies</h2>
          <p className="text-muted-foreground">
            Configure dynamic routing rules, load balancing, and failover strategies.
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="gap-2">
            <Play className="h-4 w-4" /> Simulate
          </Button>
          <Button className="gap-2">
            <Plus className="h-4 w-4" /> New Policy
          </Button>
        </div>
      </div>

      <div className="grid gap-4">
        {policies.map((policy) => (
          <Card key={policy.id} className="relative overflow-hidden">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary"></div>
            <CardContent className="flex items-center justify-between p-6 pl-8">
              <div className="grid gap-1 flex-1">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-lg">{policy.name}</h3>
                  <span className="px-2 py-0.5 bg-muted rounded text-xs font-medium">Priority: {policy.priority}</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-muted-foreground mt-2">
                  <div className="px-2 py-1 bg-secondary rounded text-secondary-foreground">
                    IF {policy.conditions}
                  </div>
                  <ArrowRight className="h-4 w-4" />
                  <div className="px-2 py-1 border rounded text-foreground font-medium">
                    THEN {policy.strategy}
                  </div>
                </div>
              </div>
              <div className="flex gap-2">
                <Button variant="ghost" size="sm">Edit</Button>
                <Button variant="ghost" size="sm" className="text-red-500 hover:text-red-600">Delete</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

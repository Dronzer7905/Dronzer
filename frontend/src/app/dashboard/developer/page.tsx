"use client"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Code2, Play, Terminal } from "lucide-react"

export default function DeveloperPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Developer Tools</h2>
          <p className="text-muted-foreground">
            API Explorer, Request Inspector, and Routing Simulation.
          </p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle className="text-lg">Endpoints</CardTitle>
            <CardDescription>Interactive API documentation.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="p-2 bg-muted/50 rounded font-mono text-xs flex justify-between cursor-pointer hover:bg-muted">
              <span className="text-green-500 font-bold">POST</span>
              <span>/v1/chat/completions</span>
            </div>
            <div className="p-2 bg-muted/50 rounded font-mono text-xs flex justify-between cursor-pointer hover:bg-muted">
              <span className="text-green-500 font-bold">POST</span>
              <span>/v1/embeddings</span>
            </div>
            <div className="p-2 bg-muted/50 rounded font-mono text-xs flex justify-between cursor-pointer hover:bg-muted">
              <span className="text-blue-500 font-bold">GET</span>
              <span>/v1/models</span>
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle className="text-lg flex items-center gap-2">
                <Terminal className="h-5 w-5" /> API Playground
              </CardTitle>
              <CardDescription>Test gateway endpoints directly.</CardDescription>
            </div>
            <Button size="sm" className="gap-2 bg-green-600 hover:bg-green-700 text-white">
              <Play className="h-4 w-4" /> Send Request
            </Button>
          </CardHeader>
          <CardContent>
            <div className="bg-black/90 p-4 rounded-md font-mono text-sm text-green-400 overflow-x-auto min-h-[300px]">
              {`{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": "Hello, AI Gateway!"
    }
  ],
  "stream": false
}`}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

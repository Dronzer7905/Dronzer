export default function WorkflowBuilder() {
  return (
    <div className="flex h-screen flex-col">
      <div className="border-b px-6 py-4 flex items-center justify-between bg-background">
        <h2 className="text-xl font-bold">Visual Workflow Builder</h2>
        <div className="space-x-2">
          <button className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm">Save Draft</button>
          <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium">Deploy</button>
        </div>
      </div>
      
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar - Node Palette */}
        <div className="w-64 border-r bg-muted/30 p-4 overflow-y-auto">
          <h3 className="font-semibold mb-4 text-sm uppercase text-muted-foreground tracking-wider">Nodes</h3>
          
          <div className="space-y-2">
            <div className="p-3 border rounded-md bg-card cursor-grab shadow-sm">
              <div className="font-medium text-sm">LLM Node</div>
              <div className="text-xs text-muted-foreground mt-1">Generate text via API</div>
            </div>
            
            <div className="p-3 border rounded-md bg-card cursor-grab shadow-sm">
              <div className="font-medium text-sm">HTTP Request</div>
              <div className="text-xs text-muted-foreground mt-1">Fetch or post data</div>
            </div>
            
            <div className="p-3 border rounded-md bg-card cursor-grab shadow-sm border-blue-500/30">
              <div className="font-medium text-sm">Human Approval</div>
              <div className="text-xs text-muted-foreground mt-1">Pause for manual review</div>
            </div>
            
            <div className="p-3 border rounded-md bg-card cursor-grab shadow-sm border-purple-500/30">
              <div className="font-medium text-sm">Agent Orchestrator</div>
              <div className="text-xs text-muted-foreground mt-1">Delegate to sub-agents</div>
            </div>
          </div>
        </div>
        
        {/* Main Canvas Area (Placeholder for React Flow) */}
        <div className="flex-1 bg-dot-pattern bg-[length:20px_20px] bg-muted/10 relative">
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <p className="text-muted-foreground text-sm font-medium bg-background/80 px-4 py-2 rounded-full backdrop-blur-sm border shadow-sm">
              React Flow Canvas Mount Point
            </p>
          </div>
          
          {/* Mock Node on Canvas */}
          <div className="absolute top-1/4 left-1/4 w-64 border rounded-lg bg-card shadow-lg overflow-hidden">
            <div className="bg-primary/10 px-4 py-2 border-b flex justify-between items-center">
              <span className="font-semibold text-sm">Customer Support Agent</span>
              <div className="w-2 h-2 rounded-full bg-green-500"></div>
            </div>
            <div className="p-4 space-y-3">
              <div className="text-xs">
                <span className="text-muted-foreground">Model:</span> gpt-4-turbo
              </div>
              <div className="text-xs">
                <span className="text-muted-foreground">Tools:</span> Search, Database, RefundAPI
              </div>
            </div>
          </div>
        </div>
        
        {/* Right Sidebar - Properties */}
        <div className="w-80 border-l bg-background p-4 overflow-y-auto">
          <h3 className="font-semibold mb-4 text-sm uppercase text-muted-foreground tracking-wider">Properties</h3>
          <p className="text-sm text-muted-foreground">Select a node to configure its parameters and RBAC permissions.</p>
        </div>
      </div>
    </div>
  )
}

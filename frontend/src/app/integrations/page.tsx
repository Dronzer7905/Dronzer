export default function IntegrationHub() {
  return (
    <div className="container mx-auto p-8 max-w-6xl">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Integration Hub</h1>
          <p className="text-muted-foreground mt-1">Manage MCP Servers, Connectors, and Tool Metrics</p>
        </div>
        <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md font-medium shadow-sm">
          + Add Integration
        </button>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="border rounded-xl p-5 bg-card shadow-sm">
          <div className="text-sm font-medium text-muted-foreground">Active Connectors</div>
          <div className="text-3xl font-bold mt-2">12</div>
        </div>
        <div className="border rounded-xl p-5 bg-card shadow-sm">
          <div className="text-sm font-medium text-muted-foreground">Available Tools</div>
          <div className="text-3xl font-bold mt-2">142</div>
        </div>
        <div className="border rounded-xl p-5 bg-card shadow-sm">
          <div className="text-sm font-medium text-muted-foreground">24h Tool Executions</div>
          <div className="text-3xl font-bold mt-2">1.2M</div>
        </div>
        <div className="border rounded-xl p-5 bg-card shadow-sm">
          <div className="text-sm font-medium text-muted-foreground">Avg Latency</div>
          <div className="text-3xl font-bold mt-2 text-green-600">84ms</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b mb-6">
        <div className="flex space-x-8">
          <div className="border-b-2 border-primary pb-3 font-medium cursor-pointer">MCP Servers</div>
          <div className="pb-3 text-muted-foreground hover:text-foreground cursor-pointer">Local Connectors</div>
          <div className="pb-3 text-muted-foreground hover:text-foreground cursor-pointer">Sandboxed Runtimes</div>
          <div className="pb-3 text-muted-foreground hover:text-foreground cursor-pointer">Metrics</div>
        </div>
      </div>

      {/* MCP Servers List */}
      <div className="space-y-4">
        {/* Item 1 */}
        <div className="border rounded-lg p-5 flex justify-between items-center bg-card shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center space-x-4">
            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold">
              DB
            </div>
            <div>
              <h3 className="font-semibold text-lg">Enterprise Data Lake (MCP)</h3>
              <p className="text-sm text-muted-foreground">sse://mcp.internal.corp/v1/stream</p>
            </div>
          </div>
          <div className="flex items-center space-x-6">
            <div className="text-right">
              <div className="text-sm font-medium">42 Tools</div>
              <div className="text-xs text-muted-foreground">Synced 2m ago</div>
            </div>
            <div className="px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-medium">Connected</div>
            <button className="text-muted-foreground hover:text-foreground">⋮</button>
          </div>
        </div>
        
        {/* Item 2 */}
        <div className="border rounded-lg p-5 flex justify-between items-center bg-card shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center space-x-4">
            <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center text-purple-600 font-bold">
              SL
            </div>
            <div>
              <h3 className="font-semibold text-lg">Slack Automation (MCP)</h3>
              <p className="text-sm text-muted-foreground">stdio://usr/bin/slack-mcp</p>
            </div>
          </div>
          <div className="flex items-center space-x-6">
            <div className="text-right">
              <div className="text-sm font-medium">8 Tools</div>
              <div className="text-xs text-muted-foreground">Synced 1h ago</div>
            </div>
            <div className="px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-medium">Connected</div>
            <button className="text-muted-foreground hover:text-foreground">⋮</button>
          </div>
        </div>
      </div>
    </div>
  )
}

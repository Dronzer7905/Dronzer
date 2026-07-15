export default function FleetDashboard() {
  return (
    <div className="container mx-auto p-8 max-w-6xl">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Fleet Management</h1>
          <p className="text-muted-foreground mt-1">Multi-Region Clusters, Nodes, and Disaster Recovery</p>
        </div>
        <div className="flex space-x-3">
          <button className="border border-input bg-background hover:bg-accent text-accent-foreground px-4 py-2 rounded-md font-medium shadow-sm transition-colors">
            Trigger Failover
          </button>
          <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md font-medium shadow-sm">
            Deploy Cluster
          </button>
        </div>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="border rounded-xl p-5 bg-card shadow-sm">
          <div className="text-sm font-medium text-muted-foreground">Active Clusters</div>
          <div className="text-3xl font-bold mt-2">3</div>
        </div>
        <div className="border rounded-xl p-5 bg-card shadow-sm">
          <div className="text-sm font-medium text-muted-foreground">Global Nodes</div>
          <div className="text-3xl font-bold mt-2">124</div>
        </div>
        <div className="border rounded-xl p-5 bg-card shadow-sm">
          <div className="text-sm font-medium text-muted-foreground">Cross-Region Latency</div>
          <div className="text-3xl font-bold mt-2 text-green-600">32ms</div>
        </div>
        <div className="border rounded-xl p-5 bg-card shadow-sm">
          <div className="text-sm font-medium text-muted-foreground">Last DR Snapshot</div>
          <div className="text-3xl font-bold mt-2">4h ago</div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-8">
        {/* Main Content Area */}
        <div className="col-span-2 space-y-6">
          <h2 className="text-xl font-semibold">Geographical Deployment Map</h2>
          <div className="border rounded-xl p-8 bg-slate-50 flex items-center justify-center h-80">
            {/* Placeholder for actual interactive map / globe visualization */}
            <p className="text-muted-foreground">Global Traffic Map Loading...</p>
          </div>
          
          <h2 className="text-xl font-semibold mt-8 mb-4">Cluster Topology</h2>
          
          {/* Cluster List */}
          <div className="space-y-4">
            <div className="border rounded-lg p-5 flex justify-between items-center bg-card shadow-sm">
              <div>
                <h3 className="font-semibold text-lg flex items-center">
                  <span className="w-2 h-2 rounded-full bg-blue-500 mr-2"></span>
                  dronzer-us-east (AWS)
                </h3>
                <p className="text-sm text-muted-foreground mt-1">Role: PRIMARY • 45 Nodes</p>
              </div>
              <div className="text-right">
                <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-semibold mr-3">HEALTHY</span>
                <button className="text-sm font-medium text-blue-600 hover:underline">Manage</button>
              </div>
            </div>
            
            <div className="border rounded-lg p-5 flex justify-between items-center bg-card shadow-sm">
              <div>
                <h3 className="font-semibold text-lg flex items-center">
                  <span className="w-2 h-2 rounded-full bg-purple-500 mr-2"></span>
                  dronzer-eu-central (GCP)
                </h3>
                <p className="text-sm text-muted-foreground mt-1">Role: SECONDARY • 30 Nodes</p>
              </div>
              <div className="text-right">
                <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-semibold mr-3">SYNCED</span>
                <button className="text-sm font-medium text-blue-600 hover:underline">Manage</button>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar / Alerts */}
        <div className="space-y-6">
          <h2 className="text-xl font-semibold">Consensus & Locks</h2>
          <div className="border rounded-xl p-5 bg-card shadow-sm space-y-4">
            <div className="flex justify-between items-center border-b pb-3">
              <span className="text-sm font-medium">Scheduler Leader</span>
              <span className="text-xs bg-slate-100 px-2 py-1 rounded">node-us-east-1a-5f89</span>
            </div>
            <div className="flex justify-between items-center border-b pb-3">
              <span className="text-sm font-medium">Global Replicator</span>
              <span className="text-xs bg-slate-100 px-2 py-1 rounded">node-eu-cent-2c-112e</span>
            </div>
          </div>

          <h2 className="text-xl font-semibold mt-8">Recent Alerts</h2>
          <div className="border rounded-xl p-5 bg-card shadow-sm space-y-4">
            <div className="flex space-x-3 items-start">
              <div className="w-2 h-2 mt-1.5 rounded-full bg-yellow-500 flex-shrink-0"></div>
              <div>
                <p className="text-sm font-medium">Node Draining (us-east)</p>
                <p className="text-xs text-muted-foreground">Spot instance termination notice.</p>
                <p className="text-xs text-muted-foreground mt-1">2m ago</p>
              </div>
            </div>
            <div className="flex space-x-3 items-start">
              <div className="w-2 h-2 mt-1.5 rounded-full bg-green-500 flex-shrink-0"></div>
              <div>
                <p className="text-sm font-medium">Cross-Region Sync Complete</p>
                <p className="text-xs text-muted-foreground">GCP Replica caught up to AWS.</p>
                <p className="text-xs text-muted-foreground mt-1">15m ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

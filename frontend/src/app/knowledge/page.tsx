export default function KnowledgeDashboard() {
  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Knowledge Spaces</h2>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {/* Collection Status Card */}
        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="tracking-tight text-sm font-medium">Active Collections</h3>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" className="h-4 w-4 text-muted-foreground"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold">14</div>
            <p className="text-xs text-muted-foreground">across Qdrant & pgvector</p>
          </div>
        </div>

        {/* Embedded Vectors Card */}
        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="tracking-tight text-sm font-medium">Total Vectors</h3>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" className="h-4 w-4 text-muted-foreground"><rect width="20" height="14" x="2" y="5" rx="2"></rect><path d="M2 10h20"></path></svg>
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold">4.2M</div>
            <p className="text-xs text-muted-foreground">Using text-embedding-3-small</p>
          </div>
        </div>
        
        {/* Agent Memory Card */}
        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="tracking-tight text-sm font-medium">Agent Memory Sessions</h3>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" className="h-4 w-4 text-muted-foreground"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold">128</div>
            <p className="text-xs text-muted-foreground">Active long-term contexts</p>
          </div>
        </div>
      </div>
      
      {/* Knowledge Testing Interface */}
      <div className="mt-6 space-y-4">
        <h3 className="text-xl font-semibold">Retrieval Testing</h3>
        <p className="text-sm text-muted-foreground">Simulate Semantic and Hybrid searches against your collections here.</p>
        {/* Placeholder for Search Input and Reranker toggle */}
      </div>
    </div>
  )
}

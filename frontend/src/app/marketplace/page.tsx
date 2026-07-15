export default function MarketplaceHub() {
  return (
    <div className="container mx-auto p-8 max-w-6xl">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
            AI Marketplace
          </h1>
          <p className="text-muted-foreground mt-2 text-lg">Discover Plugins, Prompts, Agents, and Workflows</p>
        </div>
        <div className="flex space-x-3">
          <button className="border border-input bg-background hover:bg-accent text-accent-foreground px-4 py-2 rounded-md font-medium shadow-sm transition-colors">
            Publisher Portal
          </button>
          <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md font-medium shadow-sm">
            Import Air-Gapped Bundle
          </button>
        </div>
      </div>

      {/* Search Bar */}
      <div className="relative mb-10">
        <input 
          type="text" 
          placeholder="Search for @google, postgres-connector, or llama-3-prompts..." 
          className="w-full border-2 border-slate-200 rounded-xl p-4 pl-12 text-lg focus:outline-none focus:border-blue-500 shadow-sm transition-colors"
        />
        <svg className="w-6 h-6 text-slate-400 absolute left-4 top-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
      </div>

      <div className="flex gap-8">
        {/* Sidebar Filters */}
        <div className="w-64 flex-shrink-0">
          <h3 className="font-semibold mb-4 text-lg">Categories</h3>
          <ul className="space-y-3 text-muted-foreground">
            <li className="text-primary font-medium cursor-pointer">All Packages</li>
            <li className="cursor-pointer hover:text-foreground">Providers</li>
            <li className="cursor-pointer hover:text-foreground">Plugins & Tools</li>
            <li className="cursor-pointer hover:text-foreground">Workflow Templates</li>
            <li className="cursor-pointer hover:text-foreground">Agent Profiles</li>
            <li className="cursor-pointer hover:text-foreground">System Prompts</li>
          </ul>

          <h3 className="font-semibold mt-8 mb-4 text-lg">Verification</h3>
          <label className="flex items-center space-x-2 cursor-pointer">
            <input type="checkbox" className="rounded border-slate-300 text-blue-600" defaultChecked />
            <span>Verified Publishers Only</span>
          </label>
        </div>

        {/* Package Grid */}
        <div className="flex-1">
          <h2 className="text-2xl font-semibold mb-6">Trending this week</h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Package Card 1 */}
            <div className="border rounded-xl p-6 bg-card shadow-sm hover:shadow-md transition-shadow cursor-pointer relative overflow-hidden">
              <div className="absolute top-0 right-0 bg-blue-100 text-blue-700 text-xs font-bold px-3 py-1 rounded-bl-lg">PLUGIN</div>
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="font-bold text-xl text-blue-600">@core/playwright-engine</h3>
                  <p className="text-sm text-slate-500 mt-1 flex items-center">
                    by Dronzer Inc. 
                    <svg className="w-4 h-4 text-green-500 ml-1" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path></svg>
                  </p>
                </div>
              </div>
              <p className="text-muted-foreground text-sm mb-6 line-clamp-2">
                Headless browser automation connector. Allows Agents to scrape DOM, take screenshots, and fill dynamic web forms.
              </p>
              <div className="flex justify-between items-center text-sm font-medium">
                <span className="flex items-center text-yellow-500">
                  ★ 4.9 <span className="text-slate-400 ml-1 font-normal">(125k)</span>
                </span>
                <span className="text-slate-500">v1.2.4</span>
              </div>
            </div>

            {/* Package Card 2 */}
            <div className="border rounded-xl p-6 bg-card shadow-sm hover:shadow-md transition-shadow cursor-pointer relative overflow-hidden">
              <div className="absolute top-0 right-0 bg-purple-100 text-purple-700 text-xs font-bold px-3 py-1 rounded-bl-lg">PROMPT</div>
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="font-bold text-xl text-blue-600">@community/llama3-prompts</h3>
                  <p className="text-sm text-slate-500 mt-1">by AI Enthusiast</p>
                </div>
              </div>
              <p className="text-muted-foreground text-sm mb-6 line-clamp-2">
                Curated system prompts specifically optimized for Llama-3 70B Instruct. Includes personas for coding, writing, and logical deduction.
              </p>
              <div className="flex justify-between items-center text-sm font-medium">
                <span className="flex items-center text-yellow-500">
                  ★ 4.5 <span className="text-slate-400 ml-1 font-normal">(15k)</span>
                </span>
                <span className="text-slate-500">v2.0.1</span>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  )
}

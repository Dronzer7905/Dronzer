export default function PromptOpsLab() {
  return (
    <div className="container mx-auto p-8 max-w-7xl">
      {/* Header */}
      <div className="flex justify-between items-center mb-8 border-b pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            LLMOps & Prompt Lab
          </h1>
          <p className="text-muted-foreground mt-1">Manage Prompts, Evaluate Models, and Track A/B Experiments</p>
        </div>
        <div className="flex space-x-3">
          <button className="border border-input bg-background hover:bg-accent text-accent-foreground px-4 py-2 rounded-md font-medium shadow-sm transition-colors">
            Import Dataset
          </button>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium shadow-sm transition-colors">
            + New Prompt
          </button>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-8">
        
        {/* Left Sidebar - Collections */}
        <div className="col-span-3 border-r pr-6">
          <h3 className="font-semibold text-slate-800 mb-4 uppercase tracking-wider text-xs">Prompt Collections</h3>
          <ul className="space-y-1">
            <li className="px-3 py-2 bg-blue-50 text-blue-700 rounded-md font-medium cursor-pointer">
              Customer Support Bots
            </li>
            <li className="px-3 py-2 text-slate-600 hover:bg-slate-50 rounded-md cursor-pointer">
              Code Generation
            </li>
            <li className="px-3 py-2 text-slate-600 hover:bg-slate-50 rounded-md cursor-pointer">
              RAG Extractors
            </li>
          </ul>

          <h3 className="font-semibold text-slate-800 mt-8 mb-4 uppercase tracking-wider text-xs">Evaluation</h3>
          <ul className="space-y-1">
            <li className="px-3 py-2 text-slate-600 hover:bg-slate-50 rounded-md cursor-pointer flex justify-between items-center">
              Golden Datasets <span className="bg-slate-100 text-slate-500 px-2 py-0.5 rounded text-xs">12</span>
            </li>
            <li className="px-3 py-2 text-slate-600 hover:bg-slate-50 rounded-md cursor-pointer">
              LLM-as-a-Judge Runs
            </li>
          </ul>
        </div>

        {/* Main Content Area */}
        <div className="col-span-9">
          
          {/* Active Prompt Header */}
          <div className="flex justify-between items-start mb-6">
            <div>
              <div className="flex items-center space-x-3">
                <h2 className="text-2xl font-bold">Support-Bot-V2</h2>
                <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded font-medium border border-green-200">PUBLISHED</span>
              </div>
              <p className="text-slate-500 text-sm mt-1">Handles initial customer inquiries and routes to human agents.</p>
            </div>
            
            <div className="flex items-center space-x-2 text-sm bg-slate-50 border rounded-lg p-1">
              <button className="px-3 py-1.5 bg-white shadow-sm rounded font-medium">Editor</button>
              <button className="px-3 py-1.5 text-slate-600 hover:text-slate-900 font-medium">Compare</button>
              <button className="px-3 py-1.5 text-slate-600 hover:text-slate-900 font-medium">A/B Tests</button>
              <button className="px-3 py-1.5 text-slate-600 hover:text-slate-900 font-medium">Analytics</button>
            </div>
          </div>

          {/* Prompt Editor */}
          <div className="border rounded-xl shadow-sm bg-white overflow-hidden mb-8">
            <div className="bg-slate-50 border-b px-4 py-3 flex justify-between items-center">
              <div className="flex space-x-4 text-sm font-mono text-slate-500">
                <span><strong className="text-slate-700">Model:</strong> gpt-4o</span>
                <span><strong className="text-slate-700">Temp:</strong> 0.7</span>
                <span><strong className="text-slate-700">Version:</strong> v2.1.0-draft</span>
              </div>
              <button className="text-sm text-blue-600 font-medium hover:underline">View History</button>
            </div>
            
            <div className="p-0">
              <textarea 
                className="w-full h-64 p-4 font-mono text-sm focus:outline-none resize-none"
                defaultValue={`You are a helpful customer support agent for Dronzer.
The user is asking a question about our enterprise billing.

User Context:
Name: {{ user_name }}
Plan: {{ subscription_tier }}

{% if subscription_tier == 'Enterprise' %}
IMPORTANT: Treat this user with the highest priority. Offer them a direct link to book a meeting with their dedicated account manager.
{% endif %}

User Query:
{{ user_query }}

Provide a polite and helpful response:`}
              />
            </div>
            
            <div className="bg-slate-50 border-t px-4 py-3 flex justify-between items-center">
              <div className="flex gap-2">
                <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded font-mono">user_name</span>
                <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded font-mono">subscription_tier</span>
                <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded font-mono">user_query</span>
              </div>
              <div className="flex space-x-2">
                <button className="px-4 py-2 border rounded text-sm font-medium hover:bg-slate-50">Run Test</button>
                <button className="px-4 py-2 bg-blue-600 text-white rounded text-sm font-medium hover:bg-blue-700">Save Draft</button>
              </div>
            </div>
          </div>

          {/* Analytics Overview */}
          <div className="grid grid-cols-4 gap-4">
            <div className="border rounded-lg p-4 bg-white shadow-sm">
              <p className="text-slate-500 text-sm font-medium">Executions (7d)</p>
              <p className="text-2xl font-bold mt-1">45.2k</p>
              <p className="text-green-500 text-xs font-medium mt-1">↑ 12% from last week</p>
            </div>
            <div className="border rounded-lg p-4 bg-white shadow-sm">
              <p className="text-slate-500 text-sm font-medium">Avg Latency</p>
              <p className="text-2xl font-bold mt-1">850<span className="text-sm font-normal text-slate-500">ms</span></p>
            </div>
            <div className="border rounded-lg p-4 bg-white shadow-sm">
              <p className="text-slate-500 text-sm font-medium">Error Rate</p>
              <p className="text-2xl font-bold mt-1">1.2%</p>
            </div>
            <div className="border rounded-lg p-4 bg-white shadow-sm">
              <p className="text-slate-500 text-sm font-medium">Total Cost (7d)</p>
              <p className="text-2xl font-bold mt-1">$125.50</p>
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}

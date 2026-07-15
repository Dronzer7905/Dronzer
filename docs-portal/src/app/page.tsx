export default function DocsPortal() {
  return (
    <div className="container mx-auto p-12 max-w-5xl">
      <div className="text-center mb-16">
        <h1 className="text-5xl font-extrabold tracking-tight text-slate-900 mb-4">
          Dronzer Developer Documentation
        </h1>
        <p className="text-xl text-slate-500 max-w-2xl mx-auto">
          Build, deploy, and scale enterprise AI Workflows. Get started with our official SDKs, CLI, and APIs.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* SDK Card */}
        <div className="border rounded-xl p-6 hover:shadow-md transition-shadow cursor-pointer bg-white">
          <h3 className="text-xl font-bold mb-2 text-blue-600">Official SDKs</h3>
          <p className="text-slate-600 mb-4">Integrate Dronzer natively into your stack using Python, TypeScript, or Go.</p>
          <div className="flex space-x-2 text-sm font-medium text-slate-500">
            <span className="bg-slate-100 px-2 py-1 rounded">Python</span>
            <span className="bg-slate-100 px-2 py-1 rounded">TypeScript</span>
          </div>
        </div>

        {/* CLI Card */}
        <div className="border rounded-xl p-6 hover:shadow-md transition-shadow cursor-pointer bg-white">
          <h3 className="text-xl font-bold mb-2 text-blue-600">Dronzer CLI</h3>
          <p className="text-slate-600 mb-4">Manage deployments, Prompts, and Models directly from your terminal.</p>
          <code className="bg-slate-100 px-3 py-2 rounded text-sm text-pink-600 block">pip install dronzer-cli</code>
        </div>

        {/* API Reference Card */}
        <div className="border rounded-xl p-6 hover:shadow-md transition-shadow cursor-pointer bg-white">
          <h3 className="text-xl font-bold mb-2 text-blue-600">API Reference</h3>
          <p className="text-slate-600 mb-4">Explore the OpenAPI 3.1 specifications for the Dronzer Gateway.</p>
          <span className="text-blue-500 hover:underline text-sm font-medium">View Endpoints →</span>
        </div>

      </div>
    </div>
  )
}

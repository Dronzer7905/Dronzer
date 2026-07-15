const OpenAI = require("openai");

// ---------------------------------------------------------
// Dronzer AI Gateway - Node.js SDK Example
// ---------------------------------------------------------
// Dronzer is fully compliant with the OpenAI API specification.
// You can use the standard official OpenAI SDK simply by 
// changing the `baseURL` to point to your Dronzer instance.

const client = new OpenAI({
    apiKey: process.env.DRONZER_API_KEY || "sk-dronzer-test-key",
    baseURL: "http://localhost:8000/v1"
});

async function runChatCompletion() {
    console.log("--- Sending Chat Completion via Dronzer ---");
    
    try {
        // You can request ANY model supported by Dronzer's routing policies
        // (e.g. gpt-4o, claude-3-opus, gemini-1.5-pro, llama-3)
        const response = await client.chat.completions.create({
            model: "claude-3-opus", // Dronzer will seamlessly translate this payload for Anthropic!
            messages: [
                { role: "system", content: "You are a helpful AI assistant routed through Dronzer." },
                { role: "user", content: "Explain what an AI Gateway is in one sentence." }
            ],
            temperature: 0.7
        });
        
        console.log("\n[Response]");
        console.log(response.choices[0].message.content);
        
        console.log(`\n[Tokens Used]: ${response.usage.total_tokens}`);
    } catch (error) {
        console.error("Failed to connect to Dronzer Gateway:", error.message);
    }
}

runChatCompletion();

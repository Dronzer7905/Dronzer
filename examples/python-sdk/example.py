import os
from openai import OpenAI

# ---------------------------------------------------------
# Dronzer AI Gateway - Python SDK Example
# ---------------------------------------------------------
# Dronzer is fully compliant with the OpenAI API specification.
# You can use the standard official OpenAI SDK simply by 
# changing the `base_url` to point to your Dronzer instance.

# 1. Initialize client pointing to Dronzer
client = OpenAI(
    api_key=os.getenv("DRONZER_API_KEY", "sk-dronzer-test-key"),
    base_url="http://localhost:8000/v1"
)

def run_chat_completion():
    print("--- Sending Chat Completion via Dronzer ---")
    
    # You can request ANY model supported by Dronzer's routing policies
    # (e.g. gpt-4o, claude-3-opus, gemini-1.5-pro, llama-3)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant routed through Dronzer."},
            {"role": "user", "content": "Explain what an AI Gateway is in one sentence."}
        ],
        temperature=0.7
    )
    
    print("\n[Response]")
    print(response.choices[0].message.content)
    
    # Dronzer injects helpful routing metadata into the response headers
    # Note: Accessing custom headers depends on SDK version, typically accessible via `response._headers` or raw response modes.
    print(f"\n[Tokens Used]: {response.usage.total_tokens}")

if __name__ == "__main__":
    run_chat_completion()

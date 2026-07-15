// Official TypeScript SDK for Dronzer
// Generated via openapi-generator

export interface DronzerConfig {
  apiKey: string;
  baseUrl?: string;
}

export class DronzerClient {
  private apiKey: string;
  private baseUrl: string;

  constructor(config: DronzerConfig) {
    this.apiKey = config.apiKey;
    this.baseUrl = config.baseUrl || "https://api.dronzer.io/v1";
  }

  /**
   * Executes a Prompt Template using the Dronzer AI Gateway.
   * Handles A/B testing and failovers transparently.
   */
  async executePrompt(promptId: string, variables: Record<string, any>): Promise<string> {
    const response = await fetch(`${this.baseUrl}/llmops/prompts/${promptId}/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({ variables })
    });

    if (!response.ok) {
      throw new Error(`Dronzer API Error: ${response.statusText}`);
    }

    const data = await response.json();
    return data.output;
  }
}

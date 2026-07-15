# Dronzer LLMOps & PromptOps Guide

Welcome to the Dronzer LLMOps Platform. This guide outlines how to manage the full lifecycle of Prompt Engineering, AI Evaluation, and Production Experiments.

## 1. Prompt Registry & Versioning
Dronzer treats Prompts like code. 
- You do not edit a prompt in place; you create a new `PromptVersion` (e.g. `v1.2.0-draft`).
- Templates use **Jinja2** syntax. Variables like `{{ user_name }}` are strongly typed and enforced by the `PromptCompiler`.
- Use `{% if condition %}` to dynamically compose prompts based on context.

## 2. LLM-as-a-Judge Evaluation
Instead of manual testing, Dronzer automates quality assurance.
- Import **Golden Datasets** containing test queries and reference answers.
- Run the `LLMJudgeEvaluator`, which uses a superior model (like GPT-4o) to grade your target prompt/model on Factual Accuracy, Reasoning Quality, and Tone.

## 3. A/B Testing & Automatic Rollbacks
When deploying a new prompt version, never route 100% of traffic immediately.
- Use the **A/B Traffic Splitter** to route 10% of API requests to a "Challenger" version.
- The **ExperimentTracker** monitors the Challenger's Latency, Cost, and Error Rates.
- If the error rate exceeds 5%, the system triggers an **Automatic Rollback**, instantly routing all traffic back to the Champion version to protect production users.

## 4. Benchmarking & Side-by-Side Comparisons
Before switching from OpenAI to Anthropic, or GPT-4 to Llama-3:
- Use the **Side-by-Side Comparison** UI to visually inspect the difference in formatting, tone, and logic between models concurrently.
- Run the **BenchmarkEngine** to get hard data on TTFT (Time To First Token), TPS (Tokens Per Second), and relative costs.

## 5. Traces & Observability
Every execution through the Dronzer Gateway generates a deep trace. 
If an Agent hallucinates, you can inspect the exact input variables provided, the final rendered Jinja2 template sent to the model, and the raw token-by-token response to debug the issue.
